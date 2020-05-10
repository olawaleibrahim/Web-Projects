import datetime
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

@app.route("/", methods=['POST', 'GET'])
def index():
    headline = "Welcome here!"
    semesters = ['First Semester', 'Second Semester', 'Third Semester']
    
    if session.get("notes") is None:
        session["notes"] = []
    
    if request.method == 'POST':
        note = request.form.get("note")
        session["notes"].append(note)

    return render_template("index.html", headline=headline, semesters=semesters, notes=session["notes"])

@app.route('/contact')
def contact():
    return render_template("contacts.html")

@app.route('/thankyou', methods=['POST', 'GET'])
def thank_you():
    if request.method == 'GET':
        return('Please submit the form instead')
    else:
        name = request.form.get("name")
        return render_template("thankyou.html", name=name)

