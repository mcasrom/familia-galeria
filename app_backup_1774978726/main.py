from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

# Carpetas
APP_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_DIR, "../uploads")
DATA_FOLDER = os.path.join(APP_DIR, "../data")
TAGS_FILE = os.path.join(DATA_FOLDER, "tags.json")

# Crear carpeta de datos si no existe
os.makedirs(DATA_FOLDER, exist_ok=True)

# Login simple
USERNAME = "Family"
PASSWORD = "4321"

# Cargar tags
if os.path.exists(TAGS_FILE):
    with open(TAGS_FILE, "r") as f:
        tags = json.load(f)
else:
    tags = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == USERNAME and pwd == PASSWORD:
            return redirect(url_for("gallery"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/gallery")
def gallery():
    fotos = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return render_template("gallery.html", fotos=fotos, tags=tags)

@app.route("/fotos/<filename>")
def fotos(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    # También borrar tags si existen
    if filename in tags:
        tags.pop(filename)
        with open(TAGS_FILE, "w") as f:
            json.dump(tags, f)
    return redirect(url_for("gallery"))

@app.route("/update_tag", methods=["POST"])
def update_tag():
    filename = request.form.get("filename")
    tag_value = request.form.get("tag")
    if filename:
        tags[filename] = tag_value
        with open(TAGS_FILE, "w") as f:
            json.dump(tags, f)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
