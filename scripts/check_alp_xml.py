from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALP_ROOT = ROOT / "src" / "UAV-SAR" / "_alp"
REQUIRED_PATHS = [
    ROOT / "src" / "UAV-SAR" / "UAV-SAR.alpx",
    ALP_ROOT / "Agents" / "UAV" / "AOC.UAV.xml",
    ALP_ROOT / "Agents" / "UAV" / "Code" / "Functions.java",
    ALP_ROOT / "Agents" / "Main" / "Code" / "Functions.java",
]
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
EMPTY_CODE_BLOCK = re.compile(r"<Code>(?:\s|<!\[CDATA\[|\]\]>)*</Code>", re.S)


def collect_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ALP_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".xml", ".java"}:
            files.append(path)
    return sorted(files)


def parse_xml(path: Path) -> ET.ElementTree:
    return ET.parse(path)


def main() -> int:
    failures: list[str] = []
    xml_files = [path for path in collect_text_files() if path.suffix.lower() == ".xml"]

    for required in REQUIRED_PATHS:
        if not required.exists():
            failures.append(f"MISSING: {required}")

    for path in collect_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")

        if any(marker in text for marker in CONFLICT_MARKERS):
            failures.append(f"CONFLICT MARKER: {path}")

        if path.suffix.lower() == ".xml":
            try:
                parse_xml(path)
            except ET.ParseError as exc:
                failures.append(f"XML PARSE: {path}: {exc}")
                continue

            if EMPTY_CODE_BLOCK.search(text):
                failures.append(f"EMPTY CODE BLOCK: {path}")

    if failures:
        print("FOUND ERRORS:")
        for failure in failures:
            print(failure)
        return 1

    print(f"OK: {len(xml_files)} XML files parsed and checked successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())