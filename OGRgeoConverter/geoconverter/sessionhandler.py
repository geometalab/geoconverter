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
    # Sometimes session_key is None. Why ???
    if session_key == None:
        return False
    
    # Rare case. For example if database with sessions is reset while a user is on the website.
    s = SessionStore(session_key=session_key)
    s.save()
    if s.session_key != session_key:
        return False

    return True

# Detect Session end!!!
    # http://stackoverflow.com/questions/4083426/django-detect-session-start-and-end


#from django.contrib.auth import logout
    # Destroy Session:
    #logout(request)
    # oder request.session.flush()