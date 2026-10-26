#!/usr/bin/env python3
"""Check skill packaging, relative links and parseable Python/JSON using stdlib."""

import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/industrial-vision-research"


def main():
    errors = []
    for required in ("README.md", "LICENSE", "docs/VALIDATION.md", "skills/industrial-vision-research/SKILL.md",
                     "skills/industrial-vision-research/agents/openai.yaml",
                     "skills/industrial-vision-research/references/sources.md"):
        if not (ROOT / required).is_file():
            errors.append(f"missing {required}")
    files = [p for p in ROOT.rglob("*") if p.is_file() and not any(
        part in (".git", "__pycache__", ".venv") for part in p.relative_to(ROOT).parts)]
    for path in files:
        if path.suffix not in (".py", ".json", ".md", ".yaml", ".yml"):
            continue
        try:
            content = path.read_text(encoding="utf-8")
            if path.suffix == ".py":
                ast.parse(content, filename=str(path))
            elif path.suffix == ".json":
                json.loads(content)
            elif path.suffix == ".md":
                # Remove fenced command samples before checking actual Markdown links.
                prose = re.sub(r"```.*?```", "", content, flags=re.S)
                for destination in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
                    destination = destination.split("#", 1)[0]
                    if not destination or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", destination):
                        continue
                    target = (path.parent / unquote(destination)).resolve()
                    if not target.is_relative_to(ROOT) or not target.exists():
                        errors.append(f"broken/outside relative link: {path.relative_to(ROOT)} -> {destination}")
        except (UnicodeError, SyntaxError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", entry, flags=re.S)
    if not match or not re.search(r"^name: industrial-vision-research$", match[1], re.M):
        errors.append("invalid or mismatched skill frontmatter name")
    if not match or not re.search(r"^description: .+", match[1], re.M):
        errors.append("missing skill description")
    if len(entry.splitlines()) > 220:
        errors.append("entrypoint grew beyond this repository's 220-line maintenance limit")
    print(json.dumps({"ok": not errors, "checked_files": len(files), "errors": errors}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
