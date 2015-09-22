#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: gmconfig.py
# $Date: 2015-09-22 13:22
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>
"""global config for website"""

from collections import namedtuple
from pytz import timezone

#################################
#     non-technical settings    #
#################################

TIMEZONE = timezone('US/Eastern')


USERNAME_LEN_MIN = 3
USERNAME_LEN_MAX = 23
USERNAME_REGEX_STR = r'^[a-z][a-z0-9-_\.]*$'
USERNAME_REGEX_INVALID_MESSAGE = (
    u"用户名必须以小写字母开头，且只包含小写字母、数字和'_', '.', '-'")

USERNAME_REGEX_STR_OAUTH = r'^_douban'
USERNAME_REGEX_STR_DB = \
    '({})|({})'.format(USERNAME_REGEX_STR, USERNAME_REGEX_STR_OAUTH)

PASSWORD_LEN_MIN = 8
PASSWORD_LEN_MAX = 23

NICKNAME_LEN_MIN = 2
NICKNAME_LEN_MAX = 50

EMAIL_LEN_MIN = 5
EMAIL_LEN_MAX = 100

NR_TAGS_PER_USER_MAX = 10

PHONE_NUMBER_LEN_MAX = 20

THREAD_TITLE_LEN_MAX = 100
THREAD_CONTENT_LEN_MAX = 100000

QUESTION_LEN_MIN = 1
QUESTION_LEN_MAX = 100000

ANSWER_LEN_MIN = 1
ANSWER_LEN_MAX = 100000

THREAD_CHAT_MESSAGE_LEN_MIN = 1
THREAD_CHAT_MESSAGE_LEN_MAX = 100000

CATEGORY_ABBR_LEN_MIN = 1
CATEGORY_ABBR_LEN_MAX = 30
CATEGORY_ABBR_REGEX_STR = r'^[a-z0-9_\.]*$'
CATEGORY_ABBR_REGEX_INVALID_MESSAGE = u'分类缩写只能由小写字母和数字构成'

CATEGORY_NAME_LEN_MIN = 1
CATEGORY_NAME_LEN_MAX = 30

CATEGORY_DESC_LEN_MAX = 100000

TAG_LEN_MAX = 20
NR_TAGS_PER_THREAD_MAX = 10

COMMENT_CONTENT_LEN_MIN = 1
COMMENT_CONTENT_LEN_MAX = 100000

MESSAGE_CONTENT_LEN_MAX = 200

USER_DESC_LEN_MAX = 1024

FREQUENT_LOCATION_LEN_MAX = 200

NR_SEARCH_CATEGORIES_MAX = 20
NR_SEARCH_TAGS_MAX = 5

USER_INFO_UPDATE_WHITE_LIST = (
    "sex nickname desc "
    "location birthday tags").split()

class _DefaultConfig(object):
    HOST = '0.0.0.0'
    PORT = 54321
    
    OPTIONS = {'debug': True}
    
    MONGODB_SETTINGS = {
        'DB': 'coffee',
        'HOST': 'localhost',
        'PORT': 27017,
}

app_config = _DefaultConfig()

# vim: foldmethod=marker
