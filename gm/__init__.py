#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Jul 04 14:58:30 2015 +0800
# $Author: He Zhang <mattzhang9[at]gmail[dot]com>

"""
    GM website entrance
"""


_app = None
_db = None

def get_app():
    """load modules and return WSGI application"""
    
    import os
    from flask import Flask
    from flask_login import LoginManager
    import sys
   # from common import *
    from gmconfig import app_config
    global get_app, _app
    
    _app = Flask(__name__)
    
    get_app = lambda: _app  # avoid duplicate import
    
    _app.config.from_object(app_config)
    
    _app.secret_key = "hokey dokey, here's the key"
    
    login_manager = LoginManager()
    login_manager.init_app(_app)
    
    @login_manager.user_loader
    def load_user(username):
        from model.user import User
        user = User.get_one(username=username)
        user._authenticated = True
        return user
    
    return _app


def get_db():
    """
        Use getapp() getdb() to avoid duplicate import.
        """
    
    from flask.ext.mongoengine import MongoEngine
    
    global _db, get_db
    _db = MongoEngine(get_app())
    get_db = lambda: _db
    return _db

get_db()  # this must be called last
