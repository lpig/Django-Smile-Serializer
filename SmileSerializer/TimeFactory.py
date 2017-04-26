# encoding=utf-8
from __future__ import unicode_literals

import arrow

try:
    from django.utils import timezone
except ImportError:
    raise RuntimeError('django is required in django smail serializer')


class TimeFactory(object):
    @classmethod
    def datetime2timestamp(self, dt, datetime_unit='second'):

        ts = arrow.get(dt)
        if dt.tzinfo:
            ts.to(timezone.get_current_timezone())
        ts = int(ts.timestamp)
        if datetime_unit == 'millisecond':
            ts = ts * 1000

        return ts

    @classmethod
    def datetime2str(self, dt):
        ts = arrow.get(dt)
        if dt.tzinfo:
            ts.to(timezone.get_current_timezone())

        return ts.format("YYYY-MM-DD hh:mm:ss")

    @staticmethod
    def get_time_func(datetime_type='timestamp'):
        if datetime_type == 'timestamp':
            return TimeFactory.datetime2timestamp
        elif datetime_type == 'str':
            return TimeFactory.datetime2str
