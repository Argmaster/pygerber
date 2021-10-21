# -*- coding: utf-8 -*-
import argparse
import subprocess
import sys
from typing import List

from .fork_release import create_develop_if_not_exists


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser("fork_feature")
    parser.add_argument("feature_name")
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    create_develop_if_not_exists()
    subprocess.run(["git", "checkout", "-b", f"feature-{args.feature_name}", "develop"])


if __name__ == "__main__":
    main()
