# -*-: coding: utf8 -*-

from flask import Blueprint, redirect
from flask import request as req
from flask.ext.mako import render_template as tpl

from libs.utils import jsonize
from libs.utils import DATE_DISPLAY_FORMAT, str2day, ifcode_day_map
from libs.auth import require_login

from models.api.backtest.tables import BacktestData
from models.api.backtest.calculator import FittingDataCalculator
from models.api.backtest.analysis import DataAnalyzer


api_backtest_index_page=Blueprint('api_backtest', __name__)

@api_backtest_index_page.route('/')
@require_login
@jsonize
def index():
    return {'info': 'backtest'}


@api_backtest_index_page.route('/raw_data/date/<date>/ifcode/<ifcode>')
@require_login
@jsonize
def raw_data(date, ifcode):
    if not date or not ifcode:
        return {'error': u'params is fault'}
    date = str2day(date, DATE_DISPLAY_FORMAT).strftime(DATE_DISPLAY_FORMAT)
    return FittingDataCalculator.raw_series(date, ifcode)


@api_backtest_index_page.route('/fitting_data')
@require_login
@jsonize
def fitting_data():
    if not req.args.get('date') or not req.args.get('ifcode') or not req.args.get('period'):
        return {'error': u'params is fault'}
    date = str2day(req.args.get('date')).strftime(DATE_DISPLAY_FORMAT)
    ifcode = req.args.get('ifcode')
    period = int(req.args.get('period'))
    return FittingDataCalculator.fitting_series(period, date, ifcode)


@api_backtest_index_page.route('/ema/date/<date>/ifcode/<ifcode>/period_short/<period_short>/period_long/<period_long>')
@require_login
@jsonize
def ema(date, ifcode, period_short, period_long):
    if not date or not ifcode or not period_short or not period_long:
        return {'error': u'params is fault'}
    date = str2day(date, DATE_DISPLAY_FORMAT).strftime(DATE_DISPLAY_FORMAT)
    period_short = int(period_short)
    period_long = int(period_long)
    return FittingDataCalculator.ema_chart(date, ifcode, period_short, period_long)


@api_backtest_index_page.route('/ema/save2db/<date>/<ifcode>/<period_short>/<period_long>')
@require_login
@jsonize
def ema_save2db(date, ifcode, period_short, period_long):
    if not date or not ifcode or not period_short or not period_long:
        return {'error': u'params is fault'}
    period_short = int(period_short)
    period_long = int(period_long)
    return FittingDataCalculator.ema_df(date, ifcode, period_short, period_long)


@api_backtest_index_page.route('/macd/date/<date>/ifcode/<ifcode>/period_short/<period_short>/period_long/<period_long>')
@require_login
@jsonize
def macd(date, ifcode, period_short, period_long):
    if not date or not ifcode or not period_short or not period_long:
        return {'error': u'params is fault'}
    date = str2day(date, DATE_DISPLAY_FORMAT).strftime(DATE_DISPLAY_FORMAT)
    period_short = int(period_short)
    period_long = int(period_long)
    return DataAnalyzer.macd_chart(date, ifcode, period_short, period_long)


@api_backtest_index_page.route('/dates/ifcode/<ifcode>/display_num/<display_num>')
@require_login
@jsonize
def dates_by_ifcode(ifcode, display_num):
    if not ifcode:
        return {'error': u'params is fault'}
    date_list = ifcode_day_map(ifcode)
    if len(date_list) > int(display_num):
        date_list = date_list[:int(display_num)]
    return {'date_list': date_list}
