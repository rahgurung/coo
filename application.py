import os

from flask import Flask, session, render_template, url_for, request, redirect, jsonify
from flask_session import Session
import random, json, time, datetime

from flask_socketio import SocketIO, emit, join_room, leave_room

# configure the flask_socketio
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# list of channels
channels = ["General"]
user_list = []

# Dictionary of users & messages
user_dm_list = {}

# dictionary to track rooms, or private channels
# Rooms = {"dn:" displayname, "room": room}
Rooms = {}

now = datetime.datetime.now()

startup_message = {
    "channel": "General",
    "user_from": "Flack Bot",
    "user_to": "",
    "timestamp": now.strftime("%a %b %d %I:%M:%S %Y"),
    "msg_txt": "Welcome to Flack Messaging"}

channel_messages = {
    "General": {
        'messages': [startup_message]
}}

@app.route("/")
def index():
    # returning our basic index page
    return render_template("index.html")

# handles home where list of channel is there with logout button
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

# handles channel create button which loads channel creation page
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

# handles the chatrooms
@app.route("/coochat", methods=["POST", "GET"])
def flackchat():
    user = session["d_name"]
    return render_template("chatbox.html", name=user)

# handles the logout button
@app.route("/logout", methods=["POST"])
def logout():
    # returning index page
    return render_template("index.html")
