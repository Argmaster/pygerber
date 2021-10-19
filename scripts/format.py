# -*- coding: utf-8 -*-
import subprocess
import sys


def main():
    subprocess.run([sys.executable, "-m", "isort", "."])
    subprocess.run([sys.executable, "-m", "flake8", "."])
    subprocess.run([sys.executable, "-m", "rstfmt", "docs"])
    subprocess.run([sys.executable, "-m", "rstfmt", "README.rst"])
    for folder in ("src", "tests", "examples", "scripts"):
        subprocess.run([sys.executable, "-m", "black", folder])


if __name__ == "__main__":
    main()
