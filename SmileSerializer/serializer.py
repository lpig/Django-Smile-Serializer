# encoding=utf-8
from __future__ import unicode_literals

import six
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
    from django.db.models import ForeignKey
except ImportError:
    raise RuntimeError('django is required in django smail serializer')

from .TimeFactory import TimeFactory


class Serializer(object):
    include_attr = []
    exclude_attr = []
    obj = None
    foreign = False
    use_values = False

    def __init__(self, obj, data_type='raw', datetime_unit='second', datetime_format='timestamp', **kwargs):
        self.obj = obj

        self.data_type = data_type
        self.datetime_unit = datetime_unit
        self.datetime_format = datetime_format
        self.time_func = TimeFactory.get_time_func(datetime_format)

        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

    def check_attr(self, attr):
        if self.exclude_attr and attr in self.exclude_attr:
            return False
        if self.include_attr and attr not in self.include_attr:
            return False
        return True

    def check_foreign_attr(self, attr):
        _include_attr = getattr(self, 'foreign_include_attr', [])
        _exclude_attr = getattr(self, 'foreign_exclude_attr', [])

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

                if isinstance(field, (ImageFieldFile, FileField)):
                    if self.check_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = getattr(data, field.name).url or ""
                elif not isinstance(field, ForeignKey):
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
                if isinstance(field, (ImageFieldFile, FileField)):
                    if self.check_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = getattr(data, field.name).url or ""
                elif not isinstance(field, ForeignKey):
                    if self.check_foreign_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = self._get_field(getattr(data, field.name))
                else:
                    if self.check_foreign_attr(field.name) and self.foreign:
                        obj_dict[field.name] = self.data(getattr(data, field.name))
            return obj_dict

    def _get_field(self, field):

        if isinstance(field, (str, six.string_types, bool, float, int, list, six.integer_types)):
            return field
        elif isinstance(field, dict):
            return field
        elif isinstance(field, (datetime.datetime, datetime.date, datetime.time)):
            return self.time_func(field, self.datetime_unit)
        return None

    def values_data(self, data):
        if not isinstance(data, (QuerySet)):
            raise TypeError('object type must be QuerySet')

    def format(self):
        _data = self.data(self.obj)

        output_choice = {
            'json': json.dumps(_data),
            'raw': _data,
            'dict': _data
        }
        return output_choice.get(self.data_type, _data)

    def values_format(self):
        _data = self.values_data(self.obj.values())

        output_choice = {
            'json': json.dumps(_data),
            'raw': _data,
            'dict': _data
        }
        return output_choice.get(self.data_type, _data)
