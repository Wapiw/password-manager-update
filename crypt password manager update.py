from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.fernet import Fernet
import json

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Load the key from a file
def load_key():
    try:
        with open('key.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print("Key file not found. Generate a new key.")
        return None

# Save the key to a file
def save_key(key):
    with open('key.key', 'wb') as file:
        file.write(key)

# Encrypt a message using the key
def encrypt_message(key, message):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Decrypt a message using the key
def decrypt_message(key, encrypted_message):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# Store the passwords in a JSON file
def store_passwords(passwords, key):
    encrypted_passwords = encrypt_message(key, json.dumps(passwords))
    with open('passwords.json', 'wb') as file:
        file.write(encrypted_passwords)

# Retrieve the passwords from the JSON file
def retrieve_passwords(key):
    try:
        with open('passwords.json', 'rb') as file:
            encrypted_passwords = file.read()
            return json.loads(decrypt_message(key, encrypted_passwords))
    except FileNotFoundError:
        print("Password file not found.")
        return {}

# Main password manager function
def password_manager():
    print("Password Manager")

    # Load or generate the encryption key
    key = load_key()
    if key is None:
        key = generate_key()
        save_key(key)

    while True:
        print("\nOptions:")
        print("1. Store password")
        print("2. Retrieve password")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            website = input("Enter the website or application: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # Retrieve existing passwords
            passwords = retrieve_passwords(key)
            passwords[website] = {'username': username, 'password': password}

            # Store the updated passwords
            store_passwords(passwords, key)
            print("Password stored successfully!")

        elif choice == '2':
            website = input("Enter the website or application: ")

            # Retrieve existing passwords
            passwords = retrieve_passwords(key)

            if website in passwords:
                print("Username:", passwords[website]['username'])
                print("Password:", passwords[website]['password'])
            else:
                print("No password found for the specified website.")

        elif choice == '3':
            print("Exiting the password manager...")
            break

        else:
            print("Invalid input. Please try again.")

# Run the password manager
password_manager()

