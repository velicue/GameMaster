#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: permdef.py
# $Date: 2015-09-22 13:25
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

_PERMISSION_DEFINITION = {
    'manage_user': {
        'add_user': [],
        'update_user': ['profile', 'permission'],
        'delete_user': [],
    },
}
"""
    A JSON like permission tree
    User should only change this
"""

# vim: foldmethod=marker
