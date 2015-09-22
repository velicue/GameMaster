#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: 2015-09-22 14:30
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>



from gm import get_app

from model import *
from gmconfig import *
from gmutil import *
from werkzeug.local import LocalProxy
import api
import time
import pytz

app = get_app()
