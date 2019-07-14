#!/usr/bin/env python3

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///catalog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'client_secret.json'
    SEND_FILE_MAX_AGE_DEFAULT = 0