import os

from flask import Flask, session, render_template, url_for, request, redirect, jsonify
from flask_session import Session

from flask_socketio import SocketIO, emit

# configure the flask_socketio
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# list of channels
channels = []

@app.route("/")
def index():
    session.clear()
    session["logged_in"] = 0
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":

        # adding it to the session
        session["d_name"] = request.form.get("dname")

        # adding the logged_in trigger
        session["logged_in"] = 1

        # getting Name
        name = session["d_name"]

        # returning login page
        return render_template("login.html", name = name)

    elif request.method == "GET":

        if session["logged_in"] == 1:

            name = session["d_name"]

            return render_template("login.html", name = name)

        else:
        # returning login page with display name
            return render_template("login.html")

@app.route("/logout")
def logout():

    # clearing the session
    session.clear()
    session["logged_in"] = 0

    # returning index page
    return render_template("index.html")
