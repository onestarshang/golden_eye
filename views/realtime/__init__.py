#-*- coding: utf8 -*-

from flask import Blueprint, redirect, session
from flask import request as req
from flask.ext.mako import render_template as tpl

from libs.utils import days_ago, get_date_range, DATE_DISPLAY_FORMAT, str2day, get_ifcode
from libs.auth import require_login

realtime_page = Blueprint('realtime', __name__)


@realtime_page.route('/boll')
@require_login
def boll():
    if not req.args.get('date'):
        date = days_ago(0)
        period_short = 50
        period_long = 80
        today = str2day(days_ago(0))
        ifcode = get_ifcode(today)
        return redirect('/dashboard/boll?date=%s&ifcode=%s&period_short=%s&period_long=%s' % (date, ifcode, period_short, period_long))

    date = str2day(req.args.get('date')).strftime(DATE_DISPLAY_FORMAT)
    ifcode = req.args.get('ifcode')
    period_short = int(req.args.get('period_short'))
    period_long = int(req.args.get('period_long'))
    ctx = {'req': req, 'date': date,
           'ifcode': ifcode
          }
    ctx = {'req': req}
    return tpl('/realtime/boll.html', **ctx)
