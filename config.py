#!/usr/bin/env python3

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///catalog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret'
    SEND_FILE_MAX_AGE_DEFAULT = 0