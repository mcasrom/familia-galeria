from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def register_upload(app, UPLOAD_FOLDER):

    @app.route("/upload", methods=["POST"])
    def upload():
        if "file" not in request.files:
            return redirect(url_for("gallery"))

        file = request.files["file"]
        if file.filename == "":
            return redirect(url_for("gallery"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        return redirect(url_for("gallery"))
