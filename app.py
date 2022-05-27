from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    return ""
    
@app.route("/search", methods=["GET"])
def search():
    return []
