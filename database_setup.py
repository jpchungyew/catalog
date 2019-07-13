# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# from sqlalchemy.orm import object_session
# from sqlalchemy import select, func
 
# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'user'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     email = Column(String(250), nullable=False)
#     picture = Column(String(250))

#     @property
#     def serialize(self):
#         return {
#             'id' : self.id,
#             'name' : self.name,
#             'email' : self.email,
#             'picture' : self.picture
#         }

# class Category(Base):
#     __tablename__ = 'category'
   
#     id = Column(Integer, autoincrement=True)
#     name = Column(String(250), primary_key=True)

#     @property
#     def item_count(self):
#         return object_session(self).\
#             scalar(
#                 select([func.count(Item.id)]).\
#                     where(Item.category_id==self.id)
#             )

#     @property
#     def serialize(self):
#         return {
#             'id'           : self.id,
#             'name'         : self.name
#         } 

# class Item(Base):
#     __tablename__ = 'item'

#     id = Column(Integer, autoincrement=True)
#     name =Column(String(80), primary_key=True)
#     description = Column(String(250))
#     category_id = Column(Integer,ForeignKey('category.id'))
#     category = relationship(Category)
#     user_id = Column(Integer,ForeignKey('user.id'))
#     user = relationship(User)

#     @property
#     def serialize(self):
#         return {
#             'id' : self.id,
#             'name' : self.name,
#             'description' : self.description
#         }

# engine = create_engine('sqlite:///catalog.db')
# Base.metadata.create_all(engine)