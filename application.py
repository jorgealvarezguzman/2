import os

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = []
channel_posts = {}
current_channel = None

MAX_POSTS_NUMBER = 100

@app.route("/")
def index():
    if current_channel is not None:
        return redirect(url_for('channel', channel=current_channel))

    return render_template("index.html", channels=channels)

@socketio.on("submit displayName")
def addDisplayName(data):
    displayName = data["displayName"]
    emit("confirmDisplayName", displayName, broadcast=True)

@socketio.on("submit channel")
def addChannel(data):
    global current_channel
    channel = data["channel"]
    if channel in channels:
        return render_template("index.html", channels=channels)
    current_channel = channel
    if channel not in channel_posts:
        channel_posts[channel] = []
    channels.append(channel)
    emit("addChannel", channel, broadcast=True)

@app.route("/channel/<string:channel>", methods=["POST", "GET"])
def channel(channel):
    global current_channel
    current_channel = channel
    if request.method == "GET":
        return render_template("index.html", channels=channels)
    return jsonify(channel_posts[current_channel])

@socketio.on("submit post")
def addPost(data):
    global current_channel
    post = data["displayName"] + " " + str(datetime.now()) + " " + data["post"]

    if len(channel_posts[current_channel]) == MAX_POSTS_NUMBER:
        channel_posts[current_channel].pop(0)
    channel_posts[current_channel].append(post)
    emit("addPost", post, broadcast=True)
