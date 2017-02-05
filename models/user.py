# -*- coding: utf8 -*-

from consts import USERS


class User(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def get(cls, userid):
        return USERS.get(userid)
