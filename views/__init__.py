# -*- coding: utf8 -*-

import simplejson
import hashlib

from flask import Blueprint, redirect, session, jsonify
from flask import request as req
from flask.ext.mako import render_template as tpl

from models.user import User
from models.consts import USERS
from libs.auth import require_login
from libs.utils import days_ago

index_page = Blueprint('index', __name__)
login_page = Blueprint('login', __name__)

@index_page.route('/')
@require_login
def index():
    return redirect('/backtest/ema')


@login_page.route('/login', methods=['POST', 'GET'])
def login():
    if req.method == 'POST':
        success = validate_params(req)
        if success:
            return jsonify(**{'redirect': '/'})
        return jsonify(**{'error': '用户名或密码错误'})
    else:
        salt = get_salt()
        ctx = {'req': req, 'salt': salt}
        return tpl('/login.html', **ctx)


def get_salt():
    salt = days_ago(0) + 'hand.of.midas.salt'
    m = hashlib.md5()
    m.update(salt)
    salt = m.hexdigest()[:6]
    return salt


def validate_params(req):
    hom_user = req.form.get('username')
    password = req.form.get('password')
    user_entry = User.get(hom_user)
    if hom_user in USERS.keys():
        salt = get_salt()
        m = hashlib.md5()
        m.update(user_entry[1] + salt)
        de_user_pass = m.hexdigest()
        if password == de_user_pass:
            session['userid'] = user_entry[0]
            return True
    return False


@login_page.route('/logout')
@require_login
def logout():
    del session['userid']
    return redirect('/index/login')
