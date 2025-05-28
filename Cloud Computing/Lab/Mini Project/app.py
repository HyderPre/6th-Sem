from flask import Flask, render_template, request, redirect
from cryptography.fernet import Fernet
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'encrypted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🛡️ Load or generate encryption key
KEY_PATH = 'encryption_key.key'
if os.path.exists(KEY_PATH):
    with open(KEY_PATH, 'rb') as key_file:
        encryption_key = key_file.read()
else:
    encryption_key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(encryption_key)

fernet = Fernet(encryption_key)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_and_encrypt():
    file = request.files['file']
    if file.filename == '':
        return 'No file selected.'

    # 🔐 Load or create encryption key
    KEY_PATH = 'encryption_key.key'
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as key_file:
            encryption_key = key_file.read()
    else:
        encryption_key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as key_file:
            key_file.write(encryption_key)

    fernet = Fernet(encryption_key)

    # 🔒 Encrypt the file
    original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)

    encrypted_filename = f"encrypted_{file.filename}"
    encrypted_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)

    with open(encrypted_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    # ✅ Authenticate with Google Drive here (inside the route)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # ☁️ Upload encrypted file to Drive
    drive_file = drive.CreateFile({'title': encrypted_filename})
    drive_file.SetContentFile(encrypted_path)
    drive_file.Upload()

    return f'File "{file.filename}" encrypted and uploaded to Google Drive successfully.'

if __name__ == '__main__':
    app.run(debug=True)
