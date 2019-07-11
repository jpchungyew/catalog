from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session as login_session, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

import random, string, requests, httplib2, json

app = Flask(__name__)
app.secret_key = 'super_secret_key'

#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)