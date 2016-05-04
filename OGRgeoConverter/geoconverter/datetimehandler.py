'''
Functions concering dates and time.
'''

import datetime
from django.utils.timezone import utc


def get_default_datetime():
    return datetime.datetime.fromtimestamp(0).replace(tzinfo=utc)


def get_now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)
