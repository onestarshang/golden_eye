# -*- coding: utf8 -*-

from flask import Blueprint, redirect, session
from flask import request as req
from flask.ext.mako import render_template as tpl

from libs.utils import (days_ago, get_date_range,
                        DATE_DISPLAY_FORMAT, str2day,
                        get_ifcode, get_week_day, day2str,
                        ifcode_day_map)
from libs.auth import require_login
from models.api.backtest.analysis import DataAnalyzer

backtest_page = Blueprint('backtest', __name__)


@backtest_page.route('/ema')
@require_login
def ema():
    if not req.args.get('date'):
        date = day2str(get_week_day(str2day(days_ago(1))))
        period_short = 480
        period_long = 1400
        today = str2day(days_ago(0))
        ifcode = get_ifcode(today)
        return redirect('/backtest/ema?date=%s&ifcode=%s&period_short=%s&period_long=%s' % (date, ifcode, period_short, period_long))


    _date = str2day(req.args.get('date'))
    ifcode = req.args.get('ifcode')
    date = _date.strftime(DATE_DISPLAY_FORMAT)
    if _date.weekday() in [5, 6]:
        ctx = {'req': req, 'date': date,
               'ifcode': ifcode,
               'profit_infos': [],
               'profit_all': 0
               }
        return tpl('/backtest/ema.html', **ctx)

    period_short = int(req.args.get('period_short'))
    period_long = int(req.args.get('period_long'))
    profit_infos = DataAnalyzer.ema(date, ifcode, period_short, period_long)
    profit_all = 0
    for item in profit_infos:
        if item['gain'] != '-':
            profit_all += int(item['gain'])
    ctx = {'req': req, 'date': date,
           'ifcode': ifcode,
           'profit_infos': profit_infos,
           'profit_all': profit_all
          }
    return tpl('/backtest/ema.html', **ctx)


@backtest_page.route('/macd')
@require_login
def macd():
    if not req.args.get('date'):
        date = day2str(get_week_day(str2day(days_ago(1))))
        period_short = 12
        period_long = 26
        today = str2day(days_ago(0))
        ifcode = get_ifcode(today)
        return redirect('/backtest/macd?date=%s&ifcode=%s&period_short=%s&period_long=%s' % (date, ifcode, period_short, period_long))

    _date = str2day(req.args.get('date'))
    ifcode = req.args.get('ifcode')
    date = _date.strftime(DATE_DISPLAY_FORMAT)
    if _date.weekday() in [5, 6]:
        ctx = {'req': req, 'date': date,
               'ifcode': ifcode,
               'profit_infos': [],
               'profit_all': 0
               }
        return tpl('/backtest/macd.html', **ctx)

    period_short = int(req.args.get('period_short'))
    period_long = int(req.args.get('period_long'))
    profit_infos = DataAnalyzer.macd(date, ifcode, period_short, period_long)
    profit_all = 0
    for item in profit_infos:
        if item['gain'] != '-':
            profit_all += int(item['gain'])
    ctx = {'req': req, 'date': date,
           'ifcode': ifcode,
           'profit_infos': profit_infos,
           'profit_all': profit_all
          }
    return tpl('/backtest/macd.html', **ctx)


@backtest_page.route('/boll')
@require_login
def boll():
    ctx = {'req': req}
    return tpl('/backtest/boll.html', **ctx)


@backtest_page.route('/report/ema')
@require_login
def ema_report():
    if not req.args.get('ifcode'):
        ifcode = get_ifcode(str2day(days_ago(0)))
        display_num = 10
        return redirect('/backtest/report/ema?ifcode=%s&display_num=%s' % (ifcode, display_num))

    ctx = {'req': req}
    return tpl('/backtest/ema_report.html', **ctx)


@backtest_page.route('/report/macd')
@require_login
def macd_report():
    if not req.args.get('ifcode'):
        ifcode = get_ifcode(str2day(days_ago(0)))
        display_num = 6
        period_short = 12
        period_long = 26
        trans_amount = 1
        return redirect('/backtest/report/macd?ifcode=%s&period_short=%s&period_long=%s&display_num=%s&trans_amount=%s' % \
                (ifcode, period_short, period_long, display_num, trans_amount))

    display_num = int(req.args.get('display_num'))
    ifcode = req.args.get('ifcode')
    period_short = int(req.args.get('period_short'))
    period_long = int(req.args.get('period_long'))
    trans_amount = int(req.args.get('trans_amount'))
    date_list = ifcode_day_map(ifcode)

    if len(date_list) > int(display_num):
        date_list = date_list[:int(display_num)]

    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    trans_total_num = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        profit_infos = DataAnalyzer.macd(day, ifcode, period_short, period_long)
        profit_all = 0
        trans_num = (len(profit_infos) - 1) / 2
        trans_total_num += trans_num
        for item in profit_infos:
            if item['gain'] != '-':
                profit_all += int(item['gain']) * trans_amount
        rs.append({'date': day, 'profit': profit_all, 'trans_num': trans_num})
        total += profit_all
        if profit_all >= 0:
            pos_num += 1
        elif profit_all < 0 :
            nag_num += 1

    if nag_num == 0:
        profit_rate = pos_num
    else:
        profit_rate = pos_num*1.0/nag_num
    fees = trans_total_num * 2300
    real_profit = total - fees
    ctx = {'req': req, 'total': total,
           'profit_rate': profit_rate,
           'trans_total_num': trans_total_num, 'fees': fees,
           'real_profit': real_profit,
           'detail': rs, 'trans_amount': trans_amount}
    return tpl('/backtest/macd_report.html', **ctx)
