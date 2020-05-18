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
        review1 = db1.execute("SELECT * FROM reviews WHERE book_id=:idd", {"idd": book_id}).fetchall()
        avg = db1.execute("SELECT AVG(reviews.score) FROM reviews WHERE book_id=:idd", {"idd": book_id})
        db1.commit()
        reviews = []
        scores = []
        avgscore = []
        for review in review1:
            reviews.append(review.review)
            db1.commit()
        for review in review1:
            scores.append(review.score)
            db1.commit()
        for i in avg:
            avgscore.append(i)

        return render_template("book.html", book=book, reviews=reviews, scores=scores, avgscore=avgscore)


@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        return render_template("error.html", message="Access Denied. Sign in and search for book")
    else:
        value = request.form.get("value")
        #title = request.form.get("title")
        #author = request.form.get("author")

        if (db1.execute("SELECT * FROM books WHERE isbn=:value", {"value": value}).rowcount == 0) and (db1.execute("SELECT * FROM books WHERE title=:value", {"value": value}).rowcount == 0) and (db1.execute("SELECT * FROM books WHERE author=:value", {"value": value}).rowcount == 0):
            return render_template("error.html", message="No book with matching records")

        else:
            books = db1.execute("SELECT * FROM books WHERE author LIKE :value OR title LIKE :value OR isbn LIKE :value", {"value": value,"value": value, "value": value}).fetchall()
            #books = Books.query.filter(Books.title.like('%title%')).all()
            db.session.commit()
            return render_template("results.html", books=books)

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    if request.method == 'GET':
        return render_template("error.html", message="Invalid request.")
    else:
        score = request.form.get("review")
        review = request.form.get("description")
        title = request.form.get("book_title")

        if score == None or title == None:
            return render_template("error.html", message="Please give a review or select book title")
        else:
            book = db1.execute("SELECT * FROM books WHERE title=:title", {'title': title}).fetchone()
            
            book_id = book.idd

            db1.execute("INSERT INTO reviews (score, review, title, book_id) VALUES (:score, :review, :title, :book_id)",
            {"score": score, "review": review, "title": title, "book_id": book_id})
            db1.commit()
            #review1 = Reviews(review=review, score=score, title=title, book_id=book_id)
            #b.session.add(review1)
            #db.session.commit()
            return render_template("submitted.html", message="Review submitted")


def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "XpVcEz3pf5hXpJ7pzhMng", "values": "9781632168146"})
    print(res.json())


if __name__ == '__main__':
    main()
