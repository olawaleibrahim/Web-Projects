import os
import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

SECRET_KEY = 'dbfjblgfbxk'
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/chatapp', methods=['POST'])
def chatapp():
    username = request.form.get("username")
    return render_template("chatapp.html", username=username)

@socketio.on('create channel')
def channel(data):
    selection = data['selection']
    emit("channel created", {'selection': selection}, broadcast=True)

@socketio.on('message sent')
def message(data):
    message = data['message']
    emit('message bc', {'message': message}, broadcast=True)
