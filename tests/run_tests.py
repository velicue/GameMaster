#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: run_tests.py
# $Date: Tue Feb 25 02:40:19 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>


from importlib import import_module
from pkgutil import walk_packages
import os
import sys
import random
import unittest
import argparse

from testcases import *


def get_args():
    parser = argparse.ArgumentParser(
        description='Run unittest')
    parser.add_argument(
        '-f', '--fake-db', action='store_true',
        help='fake db before running test')
    parser.add_argument(
        '-s', '--seed', default=None,
        help='random seed to use when fake db')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.fake_db:
        if args.seed:
            random.seed(args.seed)
        fake_db()

    prog = unittest.main(verbosity=2, argv=[sys.argv[0]], exit=False)
    #if not prog.result.wasSuccessful():

# vim: foldmethod=marker
