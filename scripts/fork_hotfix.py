# -*- coding: utf-8 -*-
from .fork_release import fork_branch


def main():
    fork_branch("patch", "hotfix")


if __name__ == "__main__":
    exit(main())
