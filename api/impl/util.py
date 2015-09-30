#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Thu Apr 30 15:28:54 2015 +0800
# $Author: He Zhang <mattzhang9[at]gmail[at]com>


"""
@api_impl should be the last decorator.
other decorators please wrap it with @api_impl_deco
"""

from flask import request, redirect, url_for, abort, session, jsonify
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
import flask_login
import copy
import model
from model import *
from gmconfig import *
from gmutil import *
from werkzeug.local import LocalProxy
import inspect
# import dateutil

from gm import get_app
import mongoengine
from mongoengine import Q, Document
from mongoengine import ReferenceField, ListField
from functools import wraps

app = get_app()



class api_impl(object):
    """
        a decorator for all api methods inside `impl' directory.

        Implementation detail:
            This decorator just store functions in a list and do not do actual
            decorating. Function list stored will be used in parent directory
            to generate actual apis

        further more, a raised Exception with type dict

        Arguments passed to api_impl will be passed to
        :py:class:`api.api_method`, which in turns pass to
        :py:meth:`Flask.add_url_rule`, except for the following two:
            - preprocessors:
                An dict of string to function that transforms request strings
                to meaningful data.
            - permission_required:
                Declare user-level permission requirement for this API, e.g,
                category_create, login, etc.
                However, more complicatd permissions should be checked on
                a per-api bases, e.g, whether a user is authorized to edit a
                specific thread.
    """

    url_rule = None
    kwargs = None
    func = None
    preprocessors = None

    api_list = []

    def __init__(
            self, url_rule,
            preprocessors=None,
            **kwargs):
        self.preprocessors = preprocessors
        self.url_rule = url_rule
        self.kwargs = kwargs

    def __call__(self, func):

        @wraps(func)
        def request_preprocess_wrapper(*args, **kwargs):
            """
            apply preprocessors.

            Anonymous checked first, then the user permission.
            The permission is determined by the first True of False in the perm
            Permission from inspect and request.
            """
            ###########################
            #   apply preprocessors   #
            ###########################
            argspec = inspect.getargspec(func)
            if argspec.varargs:  # XXX: Does not support positional args
                raise RuntimeError(
                    'filter_args can not decorate functions' +
                    ' with positional args')

            if argspec.defaults:
                default_args = dict(zip(
                    argspec.args[-len(argspec.defaults):],
                    argspec.defaults))
            else:
                default_args = dict()

            non_default_positional_args = set(argspec.args) - set(default_args)

            # filter params in request
            if request.method == 'POST':
                req = request.json
            elif request.method == 'GET':
                req = request.values
            else:
                print 'The method {} is not supported'.format(request.method)
                return dict(error=u'method {} is not supported'.format(
                    request.method))
            print 'The request of {} is'.format(request.url)
            print req
            for key in req.keys():
                val = req.get(key)
                # if key in non_default_positional_args:
                #     print 'request arg error!'
                #     print set(argspec.args)
                #     print set(default_args)
                #     print non_default_positional_args
                #     return dict(
                #         success=0,
                #         msg=(
                #             u'internal error: keyword \'{}\' should ' +
                #             u'specify a default value').format(key))

                # if function has keyword args, pass all arguments
                if argspec.keywords:
                    kwargs[key] = val
                # else if keys duplicates
                elif key in kwargs:
                    return dict(
                        error=u'interal error: duplicate keyword({})'.format(
                            key))
                elif key in argspec.args:
                    kwargs[key] = val

            # check if all required args present
            nr_defaults = 0
            if argspec.defaults:  # may be None
                nr_defaults = len(argspec.defaults)

            nr_required_args = len(argspec.args) - nr_defaults
            required_args = argspec.args[0:nr_required_args]
            missing_args = []
            for key in required_args:
                if key not in kwargs:
                    missing_args.append(key)

            if len(missing_args):
                return dict(
                    error=u'internal error: args_required',
                    detail=missing_args)

            # preprocess params
            if self.preprocessors:
                for name, preprocessor in self.preprocessors.iteritems():
                    if name in kwargs:
                        try:
                            kwargs.update({name: preprocessor(kwargs[name])})
                        except ValueError as e:
                            return dict(error=u'error preprocessor in PARA: {}'.format(
                                name))

            try:
                ret = func(*args, **kwargs)
            except mongoengine.errors.ValidationError as e:
                print e
                return dict(
                    error='internal erorr: validation_error',
                    detail=str(e))
            return ret

        if self.preprocessors:
            self.func = request_preprocess_wrapper  # filter args
        else:
            self.func = func

        api_impl.api_list.append(self)

        self.populate_doc(func)
        return func

    def populate_doc(self, func):
        doc = ":Route: {}\n".format(self.url_rule)
        if func.__doc__ is None:
            func.__doc__ = ''
        func.__doc__ = doc + func.__doc__


class api_impl_deco(object):
    """
        wraps a decorator and store it in object.__dict__['_deco_funcs']
    """

    deco_func = None

    def __init__(self, deco_func):
        self.deco_func = deco_func

    def __call__(self, func):
        if '_deco_funcs' not in func.__dict__:
            func.__dict__['_deco_funcs'] = []
        func.__dict__['_deco_funcs'].append(self.deco_func)
        return func

    def __name__(self):
        return func.__name__


def patch_api_impl_deco(namespace, function_names):
    """
        patch decorators
    """
    if isinstance(function_names, basestring):
        function_names = [function_names]
    for funcname in function_names:
        func = namespace[funcname]
        func = api_impl_deco(func)
        namespace[funcname] = func


def preDeref(items, depth):
    """
    use deref() to recursively dereference a list of items to a given depth.
    in every step, only one "$in" query on every collection will be executed,
    in this way to cut database query.
    tested under _get_threads but not in other circumstances..
    author:daiwentao
    """
    derefs = deref(items, dict(), depth)
    for i in range(len(items)):
        items[i] = derefs[items[i].id]
    return items


def deref(items, table, depth):
    """
    used by preDeref to dereference a list of items with fewer database query.
    output will be a dict in which key is the id and value is the entities of
    the items.
    """
    if depth <= 0:
        res = dict()
        for i in items:
            res[i.id] = i
        return res

    # find all undereferenced objects in items and divide them according to
    # their type
    unDerefList = dict()
    for item in items:
        unDerefList.setdefault(type(item), []).append(item.id)

    # database query
    for cls in unDerefList:
        for i in cls.objects.filter(id__in=unDerefList[cls]).select_related():
            table[i.id] = i

    # attach the result to the items
    for i in range(len(items)):
        items[i] = table[items[i].id]

    if depth == 1:
        res = dict()
        for i in items:
            res[i.id] = i
        return res

    # construct item list in next depth
    nextItems = list()
    for item in items:
        for k, f in item._fields.iteritems():
            if isinstance(item[k], Document):
                # avoid circle
                if item[k].id not in table:
                    nextItems.append(item[k])
            elif isinstance(f, ListField) and isinstance(
                    f.field, ReferenceField):
                for i in item[k]:
                    if i.id not in table:
                        nextItems.append(i)
    if nextItems != []:
        result = deref(nextItems, table, depth - 1)
        for i in range(len(items)):
            for k, f in items[i]._fields.iteritems():
                if isinstance(items[i][k], Document):
                    items[i][k] = result.get(
                        items[i][k].id, table[items[i][k].id])
                elif isinstance(f, ListField) and isinstance(
                        f.field, ReferenceField):
                    for j in range(len(items[i][k])):
                        items[i][k][j] = result.get(
                            items[i][k][j].id, table[items[i][k][j].id])

    res = dict()
    for i in items:
        res[i.id] = i
    return res


def gen_entity_list_json_by_pagination(
        pagination, item_as_json=True,
        iter_pages_params=dict(), **kwargs):
    """
        generate APIs return list by pagination object.
        kwargs are passed to ``as_json`` method for
        entity object.
    """
    items = preDeref(pagination.items, depth=2)

    if item_as_json:
        data = [i.as_json(**kwargs) for i in items]
    else:
        data = items
    return dict(
        data=data,
        pagination=gen_pagination_json(
            pagination,
            iter_pages_params=iter_pages_params))


def gen_pagination_json(pagination, iter_pages_params=dict()):
    """
        generate pagination json from a pagination object
        for APIs
    """
    return dict(
        page=pagination.page,
        per_page=pagination.per_page,
        pages=[x for x in pagination.iter_pages(**iter_pages_params)],
        has_prev=pagination.has_prev,
        has_next=pagination.has_next)


def Q_or_cond(orig, new):
    if orig is None:
        return new
    elif new is None:
        return orig
    else:
        return orig | new


def Q_and_cond(orig, new):
    if orig is None:
        return new
    elif new is None:
        return orig
    else:
        return orig & new


def filter_category_list(categories):
    """Filter the elements in categories , return None if 'all'.
        Called by _get_threads.
    """
    if not categories:
        return None
    _categories = []
    for cate in categories:
        if isinstance(cate, basestring):
            if cate == 'all':
                return None
        if cate:
            _categories.append(cate)
    return _categories[:NR_SEARCH_CATEGORIES_MAX]


def filter_tag_list(tags):
    """Filter the elements in tags , return None if 'all'.
        Called by _get_threads.
    """
    if not tags:
        return None
    _tags = []
    for tag in tags:
        if isinstance(tag, basestring):
            if tag == 'all':
                return None
        if tag:
            _tags.append(tag)
    return _tags[NR_SEARCH_TAGS_MAX]


def get_wtform_errors(form):
    ret = {}
    for field in form._fields:
        errors = getattr(form, field).errors
        if errors:
            ret[field] = errors
    return ret


def update_document(document, *args, **kwargs):
    """originated from
        http://stackoverflow.com/questions/19002469/
            update-a-mongoengine-document-using-a-python-dict

        :usage:
            either of :
                1. update_document(doc, dict(key=val, good=well))
                2. update_document(doc, key=val, good=well)

        :return:
            keys that are updated
    """

    if len(args) == 1:
        data_dict = args[0]
    else:
        data_dict = kwargs

    from mongoengine import fields

    def field_value(field, value):

        if field.__class__ in (fields.ListField, fields.SortedListField):
            return [
                field_value(field.field, item)
                for item in value
            ]
        if field.__class__ in (
            fields.EmbeddedDocumentField,
            fields.GenericEmbeddedDocumentField,
            fields.ReferenceField,
            fields.GenericReferenceField
        ):
            return value
        else:
            return value

    updated_keys = []
    for key, value in data_dict.items():
        orig = getattr(document, key)
        if value != orig:
            setattr(document, key,
                    field_value(document._fields[key], value)
                    )
            updated_keys.append(key)

    return updated_keys

patch_api_impl_deco(locals(), ['login_required'])


def to_bool(s):
    table = {
        '0': False,
        '1': True,
        'true': True,
        'false': False
    }
    global to_bool

    to_bool = lambda x: table[x]

    return table[x]


def split_by_comma(s):
    if len(s) == 0:
        return []
    return s.split(',')


def get_user(user_or_username):
    from model.user import User
    if isinstance(user_or_username, basestring):
        return User.get_one(username=user_or_username)
    if isinstance(user_or_username, User):
        return user_or_username
    return None


def to_dict(s):
    '''
    convert 'comma splitted colon seperated pair of key and value' to a dict
    example input:
        1:2,a:b
    '''
    dict(tuple(p.split(':')) for p in s.split(','))


def to_list_of_tuple(s):
    return list(tuple(p.split(':')) for p in s.split(','))


def format_list_of_tuple(lst, fmt):
    ret = []
    for tup in lst:
        tup = list(tup)
        for idx, typ in fmt:
            tup[idx] = typ(tup[idx])
        ret.append(tuple(tup))
    return ret


def format_dict(d, key_type=None, value_type=None):
    '''
    convert all keys and values of dict to specified type
    '''
    arr = []
    for key, val in d.iteritems():
        if not (key_type is None):
            key = key_type(key)
        if not (value_type is None):
            val = value_type(val)
        arr.append((key, val))
    return dict(arr)


def convert_dict_key_to_object(klass, d):
    '''
    Illegitimate keys are abandoned and will not raise exception because of
    this. Existing object keys with type klass are preserved.
    '''
    ret = dict()
    objs = klass.objects(id__in=filter(
        lambda x: isinstance(x, basestring), d.keys()))
    for obj in objs:
        ret[obj] = d[str_object_id(obj)]
    for key, val in d.iteritems():
        if isinstance(key, klass):
            ret[obj] = val
    return ret


def clip_value(val, lower, upper):
    return min(upper, max(val, lower))


def ensure_user(user):
    '''
    ensure a user is returned.
    :param user: string or User object

    :return: a User object or None
    '''
    if isinstance(user, basestring):
        return User.get_one(username=user)
    if isinstance(user, User):
        return user
    return None


def ensure_users(users):
    '''
    ensure a list of users is returned.
    :param users: a list of strings and User objects

    :return: a list of User object and None
    '''
    return map(ensure_user, users)


def update_timestamp(doc):
    if not doc.creation_time:
        doc.creation_time = datetime_now_local()
    doc.modification_time = datetime_now_local()

# vim: foldmethod=marker
