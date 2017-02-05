#-*- coding: utf8 -*-

from functools import wraps
from flask import redirect


def require_login(func):
    @wraps(func)
    def _(*args, **kwargs):
        session = func.func_globals.get('session', None)
        req = func.func_globals.get('req', None)
        if req:
            if 'userid' not in session:
                return redirect('/index/login')
            else:
                req.userid = session['userid']
                func.func_globals['req'] = req
        return func(*args, **kwargs)
    return _
