#!/usr/bin/env python3
from app import db, login
from sqlalchemy.orm import relationship
from sqlalchemy.orm import object_session
from sqlalchemy import select, func
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'picture' : self.picture
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    __tablename__ = 'category'
   
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(250), primary_key=True)

    @property
    def item_count(self):
        return object_session(self).\
            scalar(
                select([func.count(Item.id)]).\
                    where(Item.category_id==self.id)
            )

    @property
    def serialize(self):
        return {
            'id'           : self.id,
            'name'         : self.name
        } 

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(250))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description
        }
