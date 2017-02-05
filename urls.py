# -*- coding: utf-8 -*-

from views import index_page, login_page
from views.backtest import backtest_page
from views.api import api_index_page
from views.api.backtest import api_backtest_index_page
from views.realtime import realtime_page
from views.api.realtime import api_realtime_index_page
from views.record import record_page


def register_urls(app):
    app.register_blueprint(index_page, url_prefix='/')
    app.register_blueprint(login_page, url_prefix='/index')
    app.register_blueprint(backtest_page, url_prefix='/backtest')
    app.register_blueprint(api_index_page, url_prefix='/api')
    app.register_blueprint(api_backtest_index_page, url_prefix='/api/backtest')
    app.register_blueprint(realtime_page, url_prefix='/dashboard')
    app.register_blueprint(api_realtime_index_page, url_prefix='/api/realtime')
    app.register_blueprint(record_page, url_prefix='/record')
