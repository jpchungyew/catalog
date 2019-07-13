#!/usr/bin/env python3
from app import app, db 
from flask import render_template, request, redirect, jsonify, url_for, flash
from flask_login import current_user, login_user
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

@app.route('/user/JSON')
def usersJSON():
    users = db.session.query(User).all()
    return jsonify(users=[u.serialize for u in users])

# Catalog Pages
# Show all categories with latest added items
@app.route('/')
@app.route('/catalog')
def showHomepage():

    User1 = User(id=1, name="Mr. Bogus", email="mr.bogus@bogusland.com",
             picture='https://en.wikipedia.org/wiki/File:Bogus.jpg')
    login_user(User1)
    # login_session['username'] = 'username'
    # login_session['user_id'] = 1

    categories = db.session.query(Category).all()

    if not current_user.is_authenticated:
        return render_template('publichomepage.html', categories=categories)
    else:
        return render_template('homepage.html', categories=categories)

# Show all items in a category
@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>/items')
def showCategoryItems(category_name):
    category = db.session.query(Category).filter_by(name=category_name).one()
    items = db.session.query(Item).filter_by(category_id=category.id).all()
    
    if not current_user.is_authenticated:
        return render_template('publicitems.html', category=category, items=items)
    else:
        return render_template('items.html', category=category, items=items)


# Create a new item
@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
def newItem(category_name):
    if not current_user.is_authenticated:
        return redirect('/login')
    
    category = db.session.query(Category).filter_by(name=category_name).one()

    logged_in_user = User(id=1)

    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category.id,
            user_id=logged_in_user.id)

        db.session.add(newItem)
        db.session.commit()

        flash('%s successfully added' % (newItem.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('newitem.html', category_id=category.id)

# Edit an item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if not current_user.is_authenticated:
        return redirect('/login')

    item = db.session.query(Item).filter_by(name=item_name).one()
    category = db.session.query(Category).filter_by(id=item.category_id).one()

    if current_user.id != item.user_id:
        return render_template('unauthorizedtoedititem.html')
    
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']

        db.session.add(item)
        db.session.commit()
        flash('%s successfully edited' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('edititem.html', category=category, item=item)

# Delete an item
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if not current_user.is_authenticated:
        return redirect('/login')

    item = db.session.query(Item).filter_by(name=item_name).one()
    category = db.session.query(Category).filter_by(id=item.category_id).one()

    if current_user.id != item.user_id:
        return render_template('unauthorizedtodeleteitem.html')
        
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('%s successfully deleted' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('deleteitem.html', category=category, item=item)
