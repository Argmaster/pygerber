# -*- coding: utf-8 -*-
import argparse
import re
import subprocess
import sys
from subprocess import PIPE
from typing import List

import bumpversion
from bumpversion.cli import main as bumpversion_main

from .version_tag import __version__


def main():
    args = parse_args(sys.argv[1:])
    fork_branch(args.bump_type, "release")


def fork_branch(bump_type: str, branch_type: str):
    try:
        new_version = bump_version_string(__version__, bump_type)
    except ValueError as e:
        print(e)
        return 2
    BRANCH_NAME = f"{branch_type}-{new_version}"
    if not create_branch_with_version_bump(BRANCH_NAME, __version__, bump_type):
        message = f"Bumpversion failed, {BRANCH_NAME} branch won't be created."
        print("=" * len(message))
        print(message)
        print("Fix reported problems and retry.")
        print("=" * len(message))
        return 1
    else:
        return 0


def bump_version_string(current_version: str, bump_type: str) -> str:
    major, minor, patch = [int(x) for x in current_version.split(".")]

    if "patch" == bump_type:
        patch += 1
    elif "minor" == bump_type:
        patch = 0
        minor += 1
    elif "major" == bump_type:
        patch = 0
        minor = 0
        major += 1
    else:
        raise ValueError(f"Version type {bump_type} not supported.")
    return f"{major}.{minor}.{patch}"


def create_branch_with_version_bump(
    branch_name: str,
    current_version: str,
    bump_type: str,
    from_branch: str = "develop",
) -> None:
    create_develop_if_not_exists()
    subprocess.run(
        ["git", "checkout", "-b", branch_name, from_branch], stdout=PIPE, stderr=PIPE
    )
    try:
        bumpversion_main([bump_type, "--current-version", current_version])
    except Exception:
        subprocess.run(["git", "checkout", from_branch], stdout=PIPE, stderr=PIPE)
        subprocess.run(["git", "branch", "-D", branch_name], stdout=PIPE, stderr=PIPE)
        return False
    return True


def create_develop_if_not_exists():
    cp = subprocess.run(["git", "branch"], stdout=subprocess.PIPE)
    if re.search(r"develop", cp.stdout.decode("utf-8")) is None:
        subprocess.run(["git", "checkout", "-b", "develop", "main"])


def parse_args(argv: List[str]):
    parser = argparse.ArgumentParser("fork_release")
    group = parser.add_mutually_exclusive_group(required=True)
    for flag in ("patch", "minor", "major"):
        group.add_argument(
            f"--{flag}",
            required=False,
            dest="bump_type",
            action="store_const",
            const=flag,
        )
    return parser.parse_args(argv)


if __name__ == "__main__":
    print("Bumpversion version:", bumpversion.__version__)
    exit(main())
