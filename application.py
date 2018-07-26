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

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":

        # adding it to the session
        session["d_name"] = request.form.get("dname")

        # returning login page
        return render_template("login.html")

    elif request.method == "GET":

        # returning login page
        return render_template("login.html")

@app.route("/logout")
def logout():

    # clearing the session
    session.clear()

    # returning index page
    return render_template("index.html")

@app.route("/new_room", methods = ['GET', 'POST'])
def new_room():
    if request.method == "POST":

        #create new room
        return 0;
        #redirect to chatbox

@app.route("/chatbox/<room>", methods = ['GET', 'POST'])
def chatroom():
    return 0;
