from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, session
import os
import json
import shutil

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# =========================
# Carpetas y rutas ajustadas
APP_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_DIR, "uploads")
DATA_FOLDER = os.path.join(APP_DIR, "data")
TRASH_FOLDER = os.path.join(APP_DIR, "trash")
TAGS_FILE = os.path.join(DATA_FOLDER, "tags.json")

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(TRASH_FOLDER, exist_ok=True)

# =========================
# Import del módulo de uploads
from upload_module import register_upload
register_upload(app, UPLOAD_FOLDER)

# =========================
# Usuarios y contraseñas
USERNAME = "Family"
PASSWORD = "4321"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# =========================
# UTILIDADES
# =========================
def load_tags():
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_tags(tags):
    with open(TAGS_FILE, "w") as f:
        json.dump(tags, f, indent=4)


def safe_filename(filename):
    return os.path.basename(filename)


def require_admin():
    if not session.get("logged") or session.get("role") != "admin":
        return False
    return True


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == USERNAME and pwd == PASSWORD:
            session["logged"] = True
            session["role"] = "viewer"
            return redirect(url_for("gallery"))
        elif user == ADMIN_USER and pwd == ADMIN_PASS:
            session["logged"] = True
            session["role"] = "admin"
            return redirect(url_for("gallery"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")


# =========================
# GALERÍA
# =========================
@app.route("/gallery")
def gallery():
    if not session.get("logged"):
        return redirect(url_for("login"))
    
    fotos = sorted([
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    tags = load_tags()
    return render_template("gallery_v2.html", fotos=fotos, tags=tags)


@app.route("/fotos/<filename>")
def fotos(filename):
    filename = safe_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)


# =========================
# BORRAR FOTO
# =========================
@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    if not require_admin():
        return jsonify(success=False, error="No autorizado"), 403
    
    filename = safe_filename(filename)
    src = os.path.join(UPLOAD_FOLDER, filename)
    dst = os.path.join(TRASH_FOLDER, filename)
    
    if os.path.exists(src):
        shutil.move(src, dst)
    
    # Eliminar tags asociados
    tags = load_tags()
    if filename in tags:
        tags.pop(filename, None)
        save_tags(tags)
    
    return jsonify(success=True)


# =========================
# TAGS (AÑADIR Y ELIMINAR)
# =========================
@app.route("/update_tag", methods=["POST"])
def update_tag():
    filename = safe_filename(request.form.get("filename"))
    tag_value = request.form.get("tag")

    tags = load_tags()
    if filename not in tags:
        tags[filename] = []
    
    if tag_value and tag_value not in tags[filename]:
        tags[filename].append(tag_value)
        save_tags(tags)

    return jsonify(success=True, tags=tags.get(filename, []))


@app.route("/delete_tag", methods=["POST"])
def delete_tag():
    if not session.get("logged"):
        return jsonify(success=False), 403

    filename = safe_filename(request.form.get("filename"))
    tag = request.form.get("tag")

    tags = load_tags()

    if filename in tags and tag in tags[filename]:
        tags[filename].remove(tag)
        if not tags[filename]:          # Si ya no quedan tags, eliminamos la entrada
            tags.pop(filename)
        save_tags(tags)

    return jsonify(success=True, tags=tags.get(filename, []))


# =========================
# PAPELERA
# =========================
@app.route("/restore/<filename>", methods=["POST"])
def restore(filename):
    if not require_admin():
        return jsonify(success=False, error="No autorizado"), 403
    
    filename = safe_filename(filename)
    src = os.path.join(TRASH_FOLDER, filename)
    dst = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(src):
        shutil.move(src, dst)
    
    return jsonify(success=True)


@app.route("/delete_permanent/<filename>", methods=["POST"])
def delete_permanent(filename):
    if not require_admin():
        return jsonify(success=False), 403
    
    filename = safe_filename(filename)
    path = os.path.join(TRASH_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    
    return jsonify(success=True)


@app.route("/trash")
def trash():
    if not require_admin():
        return redirect(url_for("login"))
    
    fotos = sorted([
        f for f in os.listdir(TRASH_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    return render_template("trash.html", fotos=fotos)   # ← Asegúrate de tener esta plantilla


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
