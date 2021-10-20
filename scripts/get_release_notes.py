# -*- coding: utf-8 -*-
import argparse
import re
import sys
from typing import Dict, List

VERSION_CHANGELOG_RE = re.compile(
    r"(?P<VERSION>\d+\.\d+\.\d+)\s+\(\d+-\d+-\d+\)\s+-+\s+"
    r"(?P<CHANGES>(\*\s+.*?\n)+(\*\s+.*)*)"
)


def main():
    args = parse_args(sys.argv[1:])
    notes = generate_release_notes(args.version)
    if args.file is not None:
        with open(args.file, "w", encoding="utf-8") as file:
            file.write(notes)
    if args.print:
        print(notes)


def parse_args(argv: List[str]):
    parser = argparse.ArgumentParser("get_release_notes")
    parser.add_argument("--version", default="last")
    parser.add_argument("--file", default=None)
    parser.add_argument("--print", default=False, action="store_true")
    return parser.parse_args(argv)


def generate_release_notes(version: str = "last"):
    version_logs, prev_last_version, last_version = parse_version_logs()
    changes = version_logs.get(version, "")
    if prev_last_version is not None and last_version is not None:
        link = (
            f"*Full list of changes:* [v{prev_last_version}...v{last_version}]"
            f"(https://github.com/Argmaster/test-project/compare/v{prev_last_version}...v{last_version})"
        )
    else:
        link = ""
    return RELESE_NOTES.format(changelog=changes, link=link)


def parse_version_logs() -> Dict[str, str]:
    with open("CHANGELOG.rst") as file:
        changelog = file.read()
    version_logs = {}
    prev_last_version = None
    last_version = None
    for match in VERSION_CHANGELOG_RE.finditer(changelog):
        match_dict = match.groupdict()
        version_logs[match_dict.get("VERSION")] = match_dict.get("CHANGES")
        prev_last_version = last_version
        last_version = match_dict.get("VERSION")
    if version_logs:
        version_logs["last"] = match_dict.get("CHANGES")
    return version_logs, prev_last_version, last_version


RELESE_NOTES = """# Release Notes
### What's Changed

{changelog}

{link}

"""


if __name__ == "__main__":
    main()
