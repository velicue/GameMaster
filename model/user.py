#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user.py
# $Date: 2015-09-22 18:29
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from gm import get_app

from passlib.hash import bcrypt, md5_crypt, sha512_crypt
app = get_app()
Sex = enum('unknown', 'male', 'female')

cryptor = bcrypt

class User(db.Document):
    email = db.StringField(
        required=True, unique=True,
        max_length=USERNAME_LEN_MAX,
        min_length=1)

    password = db.StringField(required=True)

    nickname = db.StringField(
        min_length=NICKNAME_LEN_MIN,
        max_length=NICKNAME_LEN_MAX)

    sex = db.IntField(choices=Sex, default=Sex.unknown)
#    phone_number = db.StringField(required=True)
    _authenticated = False  # flask_login use

    meta = {
        'indexes': [
            'email', 'nickname', 
        ],
        'ordering': ['-registration_time']
    }

    def __init__(self, *args, **kwargs):
        self._authenticated = False

        super(User, self).__init__(*args, **kwargs)


    def as_json(self, verbose = 0):
        data = dict(email=self.email,
                    nickname=self.nickname,
                    )
        return data

    @staticmethod
    def encrypted_password(password):
        return cryptor.encrypt(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return cryptor.verify(password, hashed_password)

    @staticmethod
    def login_user(user, password):
        """try login a user with username and password

        :Returns:
          - user instance when succeed.
          - None otherwise.
        """
        if User.verify_password(password, user.password):
            return True
        else:
            return False



    # Flask-Login required methods
    def is_authenticated(self):
        return self._authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
