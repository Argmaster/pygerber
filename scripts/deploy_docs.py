from __future__ import annotations

import sys

import click
import dulwich
import dulwich.porcelain
import dulwich.repo
from mike.driver import main as mike_main
from packaging.version import Version
from test import THIS_DIRECTORY

import pygerber


@click.command()
@click.option("--is-dev", is_flag=True, default=False)
@click.option("--check-only", is_flag=True, default=False)
def main(*, is_dev: bool, check_only: bool) -> None:
    version = Version(pygerber.__version__)

    is_unstable = version.is_devrelease or version.is_prerelease
    aliases = []

    repo = dulwich.repo.Repo((THIS_DIRECTORY / ".." / ".git").as_posix())
    versions = [Version(t.decode("utf-8")) for t in dulwich.porcelain.tag_list(repo)]

    if not is_dev:
        aliases.append(pygerber.__version__)

        latest_unstable = find_latest_unstable(versions)

        if version > latest_unstable:
            aliases.append("latest")

        latest_stable = find_latest_stable(versions)

        if not is_unstable and version > latest_stable:
            aliases.append("stable")

    else:
        aliases.append("dev")

    print("Aliases:", aliases)  # noqa: T201
    if check_only:
        return

    sys_argv_original = sys.argv.copy()

    sys.argv = ["mike", "deploy", "--push", "--update-aliases", *aliases]
    mike_main()

    sys.argv = sys_argv_original


def find_latest_stable(versions: list[Version]) -> Version:
    return max(filter(lambda v: not (v.is_devrelease or v.is_prerelease), versions))


def find_latest_unstable(versions: list[Version]) -> Version:
    return max(filter(lambda v: (v.is_devrelease or v.is_prerelease), versions))


if __name__ == "__main__":
    main()
