#-*- coding:utf8 -*-

import logging
from logging.config import fileConfig

from const import path_logcfg

fileConfig(path_logcfg)
yh_api_logger = logging.getLogger('yh_api')
