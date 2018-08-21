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

    if (msg_status == "PUBLIC"):
        my_msgs = channel_messages.get(channel)
    else:
        my_msgs = user_dm_list.get(channel)

    if my_msgs:
        msglist = my_msgs['messages']
        if ((msg_status == 'PUBLIC') or (channel == dn)):
            return jsonify({"success": True, "channel_msgs": msglist})
        else:
            all_msgs = []
            for msg in msglist:
                if((msg["user_from"] == dn) or (msg["user_to"] == dn)):
                    all_msgs.append(msg)
                return jsonify({"success": True, "channel_msgs": all_msgs})
    else:
        return jsonify({"success": False, "error_msg": "No messages"})

# this is the socketio backend to handle the submit messages
# event in the flask, it shows public channel
@socketio.on("submit message")
def new_message(data):
    channel = data["channel"]
    user_from = data["user_from"]
    msg_txt = data["msg_txt"]
    timestamp = time.asctime( time.localtime( time.time() ) )

    msg = {"channel": channel,
           "user_from": user_from,
           "user_to": channel,
           "timestamp": timestamp,
           "msg_txt": msg_txt}

    if channel in channel_messages:
         # Public Channel with messages
        msgs = channel_messages[channel]
        msg["msg_type"] = "PUBLIC"
        if len(msgs['messages']) >= 100:
            del msgs['messages'][0]
        msgs['messages'].append(msg)
        emit("announce message", msg, broadcast=True)
        return jsonify ({"success": True, "msg_type": "PUBLIC"})
    else:
        if (not (channel in user_dm_list)):
            # public channel, first message
            msg["msg_type"] = "PUBLIC"
            channel_messages[channel] = {"channel": channel, "messages": [msg]}
            emit("announce message", msg, broadcast=True)
            return jsonify ({"success": True, "msg_type": "PUBLIC"})
        else:
            # private message
            msg["msg_type"] = "PRIVATE"
            if (channel in user_dm_list):
                for user in [user_from, channel]:
                    msgs = user_dm_list[user]
                    if len(msgs['messages']) >= 100:
                        del msgs['messages'][0]
                    msgs['messages'].append(msg)
            else:
                user_dm_list[user] = {"channel": channel, "messages": [msg]}
            print (f"NM: emit msg to ", user_from)
            msg["channel"] = channel
            emit("announce message", msg, room=Rooms[user_from])
            print (f"NM: emit msg to ", channel)
            msg["channel"] = user_from
            emit("announce message", msg, room=Rooms[channel])
            return jsonify ({"success": True, "msg_type": "PRIVATE"})
