import os
import requests

from flask import Flask, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
DATABASE_URL = "postgresql://postgres:Toronto1.@localhost:5432/projects"
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


engine = create_engine(DATABASE_URL)
db1 = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home", methods=["POST", 'GET'])
def home():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users2(id=id, first_name=first_name,
                      last_name=last_name, email=email, password=password)
        # db.session.add(user)
        #print(f'{first_name} {last_name}, {email} and {len(password)*"*"} are recorded')
        # db.session.commit()

        db1.execute('INSERT INTO users2 (email, password, first_name, last_name) VALUES (:email, :password, :first_name, :last_name)',
                    {"email": email, "password": password, "first_name": first_name, "last_name": last_name})

        db1.commit()

        return render_template("home.html", first_name=first_name, last_name=last_name,
                               email=email, password=password)

    else:
        return 'Failed'


@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'GET':
        return render_template("error.html", message="Access Denied. Login to enter books page")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        
        if db1.execute("SELECT * FROM users2 WHERE email=:email AND password=:password", {"email": email, "password": password}).fetchone():
            return render_template("books.html")
        else:
            return render_template("error.html", message="Incorrect login details")

@app.route('/books/<int:book_id>', methods=['POST', 'GET'])
def book(book_id):
    book = db1.execute("SELECT * FROM books WHERE idd=:idd", {"idd":book_id}).fetchone()
    if book == None:
        return render_template("error.html", message="No such book exist")
    else:

        return render_template("book.html", book=book)


@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        return render_template("error.html", message="Access Denied. Sign in and search for book")
    else:
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")

        if (db1.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).rowcount == 0) and (db1.execute("SELECT * FROM books WHERE title=:title", {"title": title}).rowcount == 0) and (db1.execute("SELECT * FROM books WHERE author=:author", {"author": author}).rowcount == 0):
            return render_template("error.html", message="No book with matching records")

        else:
            books = db1.execute("SELECT * FROM books WHERE author=:author OR title=:title OR isbn=:isbn", {"author": author,"title": title, "isbn": isbn}).fetchall()
            
            return render_template("results.html", books=books)


def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "XpVcEz3pf5hXpJ7pzhMng", "isbns": "9781632168146"})
    print(res.json())


if __name__ == '__main__':
    main()
