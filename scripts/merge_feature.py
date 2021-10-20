# -*- coding: utf-8 -*-
import argparse
import re
import subprocess
import sys
from typing import List

from .fork_release import create_develop_if_not_exists


def main():
    args = parse_args(sys.argv[1:])
    branch_name = f"feature-{args.feature_name}"

    cp = subprocess.run(["git", "branch"], stdout=subprocess.PIPE)
    if re.search(branch_name, cp.stdout.decode("utf-8")) is None:
        print(f"Branch {branch_name} doesn't exist.")
        exit(1)

    create_develop_if_not_exists()
    subprocess.run(["git", "checkout", "develop"])
    subprocess.run(["git", "merge", "--no-ff", branch_name])
    subprocess.run(["git", "branch", "-d", branch_name])


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser("merge_feature")
    parser.add_argument("feature_name")
    return parser.parse_args(argv)


if __name__ == "__main__":
    exit(main())
