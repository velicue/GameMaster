#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Sun Jul 20 23:44:02 2014 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import unittest
from faker import Factory
from collections import namedtuple
from functools import wraps

import urllib
import urllib2
import cookielib
import json
import random

from gmconfig import app_config

API_HOST = app_config.HOST
API_PORT = app_config.PORT
PROTOCOL = 'http'


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
        response = self.urlopener.open(url)
        return json.loads(response.read())

    def post(self, url, **kwargs):
        """a POST request to url with data.(post)
        url is a location relative to root, e.g '/add_tab'
        return: json data
        """
#         req = urllib2.Request(
#             self._url(url), urllib.urlencode(kwargs),
#             )
        response = self.urlopener.open(
            self._url(url), urllib.urlencode(kwargs))
        return json.loads(response.read())

    def _url(self, url):
        return self.url_base + url

    def _get_url(self, url, data={}):
        if len(data):
            url = url + '?' + urllib.urlencode(data)
        return self._url(url)


faker = Factory.create()

User = namedtuple(
    'User',
    ('username password password_confirm' +
        ' nickname sex email phone_number categories tags').split())


def fake_user():
    password = 'aaASDFs12sdf'
    return User(
        username=faker.user_name(),
        password=password,
        password_confirm=password,
        nickname=faker.name(),
        sex=random.choice('unknown male female'.split()),
        email=faker.email(),
        phone_number=faker.phone_number(),
        categories=["123123"],
        tags="asdf,asdfe,asdewf")


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
        self.assertIn('success', res)

    def assertError(self, res, error_msg=None):
        if not (error_msg is None):
            self.assertDictContainsSubset(res, dict(error=error_msg))
        else:
            self.assertIn('error', res)

    def login(self, user):
        return self.post(
            '/login',
            user_id=user.username, password=user.password)

    def logout(self):
        return self.get('/logout')

    def register(self, user):
        return self.post('/register', **user.__dict__)


class APITestCaseWithRegisteredUser(APITestCaseBase):
    def setUp(self):
        self.user = fake_user()
        self.register(self.user)
        self.login(self.user)

    def tearDown(self):
        # TODO: should delete the user.
        # wait until user permission model is finished
        self.logout()


class APITestCaseWithPermissions(APITestCaseBase):
    def fakeUserWithPermissions(self, permissions):
        from model.user import User
        self.password = 'aaASDFs12sdf'
        user = User(
            username=faker.user_name()[0:4] + '_test',
            password=User.encrypted_password(self.password),
            nickname=faker.name(),
            phone_number=faker.phone_number())
        user.permissions = permissions
        return user

    def setUp(self):
        if 'permissions' in dir(self):
            self.user = self.fakeUserWithPermissions(self.permissions)
            self.user.save()
            self.user.password = self.password
            self.login(self.user)

    def tearDown(self):
        if 'permissions' in dir(self):
            self.logout()
            self.user.delete()

# vim: foldmethod=marker
