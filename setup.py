#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


with open("src/requirements.txt") as file:
    INTALL_REQUIRES = [r.strip() for r in file.readlines()]

setup(
    name="pygerber",
    version="1.0.0",
    license="MIT",
    description="Python package for 2D and 3D rendering of GerberX3 files.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Krzysztof Wiśniewski",
    author_email="argmaster.world@gmail.com",
    url="https://github.com/Argmaster/pygerber",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
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
    ],
    project_urls={
        "Documentation": "https://pygerber.readthedocs.io/",
        "Changelog": "https://pygerber.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/Argmaster/pygerber/issues",
    },
    keywords=[
        "python-3",
        "gerber",
        "gerber-rendering",
        "gerber-x3",
        "python-rendering",
        "gerber-parser",
        "python-3.9",
    ],
    python_requires="==3.9.*",
    install_requires=INTALL_REQUIRES,
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        "console_scripts": [
            "pygerber = pygerber.cli:main",
        ]
    },
)
