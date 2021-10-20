# -*- coding: utf-8 -*-
import re


def fetch_version(file_path: str):
    with open(file_path) as file:
        match = re.compile(r"__version__\s*=\s*['\"](?P<VERSION>.*?)['\"]").search(
            file.read()
        )
    if not match:
        print(f"Failed to find version string in {file_path}")
        exit(667)
    return match.groupdict().get("VERSION")


__version__ = fetch_version("src/pygerber/__init__.py")


if __name__ == "__main__":
    print(__version__, end="")
