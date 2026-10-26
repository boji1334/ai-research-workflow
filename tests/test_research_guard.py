"""Synthetic guardrail tests; these are not scientific experimental results."""

import copy
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/ai-research-workflow/scripts/research_guard.py"
SPEC = importlib.util.spec_from_file_location("research_guard", SCRIPT)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def contract_fixture():
    """Fully synthetic fields, with a current relative period to avoid stale tests."""
    today = datetime.now(timezone.utc).date()
    return {
        "schema_version": 1,
        "intake": {"sequence": ["project", "publication"], "project_gaps": [],
                   "publication_gaps": [], "fact_sources": ["synthetic test fixture"]},
        "project": {"task": "synthetic defect detection fixture", "bottleneck": "fixture",
                    "data_roles": {"train": "fixture train", "validation": "fixture val",
                                   "test": "fixture held out"},
                    "baseline": "fixture baseline", "prior_attempts": "none, synthetic fixture",
                    "fixed_constraints": "fixture backbone", "allowed_changes": "fixture head"},
        "resources": {"execution_target": "no actual execution", "compute_budget": "zero GPU",
                      "storage_budget": "temporary test files", "active_runs": [],
                      "execution_owner": "test", "max_total_runs": 10},
        "publication": {"target": {"kind": "tier", "value": "synthetic target",
                                    "access": "unspecified by fixture"},
                        "requirements_source": "synthetic fixture; no real journal claim",
                        "start_date": (today - timedelta(days=2)).isoformat(),
                        "deadline": (today + timedelta(days=2)).isoformat(), "timezone": "UTC"},
        "acceptance": {"primary_metric": "synthetic AP", "direction": "max", "min_effect": 1.0,
                       "scale": "percentage points", "rationale": "fixture only",
                       "repeat_plan": "fixture seeds", "fairness_controls": ["fixture controls"],
                       "evidence_requirements": ["fixture evidence"]},
    }


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.contract = contract_fixture()
        self.contract_path = self.root / "contract.json"
        self.registry = self.root / "runs.json"
        self.evidence = self.root / "result.json"
        self.evidence.write_text('{"synthetic": true}', encoding="utf-8")
        self.save_contract()
        guard.initialize(self.contract_path, self.registry)

    def save_contract(self):
        self.contract_path.write_text(json.dumps(self.contract), encoding="utf-8")

    def begin(self, tag, kind="pilot", candidate="mechanism-a", reason=""):
        return guard.reserve(self.contract_path, self.registry, candidate, kind,
                             hashlib.sha256(tag.encode()).hexdigest(),
                             "NOT EXECUTED: fixture command", "zero GPU", reason)

    def settle(self, run, outcome="no_gain"):
        return guard.finish(self.registry, run["id"], outcome, self.evidence)

    def test_template_is_not_ready(self):
        template = guard.read_json(ROOT / "skills/ai-research-workflow/assets/research-contract.json")
        self.assertTrue(guard.contract_errors(template))

    def test_project_gaps_and_wrong_intake_order_stop_reservation(self):
        for field, value in (("project_gaps", ["unknown data split"]),
                             ("sequence", ["publication", "project"])):
            changed = copy.deepcopy(self.contract)
            changed["intake"][field] = value
            self.assertTrue(guard.contract_errors(changed))

    def test_complete_contract_passes(self):
        self.assertEqual(guard.contract_errors(self.contract), [])

    def test_duplicate_fingerprint_preserves_registry(self):
        first = self.begin("same")
        self.settle(first)
        before = self.registry.read_bytes()
        with self.assertRaisesRegex(guard.GuardError, "duplicate fingerprint"):
            self.begin("same", "repair", reason="fixture hypothesis")
        self.assertEqual(self.registry.read_bytes(), before)

    def test_unsettled_candidate_does_not_start_again(self):
        self.begin("pilot")
        with self.assertRaisesRegex(guard.GuardError, "unsettled"):
            self.begin("repair", "repair", reason="fixture hypothesis")

    def test_two_repair_rounds_survive_reload(self):
        self.settle(self.begin("pilot"))
        self.settle(self.begin("repair1", "repair", reason="fixture hypothesis one"))
        self.settle(self.begin("repair2", "repair", reason="fixture hypothesis two"))
        self.assertEqual(guard.status(self.registry)["candidates"]["mechanism-a"]["repair_slots_used"], 2)
        with self.assertRaisesRegex(guard.GuardError, "two repair rounds"):
            self.begin("repair3", "repair", reason="fixture hypothesis three")

    def test_cancelled_and_invalid_repairs_keep_slots(self):
        self.settle(self.begin("pilot"), "invalid")
        self.settle(self.begin("repair1", "repair", reason="fixture fix"), "cancelled")
        self.settle(self.begin("repair2", "repair", reason="fixture fix"), "invalid")
        with self.assertRaisesRegex(guard.GuardError, "two repair rounds"):
            self.begin("repair3", "repair", reason="fixture fix")

    def test_confirmation_requires_gain(self):
        run = self.begin("pilot")
        self.settle(run)
        with self.assertRaisesRegex(guard.GuardError, "preliminary gain"):
            self.begin("confirm", "confirm")

    def test_gain_allows_confirmation_not_automatic_success(self):
        self.settle(self.begin("pilot"), "gain")
        run = self.begin("confirm", "confirm")
        self.assertEqual(run["status"], "reserved")
        self.assertNotIn("research_success", guard.status(self.registry))

    def test_changed_contract_is_not_silently_adopted(self):
        self.contract["resources"]["max_total_runs"] = 20
        self.save_contract()
        with self.assertRaisesRegex(guard.GuardError, "contract changed"):
            self.begin("pilot")

    def test_initialization_never_overwrites_history(self):
        self.begin("pilot")
        before = self.registry.read_bytes()
        with self.assertRaises(FileExistsError):
            guard.initialize(self.contract_path, self.registry)
        self.assertEqual(self.registry.read_bytes(), before)

    def test_lock_excludes_other_writer_and_is_preserved(self):
        lock = Path(str(self.registry) + ".lock")
        lock.write_text("another writer", encoding="utf-8")
        with self.assertRaisesRegex(guard.GuardError, "locked"):
            self.begin("pilot")
        self.assertEqual(lock.read_text(encoding="utf-8"), "another writer")

    def test_lock_released_after_rejected_transition(self):
        self.begin("pilot")
        with self.assertRaises(guard.GuardError):
            self.begin("bad-second-pilot")
        self.assertFalse(Path(str(self.registry) + ".lock").exists())

    def test_total_budget_counts_all_reserved_runs(self):
        self.registry.unlink()
        self.contract["resources"]["max_total_runs"] = 1
        self.save_contract()
        guard.initialize(self.contract_path, self.registry)
        self.settle(self.begin("pilot"), "cancelled")
        with self.assertRaisesRegex(guard.GuardError, "budget is exhausted"):
            self.begin("other", candidate="mechanism-b")

    def test_deadline_uses_contract_timezone(self):
        contract = copy.deepcopy(self.contract)
        contract["publication"].update(start_date="2026-10-01", deadline="2026-10-26", timezone="+08:00")
        before_midnight = datetime(2026, 10, 26, 15, 59, tzinfo=timezone.utc)
        after_midnight = datetime(2026, 10, 26, 16, 1, tzinfo=timezone.utc)
        self.assertEqual(guard.contract_errors(contract, before_midnight), [])
        self.assertTrue(any("deadline has passed" in item for item in guard.contract_errors(contract, after_midnight)))

    def test_expired_contract_stops_reservation_but_allows_settlement(self):
        run = self.begin("pilot")
        future = datetime.now(timezone.utc) + timedelta(days=5)
        with self.assertRaisesRegex(guard.GuardError, "deadline has passed"):
            guard.reserve(self.contract_path, self.registry, "mechanism-b", "pilot", "a" * 64,
                          "fixture command", "zero GPU", now=future)
        self.settle(run)
        self.assertEqual(guard.status(self.registry)["total_registered"], 1)

    def test_evidence_hash_matches_actual_file_and_outcome_is_immutable(self):
        run = self.begin("pilot")
        result = self.settle(run)
        self.assertEqual(result["evidence"]["sha256"], hashlib.sha256(self.evidence.read_bytes()).hexdigest())
        with self.assertRaisesRegex(guard.GuardError, "already finished"):
            self.settle(run, "gain")

    def test_missing_evidence_does_not_finish_run(self):
        run = self.begin("pilot")
        with self.assertRaises(FileNotFoundError):
            guard.finish(self.registry, run["id"], "gain", self.root / "missing.json")
        self.assertEqual(guard.read_registry(self.registry)["runs"][0]["status"], "reserved")

    def test_nonfinite_and_boolean_effects_fail(self):
        for value in (float("nan"), float("inf"), True, 0, -1, 10 ** 400):
            contract = copy.deepcopy(self.contract)
            contract["acceptance"]["min_effect"] = value
            self.assertTrue(guard.contract_errors(contract))

    def test_duplicate_json_keys_are_rejected(self):
        path = self.root / "duplicate.json"
        path.write_text('{"schema_version":1,"schema_version":2}', encoding="utf-8")
        with self.assertRaisesRegex(guard.GuardError, "duplicate JSON key"):
            guard.read_json(path)

    def test_cli_does_not_execute_recorded_command(self):
        marker = self.root / "command-was-executed"
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "reserve", "--contract", str(self.contract_path),
             "--registry", str(self.registry), "--candidate", "fixture", "--kind", "pilot",
             "--fingerprint", "b" * 64, "--command", "create " + str(marker), "--budget", "zero GPU"],
            capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "reserved")
        self.assertFalse(marker.exists())

    def test_symlink_alias_shares_lock_and_updates_canonical_file(self):
        alias = self.root / "alias.json"
        try:
            alias.symlink_to(self.registry)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"file symlink creation unavailable: {exc}")
        with guard.registry_lock(self.registry):
            with self.assertRaisesRegex(guard.GuardError, "locked"):
                guard.reserve(self.contract_path, alias, "mechanism-a", "pilot", "d" * 64,
                              "fixture command", "zero GPU")
        run = guard.reserve(self.contract_path, alias, "mechanism-a", "pilot", "d" * 64,
                            "fixture command", "zero GPU")
        self.assertTrue(alias.is_symlink())
        self.assertEqual(guard.read_registry(self.registry)["runs"][0]["id"], run["id"])
        self.assertEqual(guard.read_registry(alias), guard.read_registry(self.registry))
        guard.finish(alias, run["id"], "no_gain", self.evidence)
        with self.assertRaisesRegex(guard.GuardError, "duplicate fingerprint"):
            guard.reserve(self.contract_path, self.registry, "mechanism-a", "repair", "d" * 64,
                          "fixture command", "zero GPU", "fixture fix")

    def test_hardlinked_registries_are_rejected(self):
        alias = self.root / "hardlink.json"
        try:
            os.link(self.registry, alias)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"hard links unavailable: {exc}")
        before = self.registry.read_bytes()
        with self.assertRaisesRegex(guard.GuardError, "hard-linked"):
            self.begin("pilot")
        self.assertEqual(self.registry.read_bytes(), before)

    def test_cli_utf8_output_even_when_parent_requests_gbk(self):
        environment = dict(os.environ, PYTHONIOENCODING="gbk", PYTHONUTF8="0")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "reserve", "--contract", str(self.contract_path),
             "--registry", str(self.registry), "--candidate", "fixture", "--kind", "pilot",
             "--fingerprint", "e" * 64, "--command", "fixture 🚀 中文", "--budget", "zero GPU"],
            capture_output=True, encoding="utf-8", env=environment, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        run = json.loads(completed.stdout)
        self.assertEqual(run["command"], "fixture 🚀 中文")
        self.assertEqual(guard.read_registry(self.registry)["runs"][0]["id"], run["id"])

    def test_failed_initial_write_leaves_no_partial_registry(self):
        self.registry.unlink()
        real_dump = guard.json.dump

        def partial_dump(value, stream, *args, **kwargs):
            if isinstance(value, dict) and "schema_version" in value:
                stream.write('{"schema_version":1,')
                raise OSError("synthetic disk-write failure")
            return real_dump(value, stream, *args, **kwargs)

        with mock.patch.object(guard.json, "dump", side_effect=partial_dump):
            with self.assertRaisesRegex(OSError, "synthetic disk-write failure"):
                guard.initialize(self.contract_path, self.registry)
        self.assertFalse(self.registry.exists())
        self.assertEqual(list(self.root.glob("*.tmp")), [])
        self.assertFalse(Path(str(self.registry) + ".lock").exists())
        guard.initialize(self.contract_path, self.registry)
        self.assertEqual(guard.status(self.registry)["total_registered"], 0)

    def test_failed_replace_preserves_previous_registry(self):
        before = self.registry.read_bytes()
        with mock.patch.object(guard.os, "replace", side_effect=OSError("synthetic replace failure")):
            with self.assertRaisesRegex(OSError, "synthetic replace failure"):
                self.begin("pilot")
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertEqual(list(self.root.glob("*.tmp")), [])
        self.assertFalse(Path(str(self.registry) + ".lock").exists())

    def test_corrupt_history_without_pilot_is_rejected(self):
        self.settle(self.begin("pilot"))
        value = guard.read_registry(self.registry)
        value["runs"][0]["kind"] = "repair"
        value["runs"][0]["reason"] = "fixture hypothesis"
        self.registry.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(guard.GuardError, "must start with a pilot"):
            self.begin("repair", "repair", reason="fixture hypothesis")

    def test_finished_history_requires_evidence_metadata(self):
        self.settle(self.begin("pilot"))
        value = guard.read_registry(self.registry)
        del value["runs"][0]["evidence"]
        self.registry.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(guard.GuardError, "incomplete evidence"):
            guard.read_registry(self.registry)

    def test_exponent_overflow_in_extension_field_is_structured_error(self):
        self.contract_path.write_text(json.dumps(self.contract)[:-1] + ',"extra":1e999}', encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "check-contract", "--contract", str(self.contract_path)],
            capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("non-finite", json.loads(completed.stderr)["error"])
        self.assertNotIn("Traceback", completed.stderr)

    def test_huge_effect_is_controlled_validation_failure(self):
        self.contract["acceptance"]["min_effect"] = 10 ** 400
        self.save_contract()
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "check-contract", "--contract", str(self.contract_path)],
            capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(completed.returncode, 1)
        self.assertFalse(json.loads(completed.stdout)["ready"])
        self.assertNotIn("Traceback", completed.stderr)

    def test_non_utf8_input_has_structured_error(self):
        self.registry.write_bytes(b"\xff")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "status", "--registry", str(self.registry)],
            capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("error", json.loads(completed.stderr))
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
