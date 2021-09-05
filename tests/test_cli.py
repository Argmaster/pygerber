# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main
from pygerber.cli import get_argument_parser


class TestCLI(TestCase):

    def test_parser(self):
        parser = get_argument_parser()


if __name__ == '__main__':
    main()