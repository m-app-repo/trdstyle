from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton

def create_credentials_section(window):
    # Create layout and input fields for API credentials
    layout = QVBoxLayout()
    api_key_label = QLabel("API Key")
    api_key_input = QLineEdit()
    api_secret_label = QLabel("API Secret")
    api_secret_input = QLineEdit()
    session_token_label = QLabel("Session Token")
    session_token_input = QLineEdit()

    # Add widgets to the layout
    layout.addWidget(api_key_label)
    layout.addWidget(api_key_input)
    layout.addWidget(api_secret_label)
    layout.addWidget(api_secret_input)
    layout.addWidget(session_token_label)
    layout.addWidget(session_token_input)

    # Add login button
    login_button = QPushButton("Login")
    login_button.clicked.connect(lambda: window.login())
    layout.addWidget(login_button)

    # Store inputs in a dictionary for easy access
    api_inputs = {
        'api_key': api_key_input,
        'api_secret': api_secret_input,
        'session_token': session_token_input
    }

    return layout, api_inputs

def create_positions_table(window):
    from PySide6.QtWidgets import QTableWidget, QPushButton

    # Create positions table and refresh button
    positions_table = QTableWidget()
    refresh_button = QPushButton("Refresh Positions")
    refresh_button.clicked.connect(lambda: window.refresh_positions())

    return positions_table, refresh_button

def create_place_order_section(window):
    from place_order_section import create_place_order_section
    return create_place_order_section(window)
