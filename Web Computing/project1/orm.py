import csv
from flask import Flask, render_template, request
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from models import Books1, Reviews

DATABASE_URL = "postgresql://postgres:Toronto1.@localhost:5432/projects"

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)


engine = create_engine(DATABASE_URL)
db1 = scoped_session(sessionmaker(bind=engine))

def main():
    #f = open("books.csv")
    #reader = csv.reader(f)
    #for idd, isbn, title, author, year in reader:
    #    book = Books1(isbn=isbn, title=title, author=author, year=year)
    #    db.session.add(book)
    #    print(f'{book.title} is added')
    print(Books1.query.filter_by(author="Jerry Spinelli").first())
    book = Books1.query.get(6)
    print(f'{book.author}')
    book.author = "Joe Plagiariser"
    print(f'{book.author}')
    db.session.commit()
    #print(Books1.query.order_by(Books1.year).all())
    h1 = Books1.query.get(3891)
    print(h1.year)
    books = Books1.query.filter(Books1.title.like("%Lion%")).all()
    books1 = Books1.query.filter(Books1.author == "Candace Bushnell").all()
    books2 = books+books1
    for i in books:
        print(f'{i.title}')

    #review1 = Reviews(1, "dklskdg", 2, "jblbff", 4)
    #db.session.add(review1)
    db.session.commit()
    review2 = db1.execute("SELECT * FROM reviews WHERE book_id=1848").fetchall()
    db1.commit()
    reviews = []
    scores = []
    for review in review2:
        reviews.append(review.review)
        db1.commit()
    for review in review2:
        scores.append(review.score)
        db1.commit()

    print(reviews)
    print(scores)
    

if __name__ == '__main__':
    with app.app_context():
        main()
