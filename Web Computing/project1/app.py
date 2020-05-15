import os

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

        user = Users2(id=id, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        print(f'{first_name} {last_name}, {email} and {len(password)*"*"} are recorded')
        db.session.commit()

        return render_template("home.html", first_name=first_name, last_name=last_name,
                               email=email, password=password)

    else:
        return 'Failed'
