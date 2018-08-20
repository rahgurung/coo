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

# this is our index page
@app.route("/")
def index():
    return render_template("index.html")


# this function handles the logout button and returns
# index page as a result
@app.route("/logout", methods=["POST"])
def logout():
    return render_template("index.html")


# this handles the whole chatrooms
@app.route("/chatbox", methods=["POST", "GET"])
def chatbox():
     user = request.form.get("displayname")
     return render_template("chatbox.html", name=user)


# this is a event of submitting channel to create
# a new channel
@socketio.on("submit channel")
def new_channel(data):
    channel = data["channel"]
    channel_list.append(channel)
    emit("announce channel", {"channel": channel}, broadcast=True)
    return 1

# this is the backend to support querying for
# list of new available channels
@app.route("/query_channels", methods=["POST"])
def query_channels():
    return jsonify({"success": True, "channel_list": channel_list})


# this is the backend to support querying for
# users in a channel
@app.route("/query_users", methods=["POST"])
def query_users():
    return jsonify({"success": True, "active_users": user_list})

# this is the backend to support querying for
# messages in a channel
@app.route("/query_messages", methods=["POST"])
def fetch_messages():
    channel = request.form.get("channel")
    dn = request.form.get("displayname")
    msg_status = request.form.get("msg_type")
