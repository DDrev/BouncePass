# -*- coding: UTF-8 -*-
"""
"""
from BouncePass import *
from ParseTables import mastertable
import atexit

__package__ = "bouncepass"
__title__ = "bouncepass"
__license__ = "GPLv3"
__author__ = "Dana Drevecky"
__copyright__ = "Copyright 2017 Dana Drevecky"

run = Scorer()
atexit.register(run.exit_close_serial())
