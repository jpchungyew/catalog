#!/usr/bin/env python3
from sqlalchemy import create_engine
from config import Config
from sqlalchemy.orm import sessionmaker
from catalogapp import app, db 
from flask import jsonify
from catalogapp.models import User, Category, Item

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)

# Catalog JSON APIs
@app.route('/catalog/JSON')
def catalogJSON():
    session = Session()

    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/<string:category_name>/JSON')
@app.route('/catalog/<string:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    session = Session()

    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()

    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    session = Session()

    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(
        category_id=category.id,
        name=item_name).one()

    return jsonify(item=item.serialize)

@app.route('/catalog/users/JSON')
def usersJSON():
    session = Session()

    users = session.query(User).all()
    return jsonify(users=[u.serialize for u in users])