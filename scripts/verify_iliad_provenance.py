#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "c9802c782a3e47bd44873884260c13213b6ee380"
BASELINE_TREE = "6f4860a5c85f374afce86cce61b16bf6f9e6db36"
BASELINE_SRC = "cb12a962c9a0879816fa0bd069e40d83c127c57a"
JATTE_SRC = "f13cbdd600e4e18bb63ea8aaeb735cdbbc0892d3"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def main() -> None:
    provenance = json.loads((ROOT / "ILIAD_PROVENANCE.json").read_text())
    expected = {
        "upstream_baseline_commit": BASELINE,
        "upstream_baseline_tree": BASELINE_TREE,
        "upstream_baseline_src_tree": BASELINE_SRC,
        "source_jatte_src_tree": JATTE_SRC,
    }
    for key, value in expected.items():
        if provenance.get(key) != value:
            raise SystemExit(f"provenance mismatch for {key}")
    subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASELINE, "HEAD"],
        check=True,
    )
    if git("rev-parse", f"{BASELINE}^{{tree}}") != BASELINE_TREE:
        raise SystemExit("baseline repository tree mismatch")
    if git("rev-parse", f"{BASELINE}:src") != BASELINE_SRC:
        raise SystemExit("baseline source tree mismatch")
    if git("rev-parse", "HEAD:src") != JATTE_SRC:
        raise SystemExit("reconciled source tree mismatch")
    boundary = subprocess.run(
        ["git", "-C", str(ROOT), "grep", "-l", "@iliad/realtime", "--", "src", "package.json"],
        text=True,
        capture_output=True,
    )
    if boundary.returncode not in (0, 1):
        raise SystemExit(boundary.stderr.strip())
    if boundary.stdout.strip():
        raise SystemExit(f"forbidden @iliad/realtime dependency: {boundary.stdout.strip()}")


if __name__ == "__main__":
    main()
