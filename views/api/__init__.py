# -*-: coding: utf8 -*-

from flask import Blueprint, redirect
from flask import request as req
from flask.ext.mako import render_template as tpl

from libs.utils import jsonize

api_index_page = Blueprint('api', __name__)

@api_index_page.route('/')
@jsonize
def index():
    return {'error': 'api index'}
