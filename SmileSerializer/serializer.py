# encoding=utf-8
from __future__ import unicode_literals

import datetime

try:
    import simplejson as json
except ImportError:
    import json

try:
    from django.db import models
    from django.core.paginator import Page
    from django.db.models.query import QuerySet
    from django.db.models.fields.files import ImageFieldFile, FileField
except ImportError:
    raise RuntimeError('django is required in django smail serializer')

from .TimeFactory import TimeFactory


class Serializer(object):
    include_attr = []
    exclude_attr = []
    obj = None
    foreign = False

    def __init__(self, obj, data_type='raw', datetime_unit='second', datetime_format='timestamp', **kwargs):
        self.obj = obj

        self.data_type = data_type
        self.datetime_unit = datetime_unit
        self.datetime_format = datetime_format
        self.time_func = TimeFactory.get_time_func(datetime_format)

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def check_attr(self, attr):
        if self.exclude_attr and attr in self.exclude_attr:
            return False
        if self.include_attr and attr not in self.include_attr:
            return False
        return True

    def check_foreign_attr(self, attr):
        _exclude_attr = getattr(self, 'foreign_exclude_attr', [])
        _include_attr = getattr(self, 'foreign_include_attr', [])

        if _exclude_attr and attr in _exclude_attr:
            return False
        if _include_attr and attr not in _include_attr:
            return False
        return True

    def data(self, data, extra=None):
        if isinstance(data, (QuerySet, Page, list)):
            convert_data = []
            for d in data:
                convert_data.append(self.data(d))

            return convert_data

        elif isinstance(data, models.Model):
            obj_dict = {}

            concrete_model = data._meta.concrete_model
            for field in concrete_model._meta.local_fields:
                if field.rel is None:
                    if self.check_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = self._get_field(getattr(data, field.name))
                else:
                    if self.check_attr(field.name) and self.foreign:
                        obj_dict[field.name] = self.foreign_data(getattr(data, field.name))

            return obj_dict

    def foreign_data(self, data):
        if isinstance(data, models.Model):
            obj_dict = {}

            concrete_model = data._meta.concrete_model
            for field in concrete_model._meta.local_fields:
                if field.rel is None:
                    if self.check_foreign_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = self._get_field(getattr(data, field.name))
                else:
                    if self.check_foreign_attr(field.name) and self.foreign:
                        obj_dict[field.name] = self.data(getattr(data, field.name))

            return obj_dict

    def _get_field(self, field):

        if isinstance(field, (str, unicode, bool, float, int, list, long)):
            return field
        elif isinstance(field, dict):
            return field
        elif isinstance(field, (datetime.datetime, datetime.date, datetime.time)):
            return self.time_func(field, self.datetime_unit)
        elif isinstance(field, (ImageFieldFile, FileField)):
            return field.url or ""

        return None

    def format(self):
        _data = self.data(self.obj)

        output_choice = {
            'json': json.dumps(_data),
            'raw': _data,
            'dict': _data
        }
        return output_choice.get(self.data_type, _data)