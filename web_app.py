
import os
import io
import secrets
from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)

# Maximum uploaded file size: 16 MB
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

SALT_SIZE = 16
ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from the password and salt."""
    import base64

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_file():
    uploaded_file = request.files.get("file")
    password = request.form.get("password", "")
    action = request.form.get("action", "")

    if not uploaded_file or not uploaded_file.filename:
        return "Please select a file.", 400

    if len(password) < 8:
        return "Password must be at least 8 characters long.", 400

    if action not in ("encrypt", "decrypt"):
        return "Invalid action.", 400

    original_name = os.path.basename(uploaded_file.filename)
    file_data = uploaded_file.read()

    try:
        if action == "encrypt":
            salt = secrets.token_bytes(SALT_SIZE)
            key = derive_key(password, salt)
            encrypted_data = salt + Fernet(key).encrypt(file_data)
            output_data = encrypted_data
            output_name = original_name + ".enc"

        else:
            if len(file_data) <= SALT_SIZE:
                return "Invalid encrypted file.", 400

            salt = file_data[:SALT_SIZE]
            encrypted_payload = file_data[SALT_SIZE:]
            key = derive_key(password, salt)
            output_data = Fernet(key).decrypt(encrypted_payload)

            if original_name.endswith(".enc"):
                output_name = original_name[:-4] or "decrypted_file"
            else:
                output_name = "decrypted_" + original_name

    except InvalidToken:
        return (
            "Decryption failed. The password may be incorrect, "
            "or the file may be damaged.",
            400,
        )
    except Exception:
        app.logger.exception("File processing failed")
        return "Unable to process this file.", 400

    return send_file(
        io.BytesIO(output_data),
        as_attachment=True,
        download_name=output_name,
        mimetype="application/octet-stream",
    )


@app.errorhandler(413)
def file_too_large(_error):
    return "File is too large. Maximum allowed size is 16 MB.", 413


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
