from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://postgres:Toronto1.@localhost:5432/projects"

engine = create_engine(DATABASE_URL)
db1 = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

class Books(db.Model):
    __tablename__ = "books"
    idd = db.Column(db.Integer, nullable=False, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

class Users2(db.Model):
    __tablename__ = "users2"
    counter = 1

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

    def __init__(self, id, email, password, first_name, last_name):
        self.id = Users2.counter
        Users2.counter += 1

        self.users1 = []
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Books1(db.Model):
    __tablename__ = "books1"
    idd = db.Column(db.Integer, nullable=False, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

class Reviews(db.Model):
    __tablename__ = "reviews"
    counter = 1
    
    idd = db.Column(db.Integer, nullable=False, primary_key=True)
    review = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.idd'))   
    score = db.Column(db.Integer, nullable=True)

    def __init__(self, idd, review, score, title, book_id):
        self.idd = self.counter
        self.counter += 1     

        
        self.review = review
        self.title = title
        self.book_id = book_id
        self.score = score

class Loggedin(db.Model):
    __tablename__ = "loggedin"
    counter = 1

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


    def __init__(self, id, email, password):
        self.id = Users2.counter
        Loggedin.counter += 1

        
        self.email = email
        self.password = password
        
