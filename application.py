import os

from flask import Flask, session, render_template, url_for, request, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# list of channels
channels = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbox")
def chatbox():
    if method == "post":
            