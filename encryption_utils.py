import platform
import uuid
from hashlib import sha256
from cryptography.fernet import Fernet
from getmac import get_mac_address
from base64 import urlsafe_b64encode
from configparser import ConfigParser
import logging
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pad_token(token):
    if isinstance(token, str):
        token = token.encode('utf-8')
    padded_token = token + b'=' * (4 - len(token) % 4)
    logging.info("Padded token: %s", padded_token)
    return padded_token

def get_system_identifier():
    # Collect system-specific information
    mac_address = get_mac_address()
    system_name = platform.system()
    processor = platform.processor()
    machine_id = uuid.getnode()
    # Create a combined string of system information
    system_info = f"{mac_address}{system_name}{processor}{machine_id}"
    return system_info

def create_encryption_key(user_input):
    try:
        # Combine system info with user input and hash them
        system_info = get_system_identifier()
        if isinstance(user_input, bytes):
            user_input = user_input.decode('utf-8')
        if system_info is None:
            system_info = ""
        if user_input is None:
            user_input = ""
        combined_info = (system_info + user_input).encode()
        hashed_info = sha256(combined_info).digest()
        # Encode the hashed info to create a valid Fernet key
        fernet_key = urlsafe_b64encode(hashed_info)
        return fernet_key
    except Exception as e:
        logging.error("Error occurred during key creation: %s", str(e), exc_info=True)
        return None

def encrypt_data(data, passphrase):
    try:
        key = create_encryption_key(passphrase)
        fernet = Fernet(key)
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        encrypted_data = fernet.encrypt(data)
        return encrypted_data
    except Exception as e:
        logging.error("Error occurred during encryption: %s", str(e), exc_info=True)
        return None

def decrypt_data(encrypted_data, passphrase):
    try:
        logging.info("Encrypted data: %s", encrypted_data)
        key = create_encryption_key(passphrase)
        fernet = Fernet(key)
        if not isinstance(encrypted_data, bytes):
            encrypted_data = encrypted_data.encode('utf-8')
        decrypted_data = fernet.decrypt(pad_token(encrypted_data))
        logging.info("Decrypted data: %s", decrypted_data)
        return decrypted_data
    except Exception as e:
        logging.error("Error occurred during decryption: %s", str(e))
        return None

class EncryptionApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encryption Utility")
        self.setGeometry(100, 100, 400, 300)

        # Layout for the dialog
        layout = QVBoxLayout()

        # Passphrase input
        self.passphrase_label = QLabel("Enter Passphrase:")
        self.passphrase_input = QLineEdit()
        self.passphrase_input.setEchoMode(QLineEdit.Password)

        # API Key input
        self.api_key_label = QLabel("Enter API Key:")
        self.api_key_input = QLineEdit()

        # API Secret input
        self.api_secret_label = QLabel("Enter API Secret:")
        self.api_secret_input = QLineEdit()

        # Generate Config button
        self.generate_button = QPushButton("Generate Config File")
        self.generate_button.clicked.connect(self.generate_config_file)

        # Add widgets to layout
        layout.addWidget(self.passphrase_label)
        layout.addWidget(self.passphrase_input)
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(self.api_secret_label)
        layout.addWidget(self.api_secret_input)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_config_file(self):
        passphrase = self.passphrase_input.text()
        api_key = self.api_key_input.text()
        api_secret = self.api_secret_input.text()

        if not passphrase or not api_key or not api_secret:
            logging.error("Passphrase, API Key, and API Secret must all be provided.")
            return

        # Encrypt API Key and API Secret
        encrypted_api_key = encrypt_data(api_key, passphrase)
        encrypted_api_secret = encrypt_data(api_secret, passphrase)

        if not encrypted_api_key or not encrypted_api_secret:
            logging.error("Failed to encrypt API Key or API Secret.")
            return

        # Write encrypted credentials to config.ini
        config = ConfigParser()
        config['Credentials'] = {
            'api_key': encrypted_api_key.decode('utf-8'),
            'api_secret': encrypted_api_secret.decode('utf-8')
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        logging.info("Configuration file 'config.ini' generated successfully.")
        self.accept()  # Close the dialog after successful operation

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and display the encryption dialog
    encryption_app = EncryptionApp()
    encryption_app.exec()
