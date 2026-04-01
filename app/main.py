from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify
import os
import json
import shutil

# =========================
# App y configuración
app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# =========================
# Carpetas y rutas ajustadas para Render
APP_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_DIR, "../uploads")
DATA_FOLDER = os.path.join(APP_DIR, "../data")
TRASH_FOLDER = os.path.join(APP_DIR, "../trash")
TAGS_FILE = os.path.join(DATA_FOLDER, "tags.json")

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(TRASH_FOLDER, exist_ok=True)

# =========================
# Usuarios y contraseñas
USERNAME = "Family"
PASSWORD = "4321"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# =========================
# Import y registro del módulo de uploads
from app.upload_module import register_upload
register_upload(app, UPLOAD_FOLDER)

# =========================
# Rutas básicas

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if (user == USERNAME and pwd == PASSWORD) or (user == ADMIN_USER and pwd == ADMIN_PASS):
            session["user"] = user
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# =========================
# Uploads y gestión de archivos
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Ejemplo de eliminación de archivo (mover a trash)
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))
    src = os.path.join(UPLOAD_FOLDER, filename)
    dst = os.path.join(TRASH_FOLDER, filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect(url_for("index"))

# =========================
# API simple de tags
@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "POST":
        data = request.json
        with open(TAGS_FILE, "w") as f:
            json.dump(data, f)
        return jsonify({"status": "ok"})
    else:
        if os.path.exists(TAGS_FILE):
            with open(TAGS_FILE, "r") as f:
                data = json.load(f)
            return jsonify(data)
        return jsonify([])

# =========================
# Opcional: endpoint de limpieza de trash (solo admin)
@app.route("/trash/clear", methods=["POST"])
def clear_trash():
    if "user" not in session or session["user"] != ADMIN_USER:
        return redirect(url_for("login"))
    for filename in os.listdir(TRASH_FOLDER):
        path = os.path.join(TRASH_FOLDER, filename)
        if os.path.isfile(path):
            os.remove(path)
    return redirect(url_for("index"))

# =========================
# Run app local (solo si se ejecuta directamente)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
