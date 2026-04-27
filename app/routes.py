from flask import Blueprint, render_template, request, send_file
from app.stego_utils import embedding, extraction
from app.crypto_utils import blowfish_decrypt
import os
main = Blueprint("main", __name__)

# ---------- ENCRYPT ----------
@main.route("/", methods=["GET","POST"])
def encrypt_page():
    if request.method == "POST":
        os.makedirs("app/static", exist_ok=True)

        video = request.files["video"]
        message = request.form["message"]
        key = request.form["key"]

        input_path = "app/static/input_encrypt.mp4"
        video.save(input_path)
        
        embedding(input_path, message, key)

        return '''
        <h2>Encryption Successful</h2>
        <a href="/download"><button>Download Stego Video</button></a>
        <br><br>
        <a href="/decrypt">Go to Decryption</a>
        '''

    return render_template("encrypt.html")

# ---------- DECRYPT ----------
@main.route("/decrypt", methods=["GET","POST"])
def decrypt_page():

    if request.method == "POST":

        video = request.files["video"]
        key = request.form["key"]

        path = "app/static/uploaded_stego.avi"
        video.save(path)

        encrypted = extraction(path)
        message = blowfish_decrypt(encrypted, key)

        return render_template("result.html",
                               decrypted_message=message)

    return render_template("decrypt.html")

@main.route("/download")
def download():
    return send_file(
        "static/stego_video.avi",
        as_attachment=True
    )


