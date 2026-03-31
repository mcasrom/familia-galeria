from flask import Flask, render_template, request, Response
import sqlite3, os
from functools import wraps

app = Flask(__name__)

USER="family"
PASSWORD="1234"

# AUTH

def check_auth(u, p): return u==USER and p==PASSWORD

def authenticate():
    return Response("Login required",401,{"WWW-Authenticate":"Basic realm='Login'"})

def requires_auth(f):
    @wraps(f)
    def wrapped(*a, **k):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*a, **k)
    return wrapped

# ROUTES

@app.route("/")
@requires_auth
def index():
    conn = sqlite3.connect('../data/photos.db')
    photos = conn.execute("SELECT * FROM photos").fetchall()
    return render_template("index.html", photos=photos)

@app.route("/tag/<tag>")
@requires_auth
def tag(tag):
    conn = sqlite3.connect('../data/photos.db')
    photos = conn.execute("SELECT * FROM photos WHERE tags LIKE ?",('%'+tag+'%',)).fetchall()
    return render_template("index.html", photos=photos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
