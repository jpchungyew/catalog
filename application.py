from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, session as login_session, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

import random
import string
import requests
import httplib2
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'

#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db',
    connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Catalog JSON APIs
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/<string:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()

    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(
        category_id=category.id,
        name=item_name).one()

    return jsonify(item=item.serialize)

@app.route('/user/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(users=[u.serialize for u in users])

# Catalog Pages
# Show all categories with latest added items
@app.route('/')
@app.route('/catalog')
def showHomepage():

    login_session['username'] = 'username'
    login_session['user_id'] = 1

    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(5)

    if 'username' not in login_session:
        return render_template('publichomepage.html', categories=categories)
    else:
        return render_template('homepage.html', categories=categories)

# Show all items in a category
@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>/items')
def showCategoryItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    
    if 'username' not in login_session:
        return render_template('publicitems.html', category=category, items=items)
    else:
        return render_template('items.html', category=category, items=items)


# Create a new item
@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
def newItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    
    category = session.query(Category).filter_by(name=category_name).one()

    logged_in_user = User(id=1)

    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category.id,
            user_id=logged_in_user.id)

        session.add(newItem)
        session.commit()

        flash('%s successfully added' % (newItem.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('newitem.html', category_id=category.id)

# Edit an item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(id=item.category_id).one()

    if login_session['user_id'] != item.user_id:
        return render_template('unauthorizedtoedititem.html')
    
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']

        session.add(item)
        session.commit()
        flash('%s successfully edited' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('edititem.html', category=category, item=item)

# Delete an item
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(id=item.category_id).one()

    if login_session['user_id'] != item.user_id:
        return render_template('unauthorizedtodeleteitem.html')
        
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('%s successfully deleted' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('deleteitem.html', category=category, item=item)

if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)