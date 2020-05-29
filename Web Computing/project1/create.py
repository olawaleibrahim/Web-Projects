import os

from flask import Flask, render_template, request
from models import *

DATABASE_URL = "postgres://bbfndfqfhqjwjk:6edcaed6c232e33cb00795391243fc3023c01c875dc07cbe79b82549f3bca9c3@ec2-52-71-55-81.compute-1.amazonaws.com:5432/dcgps6isnvdfga"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

engine = create_engine(DATABASE_URL)
db1 = scoped_session(sessionmaker(bind=engine))

def main():
    db.create_all()
    #book = Books(year=1999, author='David Scwhimmer', isbn=1307530959484, title="The Return of the Jedis")
    #db.session.add(book)
    #b1 = db1.execute("SELECT * FROM books")
   # for i in b1:
    #    print(f'{i.year}, {i.author}, {i.id}')

if __name__ == "__main__":
    with app.app_context():
        main()
