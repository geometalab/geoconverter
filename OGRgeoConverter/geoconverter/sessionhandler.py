'''
Function to load a session created by Django
'''

from django.contrib.sessions.backends.db import SessionStore


def get_session(session_key):
    '''
    Loads and returns a session form the SessionStore based on the session key
    '''
    return SessionStore(session_key=session_key)


def is_valid_key(session_key):
    '''
    Detects if a session key is valid or not. If not the caller of this function can create a new one by calling session.flush().
    '''
    # Sometimes session_key is None when the Django website is called. Not
    # clear why.
    if session_key is None:
        return False

    # Rare case. For example if the database storing the sessions is reset
    # while a user is on the website.
    s = SessionStore(session_key=session_key)
    s.save()
    if s.session_key != session_key:
        return False

    return True


# How to detect Session end? -> Cleanup of Session database

#from django.contrib.auth import logout
# Destroy Session:
# logout(request)
# or request.session.flush()
