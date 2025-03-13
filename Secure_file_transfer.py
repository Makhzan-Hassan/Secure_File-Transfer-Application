import os
import json
import hashlib
from cryptography.fernet import Fernet

audit_log = "audit_log.json"


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved.")


def load_key():
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        generate_key()
        return open("secret.key", "rb").read()


def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)
    hash_value = hashlib.sha256(file_data).hexdigest()
    log_transfer(filename, hash_value, "Encrypted")
    print(f"File '{filename}' encrypted successfully.")


def decrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    original_filename = filename.replace(".enc", "")
    with open(original_filename, "wb") as file:
        file.write(decrypted_data)
    hash_value = hashlib.sha256(decrypted_data).hexdigest()
    log_transfer(original_filename, hash_value, "Decrypted")
    print(f"File '{original_filename}' decrypted successfully.")


def log_transfer(filename, hash_value, action):
    log_entry = {"filename": filename, "hash": hash_value, "action": action}
    logs = []
    if os.path.exists(audit_log):
        with open(audit_log, "r") as log_file:
            logs = json.load(log_file)
    logs.append(log_entry)
    with open(audit_log, "w") as log_file:
        json.dump(logs, log_file, indent=4)


def access_control():
    correct_password = "secure123"
    password = input("Enter access password: ")
    if password != correct_password:
        print("Access Denied!")
        exit()
    print("Access Granted!")


def main():
    print("Script is running...")
    access_control()
    key = load_key()

    while True:
        print("\nSecure File Transfer Application")
        print("1. Encrypt File")
        print("2. Decrypt File")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            filename = input("Enter file name to encrypt: ")
            if os.path.exists(filename):
                encrypt_file(filename, key)
            else:
                print("File not found!")
        elif choice == "2":
            filename = input("Enter file name to decrypt: ")
            if os.path.exists(filename):
                decrypt_file(filename, key)
            else:
                print("File not found!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
