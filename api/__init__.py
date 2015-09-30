#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Tue Apr 28 09:01:19 2015 +0800
# $Author: He Zhang <mattzhang9[at]gmail[at]com>

from flask import Response, request, redirect, url_for, jsonify
from gmutil import import_all_modules
from impl.util import api_impl
from impl import *
import re
import copy
import json
from gm import get_app
from functools import wraps
import os
import werkzeug
import json

app = get_app()

# import_all_modules(os.path.join(__file__, 'impl'), __name__, locals())


VALID_CALLBACK_RE = re.compile('^[$A-Za-z_][0-9A-Za-z_$.]*$')


class api_method(object):
    """use as a decorator to register an API"""
    
    all_url_rule = list()
    """class level attribute for all url rules"""
    
    url_rule = None
    """url rule for current API"""
    
    api_implementation = None
    """a callable implementing current API, which takes no argument and
        returns a dict"""
    
    url_rule_extra_kwargs = None
    """extra keyword arguments for url rule"""
    
    API_PREFIX = '/api'
    """all apis prefix with url"""
    
    endpoint = ''
    """endpoint of view_func"""
    
    def __init__(self, url_rule, **kwargs):
        self.url_rule = api_method.API_PREFIX + url_rule
        self.url_rule_extra_kwargs = kwargs
        
        meth = self.url_rule_extra_kwargs.get('methods', None)
        if meth is not None:
            if 'POST' in meth:
                meth.append('OPTIONS')

    def __call__(self, func):
        self.api_implementation = func
        self.endpoint = func.__module__ + '.' + func.__name__
        
        @wraps(func)
        def view_func(**kwargs):
            """the view_func passed to Flask.add_url_rule"""
            try:
                rst = self.api_implementation(**kwargs)
            except werkzeug.exceptions.Unauthorized:
                rst = {u'success': False, u'error': u'Auth error'}
            print 'The return of {} is'.format(request.url)
            print rst
            return jsonify(rst)
        
        app.add_url_rule(self.url_rule,
                         view_func=view_func,
                         endpoint=self.endpoint, **self.url_rule_extra_kwargs)
                         
        return func


def _patch_all_apis():
    """ decorate apis by all saved decorators and api_method """
    
    # use copy of api_list to avoid memory explosion caused
    # recursive `api_impl_deco` calls
    api_list = copy.copy(api_impl.api_list)
    
    for api in api_list:
        func = api.func
        if '_deco_funcs' in func.__dict__:
            deco_funcs = func.__dict__['_deco_funcs']
            if deco_funcs:
                for deco_func in deco_funcs:
                    func = deco_func(func)
        func = api_method(api.url_rule, **api.kwargs)(func)


_patch_all_apis()

# vim: foldmethod=marker
