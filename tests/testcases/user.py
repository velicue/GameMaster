#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user.py
# $Date: 2015-09-22 13:25
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from model.thread import Thread
from model.tile import Tile


class UserTestCase(APITestCaseWithPermissions):

    def testUserInfo(self):
        res = self.get('/user_info')
        self.assertNotError(res)
        self.assertIn('username', res)
        self.assertIn('nickname', res)

    def testUpdateUserInfo(self):
        from model.user import Sex
        res = self.post(
            '/user/{}/update'.format(self.user.username),
            sex=Sex.male, nickname='test_nick', desc='test_desc',
            location='test_loca', reputation='1000')
        self.assertSucceed(res)
        self.assertIn('updated_fields', res)
        self.assertIn('nickname', res['updated_fields'])
        self.assertTrue('reputation' not in res['updated_fields'])

    def testUpdateCategory(self):
        from model.category import Category
        cats = Category.objects()[0:3]
        res = self.post('/user/{}/category_preferences/update'.format(
            self.user.username),
            data=','.join(unicode(c.id)+':'+'-1' for c in cats))
        self.assertSucceed(res)
        cats = Category.objects()[0:4]
        res = self.post('/user/{}/category_preferences/update'.format(
            self.user.username),
            data=','.join(unicode(c.id)+':'+'1' for c in cats))
        self.assertSucceed(res)
        self.assertIn('category_preferences', res)
        for i in res['category_preferences']:
            self.assertIn('preference', i)
            self.assertEqual(1, i['preference'])

    def testAddTag(self):
        tags = 'tag0,tag1'
        res = self.post(
            '/user/{}/tag/add'.format(self.user.username), tags=tags)
        self.assertSucceed(res)
        tags = 'tag0,tag2'
        res = self.post(
            '/user/{}/tag/add'.format(self.user.username), tags=tags)
        self.assertSucceed(res)
        self.assertIn('user', res)
        self.assertIn('tags', res['user'])
        self.assertEqual(3, len(res['user']['tags']))
        tags = ','.join([('tag%d' % i) for i in range(1000)])
        res = self.post(
            '/user/{}/tag/add'.format(self.user.username), tags=tags)
        self.assertError(res)

    def testDeleteTag(self):
        tags = 'tag0,tag1'
        res = self.post(
            '/user/{}/tag/add'.format(self.user.username), tags=tags)
        self.assertSucceed(res)
        tags = 'tag0,tag2'
        res = self.post(
            '/user/{}/tag/delete'.format(self.user.username), tags=tags)
        self.assertSucceed(res)
        self.assertIn('user', res)
        self.assertIn('tags', res['user'])
        self.assertEqual(1, len(res['user']['tags']))

    def testHottestRelation(self):
        # TODO don't understand this api
        pass

    def setUp(self):
        self.permissions = []
        super(UserTestCase, self).setUp()

    def tearDown(self):
        super(UserTestCase, self).tearDown()

# vim: foldmethod=marker
