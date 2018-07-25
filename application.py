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
    return render_template("index.html")

@app.route("/chatbox", methods = ['GET', 'POST'])
def chatbox():
    if request.method == "POST":

        # getting displayname of user
        dname = request.form.get("dname")

        # remember which user has logged in
        session["d_name"] = dname

        #
    elif:

        # checking if session is there

        #showing list of channels

@app.route("/new_room", methods = ['GET', 'POST'])
def new_room:
    if request.method == "POST":

        #create new room

        #redirect to chatbox

@app.route("/chatbox/<room>", methods = ['GET', 'POST'])
def chatroom:
                     
