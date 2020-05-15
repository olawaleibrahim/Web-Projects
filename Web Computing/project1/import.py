import csv
import os
from models import Books
from flask import Flask, session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://postgres:Toronto1.@localhost:5432/projects"

engine = create_engine(DATABASE_URL)
db1 = scoped_session(sessionmaker(bind=engine))


def main():
    print(db1)
    print(Books.__table__)
    f = open("books.csv")
    reader = csv.reader(f)
    for idd, isbn, title, author, year in reader:
        db1.execute('INSERT INTO books (idd, isbn, title, author, year) VALUES (:idd, :isbn, :title, :author, :year)',
                    {"idd": idd, "isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added {title} by {author} {year} with ISBN {isbn}")
    db1.commit()


if __name__ == "__main__":
    main()
