# coding: utf-8
from flask import Flask
from flask.ext.mako import MakoTemplates
from flask.ext.mako import render_template as tpl

from urls import register_urls

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'xxxx'
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['MAKO_DEFAULT_FILTERS'] = ['decode.utf_8', 'h']
app.config['MAKO_TRANSLATE_EXCEPTIONS'] = False
mako = MakoTemplates(app)

register_urls(app)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=13333)
