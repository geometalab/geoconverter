'''
Creates and handles job id's.
A job id generated randomly and is unique.
'''

import datetime
import string
import random
import re
from OGRgeoConverter.models import JobIdentifier
from OGRgeoConverter.geoconverter import datetimehandler

def get_job_id_regex():
    '''
    Returns a regular expression representing a job id.
    Matches strings containing a job id.
    '''
    #         year   month   day   hour  minute  second  code    total: 24 characters
    return r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\w{10})'

def get_bounded_job_id_regex():
    '''
    Returns a regular expression representing a job id.
    Only matches strings being a job id (no characters before and after)
    '''
    return r'^' + get_job_id_regex() + r'$'

def get_new_job_identifier_by_client_job_token(session_key, client_job_token):
    client_job_token = _check_client_job_token(client_job_token)
    job_identifier = JobIdentifier.get_job_identifier_by_client_job_token(session_key, client_job_token)
    if len(job_identifier) == 0:
        new_job_identifier = JobIdentifier()
        new_job_identifier.session_key = session_key
        new_job_identifier.client_job_token = client_job_token
        new_job_identifier.job_id = _get_random_job_id()
        new_job_identifier.creation_time = datetimehandler.get_now()
        new_job_identifier.save()
        return new_job_identifier
    else:
        return None

def get_job_identifier_by_client_job_token(session_key, client_job_token):
    client_job_token = _check_client_job_token(client_job_token)
    job_identifier = JobIdentifier.get_job_identifier_by_client_job_token(session_key, client_job_token)
    if len(job_identifier) == 1:
        return job_identifier[0]
    else:
        return None
    
def get_job_identifier_by_job_id(session_key, job_id):
    job_identifier = JobIdentifier.get_job_identifier_by_job_id(session_key, job_id)
    if len(job_identifier) == 1:
        return job_identifier[0]
    else:
        return None

def _check_client_job_token(client_job_token):
    '''
    Makes sure a token received by a client is a string and not too long
    '''
    validated_client_job_token = str(client_job_token)
    max_length = JobIdentifier._meta.get_field('client_job_token').max_length
    if len(validated_client_job_token) > max_length:
        validated_client_job_token = validated_client_job_token[0:max_length]
    return validated_client_job_token

def _get_random_job_id():
    '''
    Generates a random job id containing the current date and a random string
    '''
    return __get_date_string() + __get_random_code()

def __get_date_string():
    now = datetime.datetime.now()
    
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second = now.strftime('%S')
    
    # e.g. 20121212151500
    return year + month + day + hour + minute + second

def __get_random_code():
    length = 10
    characters=string.ascii_lowercase + string.digits
    
    # e.g. 3a9rtf3ifw
    return ''.join(random.choice(characters) for i in range(length))

def is_valid_job_id(code):
    return re.match(get_bounded_job_id_regex(), code) != None

def split_job_id(job_id):
    '''
    Splits a job id and returns its components (year, month, ...) as a list
    If the argument is not a valid job id an empty list is returned.
    '''
    if is_valid_job_id(job_id):
        splitted_job_id = re.split(get_bounded_job_id_regex(), job_id)
        # First and last string in list is empty (see Python doc for re.split)
        return splitted_job_id[1:len(splitted_job_id)-1]
    else:
        return []

def join_job_id(*args):
    '''
    Joins a list (containing year, month, ...) to a job id.
    If the joined string is not a valid job id an empty string is returned
    '''
    joined_job_id = ''.join(args)

    if is_valid_job_id(joined_job_id):
        return joined_job_id
    else:
        return ''