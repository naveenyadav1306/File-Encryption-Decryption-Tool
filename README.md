# 🔐 File Encryption & Decryption Tool

A web-based application that allows users to encrypt and decrypt files using password-based cryptography. Built with Python Flask, this project demonstrates file security, cryptographic key derivation, and secure file handling.

## 🚀 Live Demo

**Try the application:** https://file-encryption-decryption-tool-vwj1.onrender.com

**GitHub Repository:** https://github.com/naveenyadav1306/File-Encryption-Decryption-Tool

## ✨ Features

- **File Encryption:** Encrypt files using a password.
- **File Decryption:** Restore encrypted files using the correct password.
- **Password Protection:** Requires a password of at least 8 characters.
- **Cryptographic Security:** Uses the Fernet encryption scheme and PBKDF2HMAC for key derivation.
- **File Downloads:** Download encrypted and decrypted files directly through the browser.
- **Responsive Interface:** Designed for use on desktop and mobile screens.
- **File Size Limit:** Supports uploads up to 16 MB.

## 🛠️ Technologies Used

- Python
- Flask
- Cryptography
- Waitress
- HTML5
- CSS3
- Git and GitHub
- Render

## ⚙️ Run Locally

### Prerequisites

- Python 3
- Git
- A code editor such as Visual Studio Code

### 1. Clone the repository

```bash
git clone https://github.com/naveenyadav1306/File-Encryption-Decryption-Tool.git
```

### 2. Open the project directory

```bash
cd File-Encryption-Decryption-Tool
```

### 3. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Start the application

```bash
python web_app.py
```

### 7. Open in your browser

Visit:

http://127.0.0.1:5000

## 📖 How to Use

1. Open the live application or run it locally.
2. Select the file you want to process.
3. Enter a password containing at least 8 characters.
4. Choose **Encrypt File** to encrypt the file.
5. Download the encrypted output.
6. To restore the original file, upload the encrypted file and enter the same password.
7. Choose **Decrypt File** and download the restored file.

**Important:** Keep your password safe. If you lose it, you may not be able to recover your encrypted file.

## 🔒 Security Notes

- The application uses password-derived encryption keys.
- Decryption requires the correct password and valid encrypted data.
- Use a unique, strong password for each important file.
- This is an educational project and has not been independently security-audited.
- Avoid uploading confidential or sensitive files to the public demo.

## 📂 Project Structure

```text
File-Encryption-Decryption-Tool/
├── app.py
├── app_desktop_backup.py
├── web_app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── README.md
└── templates/
    └── index.html
```

## 🎯 Project Objective

The goal of this project is to demonstrate the practical use of cryptography in a web application, including password-based key derivation, file encryption and decryption, and deployment of a Python application.

## 👨‍💻 Author

**Naveen Yadav**

- GitHub: https://github.com/naveenyadav1306

---

If you find this project useful for learning, feel free to explore the source code and experiment with it using non-sensitive sample files.