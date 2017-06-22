# -*- coding: UTF-8 -*-
"""
"""
from BouncePass import *
from ParseTables import mastertable

__package__ = "bouncepass"
__title__ = "bouncepass"
__license__ = "GPLv3"
__author__ = "Dana Drevecky"
__copyright__ = "Copyright 2017 Dana Drevecky"

run = Scorer()

while 1:
    print isinstance(run, Scorer)
    print isinstance(run.homescore, run.CasparData)
