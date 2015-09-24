#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: index.py
# $Date: 2015-09-22 14:23
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from flask.ext.login import login_required
@app.route('/')
def example():
    return app.send_static_file('index.html')
    #return render_template('index.html')

@app.route('/ttt')
@login_required
def JS():
    return 'ttt'

#@app.route('/css/<string:c>')
#def CSS(c):
#    #return render_template('css/' + c)
#    return app.send_static_file('css/'+c)
#    #return send_from_directory('css', c)

#@app.route('/assets/<string:c>')
#def ASSETS(c):
#    return app.send_static_file('assets/'+c)
    #return render_template('assets/' + c)

