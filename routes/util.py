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

from flask import send_from_directory, send_file
app = get_app()
@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
    return app.send_static_file(path)
