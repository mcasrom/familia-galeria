import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "familia-secreta-2026")

# ── Rutas absolutas ────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR  = os.path.join(BASE_DIR, "static", "images")
TAGS_FILE   = os.path.join(BASE_DIR, "data", "tags.json")

# ── Usuarios ───────────────────────────────────────────────────────────────────
USERS = {
    os.environ.get("ADMIN_USER", "admin"):  {"password": os.environ.get("ADMIN_PASS", "admin123"), "role": "admin"},
    os.environ.get("FAMILY_USER", "Family"): {"password": os.environ.get("FAMILY_PASS", "4321"),    "role": "viewer"},
}

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}

# ── Helpers ────────────────────────────────────────────────────────────────────
def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def load_tags():
    if os.path.exists(TAGS_FILE):
        try:
            return json.loads(open(TAGS_FILE).read())
        except Exception:
            pass
    return {}

def save_tags(tags):
    os.makedirs(os.path.dirname(TAGS_FILE), exist_ok=True)
    open(TAGS_FILE, "w").write(json.dumps(tags, ensure_ascii=False, indent=2))

def get_images():
    if not os.path.exists(IMAGES_DIR):
        return []
    exts = ALLOWED_EXT
    files = sorted([
        f for f in os.listdir(IMAGES_DIR)
        if f.rsplit(".", 1)[-1].lower() in exts
    ])
    return files

def is_admin():
    return session.get("role") == "admin"

def logged_in():
    return "user" in session

# ── Rutas ──────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if not logged_in():
        return redirect(url_for("login"))
    return redirect(url_for("gallery"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pwd  = request.form.get("password", "")
        if user in USERS and USERS[user]["password"] == pwd:
            session["user"] = user
            session["role"] = USERS[user]["role"]
            return redirect(url_for("gallery"))
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/gallery")
def gallery():
    if not logged_in():
        return redirect(url_for("login"))
    images = get_images()
    tags   = load_tags()
    return render_template("gallery.html",
                           images=images,
                           tags=tags,
                           is_admin=is_admin(),
                           username=session.get("user"))

# ── API tags ───────────────────────────────────────────────────────────────────
@app.route("/api/tags", methods=["GET"])
def api_tags_get():
    return jsonify(load_tags())

@app.route("/api/tags", methods=["POST"])
def api_tags_save():
    if not logged_in():
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({"error": "bad data"}), 400
    save_tags(data)
    return jsonify({"status": "ok"})

# ── Upload (solo admin, solo en local/Odroid) ──────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    if not is_admin():
        flash("Solo el administrador puede subir fotos", "error")
        return redirect(url_for("gallery"))
    f = request.files.get("file")
    if not f or f.filename == "":
        flash("No se seleccionó ningún archivo", "error")
        return redirect(url_for("gallery"))
    if not allowed(f.filename):
        flash("Formato no permitido (jpg, jpeg, png, webp)", "error")
        return redirect(url_for("gallery"))
    filename = secure_filename(f.filename)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    f.save(os.path.join(IMAGES_DIR, filename))
    flash(f"Foto '{filename}' subida correctamente", "ok")
    return redirect(url_for("gallery"))

# ── Delete (solo admin) ────────────────────────────────────────────────────────
@app.route("/delete/<filename>", methods=["POST"])
def delete_photo(filename):
    if not is_admin():
        return jsonify({"error": "unauthorized"}), 403
    path = os.path.join(IMAGES_DIR, secure_filename(filename))
    if os.path.exists(path):
        os.remove(path)
        tags = load_tags()
        tags.pop(filename, None)
        save_tags(tags)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
