
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton

def create_credentials_section(window):
    credentials_layout = QHBoxLayout()

    # API Key
    api_key_input = QLineEdit()
    api_key_input.setEchoMode(QLineEdit.Password)
    credentials_layout.addWidget(QLabel("API Key"))
    credentials_layout.addWidget(api_key_input)

    # API Secret
    api_secret_input = QLineEdit()
    api_secret_input.setEchoMode(QLineEdit.Password)
    credentials_layout.addWidget(QLabel("API Secret"))
    credentials_layout.addWidget(api_secret_input)

    # Session Token
    session_token_input = QLineEdit()
    session_token_input.setEchoMode(QLineEdit.Password)
    credentials_layout.addWidget(QLabel("Session Token"))
    credentials_layout.addWidget(session_token_input)

    # Login Button
    login_button = QPushButton("Login")
    login_button.clicked.connect(window.login)
    credentials_layout.addWidget(login_button)

    return credentials_layout, {'api_key': api_key_input, 'api_secret': api_secret_input, 'session_token': session_token_input}
