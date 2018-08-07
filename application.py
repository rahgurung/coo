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
        return render_template("home.html", name = name, channels = channels)

    elif request.method == "GET":

        # checking if we are logged in
        if session["logged_in"] == 1:

            # getting display name from session
            name = session["d_name"]

            # returning home with display name
            return render_template("home.html", name = name, channels = channels)

        else:
            # returning home page without display name
            return render_template("home.html")

@app.route("/channelcreate", methods= ['GET', 'POST'])
def channelcreate():

    #checking method
    if request.method == "GET":

        return render_template("channelcreate.html")

    elif request.method == "POST":

        # get the name of channel
        channel_name = request.form.get("channel_name")

        # error check
        if not channel_name:
            return render_template("channelcreate.html")

        # check if channel name is already there
        if channel_name in channels:
            return render_template("channelcreate.html")

        # add channel to the list
        channels.append(channel_name)

        return redirect(url_for('home'))

@app.route("/channel/<channel_name>")
def showchannel(channel_name):
    if channel_name not in channels:
        return "This channel is not there."
    return f"You are in, {channel_name} !"


@app.route("/logout")
def logout():

    # clearing the session
    session.clear()

    # setting logged_in to 0 which means we aren't logged in
    session["logged_in"] = 0

    # returning index page
    return render_template("index.html")
