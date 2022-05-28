from flask import Flask, jsonify, session, request
import base64
from db import *

app = Flask(__name__)
app.secret_key = "DPYMcFt7gaMU8hq3hvfqAsJ6C5gy9ZJJ"

@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]

    status=create_user(username, password)
    if(status == True):
        session["id"] = find_user(username)[0][0]
        return jsonify(success=True)

    return jsonify(success=False)


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user_id = check_user_creds(username, password)  #  Session token contains userid
    if(len(user_id) == 0):
        return jsonify(success = False), 401

    session["id"] = user_id[0][0]
    return jsonify(success = True)

 
@app.route("/search", methods=["GET"])
def search():
    username = request.args.get("user")
    if(username != None):
        return jsonify(users=find_user(username))
    return jsonify(users=[])


@app.route("/posts/<username>", methods=["GET"])
def user_posts(username):
    posts = find_user_posts(username)
    if(posts == False):
        return jsonify(error="User not found")
    return jsonify(posts=posts)


@app.route("/readpost/<post_id>", methods=["GET"])
def read_post(post_id):
    post = get_post_content(post_id)
    if(post == False):
        return jsonify(status="Not found"), 404

    if "id" in session:
        is_liked = is_post_liked(session["id"], post_id)
    else:
        is_liked = None

    post.append(is_liked)
    return jsonify(post)


@app.route("/like/<post_id>", methods=["GET"])
def like(post_id):
    if "id" not in session:
        return jsonify(status="Unauthorized"), 401

    post = get_post_content(post_id)
    if(post == False):
        return jsonify(status="Not found"), 404

    return jsonify(success=like_post(session["id"], post_id))


@app.route("/post", methods=["POST"])
def createPost():
    if "id" not in session:
        return jsonify(status="Unauthorized"), 401

    user_id = session["id"]
    #  Base64 encoded image is expected from frontend
    image = request.json["image"]  #  null in JSON is set to None
    try:
        image = base64.b64decode(image)
    except:
        return jsonify(error="Bad image encoding"), 400

    content = request.json["content"]
    create_post(user_id, content, image)
    return jsonify(success=True)


@app.route("/follow", methods=["GET"])
def follow():
    return jsonify(success=True)

@app.route("/feed", methods=["GET"])
def feed():
    return jsonify(a=1)

