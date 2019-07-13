#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

session.query(User).delete()
session.query(Item).delete()
session.query(Category).delete()

# dummy user
User1 = User(name="Mr. Bogus", email="mr.bogus@bogusland.com",
             picture='https://en.wikipedia.org/wiki/File:Bogus.jpg')
session.add(User1)
session.commit()

# dummy categories and items
category1 = Category(name="Mythical Places")

session.add(category1)
session.commit()

item1 = Item(
    user_id=1,
    name="Agartha",
    description="A legendary city at Earth's core.",
    category=category1)

session.add(item1)
session.commit()

item2 = Item(
    user_id=1,
    name="Atlantis",
    description="The legendary (and almost archetypal) lost continent that was supposed to have sunk into the Atlantic Ocean.",
    category=category1)

session.add(item2)
session.commit()

item3 = Item(
    user_id=1,
    name="El Dorado",
    description="Rumored city of gold in South America.",
    category=category1)

session.add(item3)
session.commit()

item4 = Item(
    user_id=1,
    name="Shangri-La",
    description="A mystical, harmonious valley enclosed in the western end of the Kunlun Mountains.",
    category=category1)

session.add(item4)
session.commit()

category2 = Category(name="Mythical Creatures")

session.add(category2)
session.commit()

item5 = Item(
    user_id=1,
    name="Centaur",
    description="A creature with a head and torso of a human and the body of a horse.",
    category=category2)

session.add(item5)
session.commit()

item6 = Item(
    user_id=1,
    name="Hugag",
    description="A 13-foot-tall moose-like... thing",
    category=category2)

session.add(item6)
session.commit()

print('added dummy items!')