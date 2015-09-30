#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user.py
# $Date: 2015-09-22 13:25
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from model import User


class UserBootstrapTestCase(APITestCaseBase):

    def testBootstrap(self):
        email = 'ttt@cornell.edu'
        pwd = 'test'
        self.user = User(email=email, password=pwd)
        res = self.register(self.user)
        self.assertSucceed(res)
        res = self.register(self.user)
        self.assertError(res)
        res = self.post('/user/repeat', email=email)
        self.assertTrue(res['repeat'])
        res = self.login(self.user)
        self.assertSucceed(res)
        res = self.logout()
        self.assertSucceed(res)

    def tearDown(self):
        user = User.get_one(email=self.user.email)
        if user is not None:
            user.delete()

# vim: foldmethod=marker
