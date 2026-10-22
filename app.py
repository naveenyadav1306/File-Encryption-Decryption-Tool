
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    import base64
    return base64.urlsafe_b64encode(
        kdf.derive(password.encode("utf-8"))
    )


def encrypt_file():
    password = password_entry.get()

    if len(password) < 8:
        messagebox.showerror(
            "Invalid Password",
            "Password must contain at least 8 characters."
        )
        return

    file_path = filedialog.askopenfilename(
        title="Select a file to encrypt"
    )
    if not file_path:
        return

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        salt = os.urandom(16)
        key = derive_key(password, salt)
        encrypted_data = Fernet(key).encrypt(data)

        output_path = file_path + ".enc"
        with open(output_path, "wb") as file:
            file.write(salt + encrypted_data)

        messagebox.showinfo(
            "Success",
            f"File encrypted successfully!\n\nSaved to:\n{output_path}"
        )

    except OSError as error:
        messagebox.showerror("File Error", str(error))
    except Exception as error:
        messagebox.showerror("Encryption Error", str(error))


def decrypt_file():
    password = password_entry.get()

    if len(password) < 8:
        messagebox.showerror(
            "Invalid Password",
            "Password must contain at least 8 characters."
        )
        return

    file_path = filedialog.askopenfilename(
        title="Select an encrypted .enc file",
        filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        if len(data) <= 16:
            raise ValueError("The selected file is empty or invalid.")

        salt = data[:16]
        encrypted_data = data[16:]
        key = derive_key(password, salt)
        decrypted_data = Fernet(key).decrypt(encrypted_data)

        original_name = os.path.basename(file_path)
        if original_name.endswith(".enc"):
            original_name = original_name[:-4]

        output_path = os.path.join(
            os.path.dirname(file_path),
            "decrypted_" + original_name
        )

        with open(output_path, "wb") as file:
            file.write(decrypted_data)

        messagebox.showinfo(
            "Success",
            f"File decrypted successfully!\n\nSaved to:\n{output_path}"
        )

    except InvalidToken:
        messagebox.showerror(
            "Decryption Failed",
            "Wrong password or damaged encrypted file."
        )
    except (OSError, ValueError) as error:
        messagebox.showerror("File Error", str(error))
    except Exception as error:
        messagebox.showerror("Decryption Error", str(error))


def clear_password():
    password_entry.delete(0, tk.END)


root = tk.Tk()
root.title("File Encryption & Decryption Tool")
root.geometry("600x440")
root.minsize(500, 400)
root.configure(bg="#101827")

title = tk.Label(
    root,
    text="FILE ENCRYPTION TOOL",
    font=("Segoe UI", 20, "bold"),
    fg="#38BDF8",
    bg="#101827"
)
title.pack(pady=(28, 8))

subtitle = tk.Label(
    root,
    text="Protect your files with password-based encryption",
    font=("Segoe UI", 10),
    fg="#CBD5E1",
    bg="#101827"
)
subtitle.pack(pady=(0, 24))

password_label = tk.Label(
    root,
    text="Enter password (minimum 8 characters)",
    font=("Segoe UI", 10),
    fg="white",
    bg="#101827"
)
password_label.pack(pady=(0, 8))

password_entry = tk.Entry(
    root,
    show="*",
    font=("Segoe UI", 12),
    width=32,
    relief="flat",
    bg="#1E293B",
    fg="white",
    insertbackground="white"
)
password_entry.pack(ipady=9, pady=(0, 18))

encrypt_button = tk.Button(
    root,
    text="Encrypt File",
    command=encrypt_file,
    font=("Segoe UI", 11, "bold"),
    bg="#0284C7",
    fg="white",
    activebackground="#0369A1",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=24,
    pady=9
)
encrypt_button.pack(pady=7)

decrypt_button = tk.Button(
    root,
    text="Decrypt File",
    command=decrypt_file,
    font=("Segoe UI", 11, "bold"),
    bg="#0F766E",
    fg="white",
    activebackground="#115E59",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=24,
    pady=9
)
decrypt_button.pack(pady=7)

clear_button = tk.Button(
    root,
    text="Clear Password",
    command=clear_password,
    font=("Segoe UI", 10),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=24,
    pady=7
)
clear_button.pack(pady=7)

footer = tk.Label(
    root,
    text="Encryption: Fernet + PBKDF2-HMAC-SHA256",
    font=("Segoe UI", 9),
    fg="#94A3B8",
    bg="#101827"
)
footer.pack(side="bottom", pady=16)

root.mainloop()
