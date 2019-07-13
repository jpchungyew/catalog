#!/usr/bin/env python3
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)

from app import models, routes_app, routes_api, login_google