#!/usr/bin/env python3
from app import app, db 
from flask import jsonify
from app.models import User, Category, Item

# Catalog JSON APIs
@app.route('/catalog/JSON')
def catalogJSON():
    categories = db.session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/<string:category_name>/JSON')
@app.route('/catalog/<string:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = db.session.query(Category).filter_by(name=category_name).one()
    items = db.session.query(Item).filter_by(
        category_id=category.id).all()

    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    category = db.session.query(Category).filter_by(name=category_name).one()
    item = db.session.query(Item).filter_by(
        category_id=category.id,
        name=item_name).one()

    return jsonify(item=item.serialize)

@app.route('/catalog/users/JSON')
def usersJSON():
    users = db.session.query(User).all()
    return jsonify(users=[u.serialize for u in users])