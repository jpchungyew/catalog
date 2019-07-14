#!/usr/bin/env python3
from sqlalchemy import create_engine
from config import Config
from sqlalchemy.orm import sessionmaker
from catalogapp import app, db, login_google
from flask import render_template, request, redirect, url_for, flash
from flask import session as login_session
# from flask_login import current_user, login_user, logout_user
from catalogapp.models import Base, User, Category, Item

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)

# Catalog Pages
# Show all categories with latest added items
@app.route('/')
@app.route('/catalog')
def showHomepage():
    session = Session()

    categories = session.query(Category).all()

    if 'id' not in login_session:
        return render_template('publichomepage.html', categories=categories)
    else:
        return render_template('homepage.html', categories=categories)

# Show all items in a category
@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>/items')
def showCategoryItems(category_name):
    session = Session()
    
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    
    if 'id' not in login_session:
        return render_template('publicitems.html', category=category, items=items)
    else:
        return render_template('items.html', category=category, items=items)

# Create a new item
@app.route('/catalog/new', methods=['GET', 'POST'], defaults={'category_name': ''})
@app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
def newItem(category_name):
    if 'id' not in login_session:
        return render_template('loginrequired.html')

    session = Session()

    categories = session.query(Category).all()

    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session.get('id'))

        session.add(newItem)
        session.commit()

        category = session.query(Category).filter_by(id=newItem.category_id).one()

        flash('%s successfully added' % (newItem.name))
        return redirect(url_for('viewItem', category_name=category.name, item_name=newItem.name))
    else:
        if category_name != '':
            category = session.query(Category).filter_by(name=category_name).one()
        else:
            category = session.query(Category).limit(1).one()

        return render_template('newitem.html', category_id=category.id, categories=categories)

# View an item
@app.route('/catalog/<string:category_name>/<string:item_name>', methods=['GET', 'POST'])
def viewItem(category_name,item_name):
    session = Session()
    
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name).one()

    if 'id' not in login_session:
        return render_template('publicitem.html', category=category, item=item)
    else:
        return render_template('item.html', category=category, item=item, current_user_id=login_session.get('id'))

# Edit an item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if 'id' not in login_session:
        return render_template('loginrequired.html')
    
    session = Session()

    item = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    categories = session.query(Category).all()

    if login_session.get('id') != item.user_id:
        flash('you are not allowed to edit this item')

        return redirect(url_for('viewItem', category_name=category.name, item_name=item_name))
    
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']

        session.add(item)
        session.commit()
        flash('%s successfully edited' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('edititem.html', category=category, item=item, categories=categories)

# Delete an item
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'id' not in login_session:
        return render_template('loginrequired.html')

    session = Session()

    item = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(id=item.category_id).one()

    if login_session.get('id') != item.user_id:
        flash('you are not allowed to delete this item')

        return redirect(url_for('viewItem', category_name=category.name, item_name=item_name))
        
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('%s successfully deleted' % (item.name))
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('deleteitem.html', category=category, item=item)

# Login methods
@app.route('/login', methods=['POST'])
def login():
    session = Session()

    response = login_google.gconnect(request)

    if response.status_code == 200 and response.json.get('email') != "":
        try:
            user = session.query(User).filter_by(email=response.json.get('email')).one()
        except:
            newUser = User(
                name=response.json.get('name'), 
                email=response.json.get('email'), 
                picture=response.json.get('picture'))
            session.add(newUser)
            session.commit()

            user = session.query(User).filter_by(email=response.json.get('email')).one()  

        # login_user(user)
        login_session['id'] = user.id

    return response

@app.route('/logout', methods=['POST'])
def logout():

    response = login_google.gdisconnect()
    # logout_user()
    del login_session['id']

    return response
