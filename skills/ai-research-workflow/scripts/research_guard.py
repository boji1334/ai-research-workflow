#!/usr/bin/env python3
"""Mechanical research guardrails. Never launches commands or judges science."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class GuardError(ValueError):
    """A contract or recorded transition needs attention."""


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise GuardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise GuardError(f"non-finite JSON number: {value}")


def _float(value):
    number = float(value)
    if not math.isfinite(number):
        raise GuardError(f"non-finite JSON number: {value}")
    return number


def read_json(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        return json.load(stream, object_pairs_hook=_pairs, parse_constant=_constant,
                         parse_float=_float)


def digest(value):
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def value_at(value, path):
    for key in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def timezone_for(name):
    if name in ("UTC", "Z"):
        return timezone.utc
    match = re.fullmatch(r"([+-])(\d{2}):(\d{2})", name or "")
    if match:
        hours, minutes = int(match[2]), int(match[3])
        if hours > 23 or minutes > 59:
            raise GuardError("invalid UTC offset")
        delta = timedelta(hours=hours, minutes=minutes)
        return timezone(delta if match[1] == "+" else -delta)
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise GuardError("timezone unavailable; use UTC or a fixed offset such as +08:00") from exc


TEXT_FIELDS = (
    "project.task", "project.bottleneck", "project.data_roles.train",
    "project.data_roles.validation", "project.data_roles.test", "project.baseline",
    "project.prior_attempts", "project.fixed_constraints", "project.allowed_changes",
    "resources.execution_target", "resources.compute_budget", "resources.storage_budget",
    "resources.execution_owner", "publication.target.value", "publication.target.access",
    "publication.requirements_source", "publication.start_date", "publication.deadline",
    "publication.timezone", "acceptance.primary_metric", "acceptance.scale",
    "acceptance.rationale", "acceptance.repeat_plan",
)


def contract_errors(contract, now=None):
    errors = []
    if not isinstance(contract, dict):
        return ["contract must be a JSON object"]
    if type(contract.get("schema_version")) is not int or contract["schema_version"] != 1:
        errors.append("schema_version must be 1")
    for field in TEXT_FIELDS:
        if not nonempty(value_at(contract, field)):
            errors.append(f"missing non-empty text: {field}")
    for field in ("intake.fact_sources", "acceptance.fairness_controls",
                  "acceptance.evidence_requirements"):
        items = value_at(contract, field)
        if not isinstance(items, list) or not items or not all(nonempty(x) for x in items):
            errors.append(f"non-empty text list required: {field}")
    for field in ("intake.project_gaps", "intake.publication_gaps"):
        if value_at(contract, field) != []:
            errors.append(f"resolve requirement gaps first: {field}")
    if value_at(contract, "intake.sequence") != ["project", "publication"]:
        errors.append("record completed project intake before publication intake")
    if not isinstance(value_at(contract, "resources.active_runs"), list):
        errors.append("resources.active_runs must be a list, including when empty")
    total = value_at(contract, "resources.max_total_runs")
    if type(total) is not int or total < 1:
        errors.append("resources.max_total_runs must be a positive integer")
    if value_at(contract, "publication.target.kind") not in ("journal", "tier"):
        errors.append("publication.target.kind must be journal or tier")
    if value_at(contract, "acceptance.direction") not in ("max", "min"):
        errors.append("acceptance.direction must be max or min")
    effect = value_at(contract, "acceptance.min_effect")
    try:
        valid_effect = type(effect) in (int, float) and math.isfinite(effect) and effect > 0
    except OverflowError:
        valid_effect = False
    if not valid_effect:
        errors.append("acceptance.min_effect must be a finite positive number in the stated scale")
    try:
        start = date.fromisoformat(value_at(contract, "publication.start_date"))
        deadline = date.fromisoformat(value_at(contract, "publication.deadline"))
        zone = timezone_for(value_at(contract, "publication.timezone"))
        today = (now or datetime.now(timezone.utc)).astimezone(zone).date()
        if deadline < start:
            errors.append("deadline precedes start_date")
        if today < start:
            errors.append("research period has not started")
        if today > deadline:
            errors.append("deadline has passed; deliver partial results or resolve a period change")
    except (TypeError, ValueError) as exc:
        errors.append(f"invalid period: {exc}")
    try:
        # Unknown extension fields must also be serializable under the frozen digest.
        digest(contract)
    except (TypeError, ValueError, OverflowError) as exc:
        errors.append(f"contract is not canonical JSON: {exc}")
    return errors


def require_contract(contract, now=None):
    errors = contract_errors(contract, now)
    if errors:
        raise GuardError("; ".join(errors))


def is_hash(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def canonical_registry(path):
    # All cooperative readers/writers and their locks address the same target.
    resolved = Path(path).resolve()
    if resolved.exists() and resolved.stat().st_nlink > 1:
        raise GuardError("hard-linked registries are unsupported; use one canonical registry file")
    return resolved


def read_registry(path):
    registry = read_json(canonical_registry(path))
    if (not isinstance(registry, dict) or type(registry.get("schema_version")) is not int
            or registry["schema_version"] != 1):
        raise GuardError("unsupported registry schema")
    if not is_hash(registry.get("contract_sha256")) or not isinstance(registry.get("runs"), list):
        raise GuardError("malformed registry")
    if not nonempty(registry.get("created_at")):
        raise GuardError("registry creation timestamp is missing")
    ids, fingerprints, histories = set(), set(), {}
    for run in registry["runs"]:
        if not isinstance(run, dict):
            raise GuardError("malformed run")
        if not nonempty(run.get("id")) or not nonempty(run.get("candidate")):
            raise GuardError("run identity is missing")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", run["candidate"]):
            raise GuardError("malformed candidate family ID")
        if run.get("kind") not in ("pilot", "repair", "confirm"):
            raise GuardError("unknown run kind")
        if run.get("status") not in ("reserved", "finished"):
            raise GuardError("unknown run status")
        if run["status"] == "finished" and run.get("outcome") not in (
                "gain", "no_gain", "invalid", "cancelled"):
            raise GuardError("finished run has no valid outcome")
        for field in ("command", "budget", "reserved_at"):
            if not nonempty(run.get(field)):
                raise GuardError(f"run field is missing: {field}")
        if run["status"] == "finished":
            evidence = run.get("evidence")
            if (not nonempty(run.get("finished_at")) or not isinstance(evidence, dict)
                    or not nonempty(evidence.get("path")) or not is_hash(evidence.get("sha256"))):
                raise GuardError("finished run has incomplete evidence metadata")
        elif any(field in run for field in ("outcome", "evidence", "finished_at")):
            raise GuardError("reserved run contains finished-state fields")
        fingerprint = run.get("fingerprint")
        if not is_hash(fingerprint) or fingerprint in fingerprints or run["id"] in ids:
            raise GuardError("duplicate or malformed run identity/fingerprint")
        ids.add(run["id"])
        fingerprints.add(fingerprint)
        family = histories.setdefault(run["candidate"], [])
        if not family:
            if run["kind"] != "pilot":
                raise GuardError("candidate history must start with a pilot")
        else:
            previous = family[-1]
            if previous["status"] != "finished":
                raise GuardError("candidate history overlaps an unsettled run")
            if run["kind"] == "pilot":
                raise GuardError("candidate history contains multiple pilots")
            if run["kind"] == "repair":
                if sum(item["kind"] == "repair" for item in family) >= 2:
                    raise GuardError("candidate history exceeds two repair rounds")
                if previous["outcome"] not in ("no_gain", "invalid", "cancelled"):
                    raise GuardError("repair history has no prior negative/invalid evidence")
                if not nonempty(run.get("reason")):
                    raise GuardError("repair history is missing its hypothesis")
            if run["kind"] == "confirm" and previous["outcome"] != "gain":
                raise GuardError("confirmation history has no prior gain")
        family.append(run)
    return registry


@contextmanager
def registry_lock(path):
    lock = Path(str(canonical_registry(path)) + ".lock")
    try:
        descriptor = os.open(str(lock), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise GuardError(f"registry is locked: {lock}; inspect the owner before cleanup") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "created_at": timestamp()}, stream)
        yield
    finally:
        lock.unlink()


def atomic_write(path, value, create=False):
    path = canonical_registry(path)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if create:
            # Publish a fully written file atomically without replacing any target.
            # NTFS/ext4 support this; unsupported filesystems fail without partial state.
            os.link(temporary, path)
        else:
            os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def initialize(contract_path, registry_path, now=None):
    contract = read_json(contract_path)
    require_contract(contract, now)
    registry_path = canonical_registry(registry_path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry = {"schema_version": 1, "created_at": timestamp(),
                "contract_sha256": digest(contract), "runs": []}
    with registry_lock(registry_path):
        atomic_write(registry_path, registry, create=True)
    return registry


def reserve(contract_path, registry_path, candidate, kind, fingerprint,
            command, budget, reason="", now=None):
    registry_path = canonical_registry(registry_path)
    contract = read_json(contract_path)
    require_contract(contract, now)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", candidate):
        raise GuardError("candidate must be a stable lowercase mechanism-family slug")
    fingerprint = fingerprint.lower()
    if not is_hash(fingerprint):
        raise GuardError("fingerprint must be a SHA-256 hex digest of real run inputs")
    if kind not in ("pilot", "repair", "confirm"):
        raise GuardError("unknown run kind")
    if not nonempty(command) or not nonempty(budget):
        raise GuardError("record the exact command and bounded run budget")
    with registry_lock(registry_path):
        registry = read_registry(registry_path)
        if registry["contract_sha256"] != digest(contract):
            raise GuardError("contract changed; preserve history and resolve protocol migration first")
        runs = registry["runs"]
        if len(runs) >= contract["resources"]["max_total_runs"]:
            raise GuardError("total registered run budget is exhausted")
        if any(run["fingerprint"] == fingerprint for run in runs):
            raise GuardError("duplicate fingerprint; inspect existing run artifacts")
        family = [run for run in runs if run["candidate"] == candidate]
        if any(run["status"] == "reserved" for run in family):
            raise GuardError("candidate already has an unsettled run; inspect its actual process")
        if kind == "pilot" and family:
            raise GuardError("candidate already has a pilot; preserve its history")
        if kind != "pilot" and not family:
            raise GuardError("pilot evidence is required first")
        if kind == "repair":
            if sum(run["kind"] == "repair" for run in family) >= 2:
                raise GuardError("two repair rounds already reserved; close this candidate")
            if family[-1].get("outcome") not in ("no_gain", "invalid", "cancelled"):
                raise GuardError("repair requires settled negative or invalid pilot evidence")
            if not nonempty(reason):
                raise GuardError("repair requires a specific evidence-based hypothesis")
        if kind == "confirm" and family[-1].get("outcome") != "gain":
            raise GuardError("confirmation requires preliminary gain and scientific review")
        run = {"id": "run-" + uuid.uuid4().hex[:12], "candidate": candidate,
               "kind": kind, "fingerprint": fingerprint, "command": command,
               "budget": budget, "reason": reason, "status": "reserved",
               "reserved_at": timestamp()}
        runs.append(run)
        atomic_write(registry_path, registry)
    return run


def finish(registry_path, run_id, outcome, evidence_path):
    registry_path = canonical_registry(registry_path)
    if outcome not in ("gain", "no_gain", "invalid", "cancelled"):
        raise GuardError("unknown outcome")
    evidence_path = Path(evidence_path).resolve(strict=True)
    if not evidence_path.is_file():
        raise GuardError("evidence must be an existing result/log file")
    file_hash = hashlib.sha256()
    with evidence_path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            file_hash.update(block)
    with registry_lock(registry_path):
        registry = read_registry(registry_path)
        run = next((item for item in registry["runs"] if item["id"] == run_id), None)
        if run is None:
            raise GuardError("unknown run ID")
        if run["status"] != "reserved":
            raise GuardError("run already finished; preserve the original outcome")
        run.update(status="finished", outcome=outcome, finished_at=timestamp(),
                   evidence={"path": str(evidence_path), "sha256": file_hash.hexdigest()})
        atomic_write(registry_path, registry)
    return run


def status(registry_path):
    registry = read_registry(registry_path)
    families = {}
    for run in registry["runs"]:
        entry = families.setdefault(run["candidate"], {"repair_slots_used": 0, "unsettled": []})
        entry["repair_slots_used"] += int(run["kind"] == "repair")
        if run["status"] == "reserved":
            entry["unsettled"].append(run["id"])
        entry["last_outcome"] = run.get("outcome")
    return {"total_registered": len(registry["runs"]), "candidates": families,
            "note": "Registry state is not a live process check or a scientific verdict."}


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    check = commands.add_parser("check-contract")
    check.add_argument("--contract", required=True)
    init = commands.add_parser("init")
    init.add_argument("--contract", required=True)
    init.add_argument("--registry", required=True)
    begin = commands.add_parser("reserve")
    begin.add_argument("--contract", required=True)
    begin.add_argument("--registry", required=True)
    begin.add_argument("--candidate", required=True)
    begin.add_argument("--kind", choices=("pilot", "repair", "confirm"), required=True)
    begin.add_argument("--fingerprint", required=True)
    begin.add_argument("--command", required=True)
    begin.add_argument("--budget", required=True)
    begin.add_argument("--reason", default="")
    end = commands.add_parser("finish")
    end.add_argument("--registry", required=True)
    end.add_argument("--run-id", required=True)
    end.add_argument("--outcome", choices=("gain", "no_gain", "invalid", "cancelled"), required=True)
    end.add_argument("--evidence", required=True)
    show = commands.add_parser("status")
    show.add_argument("--registry", required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "check-contract":
            errors = contract_errors(read_json(args.contract))
            result = {"ready": not errors, "errors": errors,
                      "scope": "Structural completeness only; verify facts and scientific validity separately."}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return int(bool(errors))
        if args.action == "init":
            result = initialize(args.contract, args.registry)
        elif args.action == "reserve":
            result = reserve(args.contract, args.registry, args.candidate, args.kind,
                             args.fingerprint, args.command, args.budget, args.reason)
        elif args.action == "finish":
            result = finish(args.registry, args.run_id, args.outcome, args.evidence)
        else:
            result = status(args.registry)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError, OverflowError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
