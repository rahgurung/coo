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

    # clearing session
    session.clear()

    # setting logged_in to which mean we are not logged in
    session["logged_in"] = 0

    # returning our basic index page
    return render_template("index.html")

@app.route("/home", methods = ['GET', 'POST'])
def home():
    if request.method == "POST":

        # adding it to the session
        session["d_name"] = request.form.get("dname")

        # adding the logged_in trigger
        session["logged_in"] = 1

        # getting Name
        name = session["d_name"]

        # returning login page
        return render_template("home.html", name = name)

    elif request.method == "GET":

        # checking if we are logged in
        if session["logged_in"] == 1:

            # getting display name from session
            name = session["d_name"]

            # returning home with display name
            return render_template("home.html", name = name)

        else:
            # returning home page without display name
            return render_template("home.html")

@app.route("/logout")
def logout():

    # clearing the session
    session.clear()

    # setting logged_in to 0 which means we aren't logged in
    session["logged_in"] = 0

    # returning index page
    return render_template("index.html")
