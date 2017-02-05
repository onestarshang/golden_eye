# -*-: coding: utf8 -*-

from flask import Blueprint, redirect
from flask import request as req
from flask.ext.mako import render_template as tpl

from libs.utils import jsonize
from libs.utils import DATE_DISPLAY_FORMAT, str2day

from models.api.realtime.calculator import BollCalculator

api_realtime_index_page=Blueprint('api_realtime', __name__)


@api_realtime_index_page.route('/')
@jsonize
def index():
    return {'info': 'realtime'}


@api_realtime_index_page.route('/boll/date/<date>/ifcode/<ifcode>/period_short/<period_short>/period_long/<period_long>')
@jsonize
def boll(date, ifcode, period_short, period_long):
    if not date or not ifcode or not period_short or not period_long:
        return {'error': u'params is fault'}
    date = str2day(date, DATE_DISPLAY_FORMAT)
    period_short = int(period_short)
    period_long = int(period_long)
    return BollCalculator.boll_chart(date, ifcode, period_short, period_long)
