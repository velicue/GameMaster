#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Sun Jul 20 23:44:02 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import unittest
from faker import Factory
from functools import wraps

import urllib
import urllib2
import cookielib
import json
import random
import requests 


from gmconfig import app_config

API_HOST = app_config.HOST
API_PORT = app_config.PORT
PROTOCOL = 'http'

req = requests.session()

class APIInterface(object):
    """
    provide get and thread method for APIs with cookie support
    """

    api_url_prefix = '/api'
    url_base = "{}://{}:{}{}" . format(
        PROTOCOL, API_HOST, API_PORT,
        api_url_prefix)

    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(
        cookielib.CookieJar()))

    def clear_cookie(self):
        """ clear saved cookie """
        self.urlopener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

    def get(self, url, **kwargs):
        """a GET request to url with data.
        url is a location relative to root, e.g '/sample'
        return: json data"""
        url = self._get_url(url, kwargs)
        response = req.get(url)
        print response.cookies
        return response.json()
#        response = self.urlopener.open(url)
#        return json.loads(response.read())

    def post(self, url, **kwargs):
        """a POST request to url with data.(post)
        url is a location relative to root, e.g '/add_tab'
        return: json data
        """
        headers = {'content-type': 'application/json'}
        response = req.post(self._url(url), data=json.dumps(kwargs), headers=headers)
        return response.json()

    def _url(self, url):
        return self.url_base + url

    def _get_url(self, url, data={}):
        if len(data):
            url = url + '?' + urllib.urlencode(data)
        return self._url(url)


def deep_print(obj, indent=4, depth=0):
    def ip(obj):  # indent print
        print ' ' * indent, obj

    if type(obj) == list:
        ip('[')
        for i in obj:
            deep_print(i, indent, depth+1)
        ip(']')
    elif type(obj) == dict:
        for key, val in obj.iteritems():
            ip('{')
            ip("{}: ".format(key))
            deep_print(val, indent, depth+1)
            ip('}')
    else:
        print obj


class APITestCaseBase(unittest.TestCase, APIInterface):

    def assertNotError(self, res):
        try:
            self.assertNotIn('error', res)
        except Exception as e:
            deep_print(res)
            raise e

    def assertSucceed(self, res):
        self.assertTrue(res['success'])

    def assertError(self, res):
        self.assertFalse(res['success'])

    def login(self, user):
        return self.post(
            '/user/login',
            email=user.email, pwd=user.password)

    def logout(self):
        return self.get('/user/logout')

    def register(self, user):
        return self.post('/user/register', 
            email=user.email, pwd=user.password)


