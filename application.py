import os

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = []
channel_posts = []

@app.route("/")
def index():
    return render_template("index.html", channels=channels)

@socketio.on("submit displayName")
def addDisplayName(data):
    displayName = data["displayName"]
    emit("confirmDisplayName", displayName, broadcast=True)

@socketio.on("submit channel")
def addDisplayName(data):
    channel = data["channel"]
    if channel in channels:
        return render_template("index.html", channels=channels)
    channels.append(channel)
    emit("addChannel", channel, broadcast=True)

@app.route("/channel/<string:channel>")
def channel(channel):
    #socketio.emit("displayChannel", channel=channel, broadcast=False)
    return render_template("index.html", channels=channels)

@app.route("/posts", methods=["POST"])
def posts():
    post = request.form.get("post")
    channel_posts.append(post)
    return jsonify(channel_posts)
