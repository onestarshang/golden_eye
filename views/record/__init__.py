# -*- coding: utf8 -*-

from flask import Blueprint, redirect, session
from flask import request as req
from flask.ext.mako import render_template as tpl
from libs.utils import days_ago, get_date_range, DATE_DISPLAY_FORMAT, str2day, get_ifcode
from libs.auth import require_login

record_page = Blueprint('record', __name__)

@record_page.route('/virtual')
@require_login
def virtual():
    ctx = {'req': req}
    return tpl('/record/virtual.html', **ctx)

