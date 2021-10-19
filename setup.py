#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


def fetch_long_description():
    readme_text = re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
        "", fetch_utf8_content("README.rst")
    )
    changelog_text = re.sub(
        ":[a-z]+:`~?(.*?)`", r"``\1``", fetch_utf8_content("CHANGELOG.rst")
    )
    return "%s\n%s" % (readme_text, changelog_text)


def fetch_utf8_content(file_path: str):
    with open(file_path, encoding="utf-8") as file:
        content = file.read()
    return content


def fetch_requirements(file_path: str):
    with open(file_path) as file:
        return [r.strip() for r in file.readlines()]


NAME = "pygerber"
VERSION = "1.0.0"
LICENSE_NAME = "MIT"
SHORT_DESCRIPTION = "Package for testing various development tools."
LONG_DESCRIPTION = fetch_long_description()
INSTALL_REQUIRES = fetch_requirements("src/requirements.txt")
AUTHOR = "Krzysztof Wiśniewski"
AUTHOR_EMAIL = "argmaster.world@gmail.com"
URL = "https://github.com/Argmaster/pygerber"
PACKAGES = find_packages(where="src")
PACKAGE_DIR = {"": "src"}
PACKAGE_PYTHON_MODULES = [splitext(basename(path))[0] for path in glob("src/*.py")]
INCLUDE_PACKAGE_DATA = True
ZIP_SAFE = False
CLASSIFIERS = [
    # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Multimedia :: Graphics :: 3D Rendering",
    "Topic :: Text Processing :: General",
    "Topic :: Utilities",
]
PROJECT_URLS = {
    "Documentation": "https://pygerber.readthedocs.io/",
    "Changelog": "https://pygerber.readthedocs.io/en/latest/changelog.html",
    "Issue Tracker": "https://github.com/Argmaster/pygerber/issues",
}
KEYWORDS = [
    "python-3",
    "python-3.9",
    "gerber",
    "gerber-rendering",
    "gerber-x3",
    "python-rendering",
    "gerber-parser",
]
EXTRAS_REQUIRE = {
    # eg:
    #   'rst': ['docutils>=0.11'],
    #   ':python_version=="2.6"': ['argparse'],
}
ENTRY_POINTS = {
    "console_scripts": [
        "pygerber = pygerber.cli:main",
    ]
}
PYTHON_REQUIREMENTS = "==3.9.*"


def run_setup_script():
    setup(
        name=NAME,
        version=VERSION,
        license=LICENSE_NAME,
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=PACKAGES,
        package_dir=PACKAGE_DIR,
        py_modules=PACKAGE_PYTHON_MODULES,
        include_package_data=INCLUDE_PACKAGE_DATA,
        zip_safe=ZIP_SAFE,
        classifiers=CLASSIFIERS,
        project_urls=PROJECT_URLS,
        keywords=KEYWORDS,
        python_requires=PYTHON_REQUIREMENTS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
    )


if __name__ == "__main__":
    run_setup_script()
