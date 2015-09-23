#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user_bootstrap.py
# $Date: 2015-09-23 13:48
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from model import *

@api_impl('/user/register', methods=['POST'], preprocessors=dict(email=str,pwd=str))
def register(email, pwd):
    exists = User.objects(email=email)
    if len(exists):
        return {'success':False}
    user = User(email=email)
    user.password = User.encrypted_password(pwd)
    user.save()
    login_user(user)
    return {'success': True}

@api_impl('/user/login', methods=['POST'], preprocessors=dict(email=str,pwd=str))
def login(email, pwd):
    if email is None or pwd is None:
        return {'success': False}
    user = User.get_one(email=email)
    if not user:
        return {'success': False}
    if User.login_user(user, pwd): # Wrong PWD
        login_user(user)
        return {'success': True}
    else:
        return {'success': False}



@api_impl('/user/repeat', methods=['POST'], preprocessors=dict(email=str))
def repeat(email):
    user = User.get_one(email=email)
    if user:
        return {'repeat': True}
    else:
        return {'repeat': False}
    
