from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QComboBox, QDateTimeEdit, QGridLayout,QGroupBox,QListWidget,QRadioButton,QDateEdit
from PySide6.QtCore import QDateTime
from PySide6.QtCore import Qt

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

def create_place_order_section(window):
    # Grid Layout 1: Exchange Type, Product Type
    grid_layout1 = QGridLayout()
    exchange_code_label = QLabel("Exchange Type")
    exchange_code_input = QLineEdit("NFO")  # Default value
    product_label = QLabel("Product Type")
    product_input = QLineEdit("options")  # Default value
    product_input.setEnabled(False)  # Make it read-only
    exchange_code_input.setEnabled(False)  # Make it read-only
    grid_layout1.addWidget(exchange_code_label, 0, 0)
    grid_layout1.addWidget(exchange_code_input, 0, 1)
    grid_layout1.addWidget(product_label, 0, 2)
    grid_layout1.addWidget(product_input, 0, 3)
    grid_layout1.setColumnStretch(0, 0)
    grid_layout1.setColumnStretch(1, 0)
    grid_layout1.setColumnStretch(2, 0)
    grid_layout1.setColumnStretch(3, 0)
    grid_layout1.setColumnStretch(4, 1)

    # Grid Layout 2: Stock Code, Lot Size, Expiry Date, Strike Price
    query_layout = QGridLayout()
    trx_layout = QGridLayout()
    stock_code_input = QComboBox()
    expiry_date_input = QListWidget()
    lot_size_input = QLineEdit()
    quantity_input = QLineEdit()
    strike_price_input= QListWidget()
    group_box = QGroupBox("Select Derivative")  # Optional: Set a title for the group
    # Set a layout for the group box, which will be query_layout
    group_box.setLayout(query_layout)

    group_trx_box = QGroupBox("Transact Derivative")  # Optional: Set a title for the group
    # Set a layout for the group box, which will be query_layout
    group_trx_box.setLayout(trx_layout)

    # Optional: Customize the appearance of the group box
    group_box.setStyleSheet("""
        QGroupBox {
            border: 2px solid gray;
            border-radius: 5px;
            margin-top: 20px; /* Space between the title and the border */
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left; /* Title positioning */
            padding: 0 3px;
        }
    """)
    
    group_trx_box.setStyleSheet("""
        QGroupBox {
            border: 2px solid gray;
            border-radius: 5px;
            margin-top: 20px; /* Space between the title and the border */
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left; /* Title positioning */
            padding: 0 3px;
        }
    """)

    # Right Field as Radio Buttons in a Group Box
    right_group = QGroupBox("Right")
    right_layout = QHBoxLayout()
    call_radio = QRadioButton("Call")
    put_radio = QRadioButton("Put")
    right_layout.addWidget(call_radio)
    right_layout.addWidget(put_radio)
    right_group.setLayout(right_layout)
    right_group.setMaximumWidth(150)  # Set maximum width to reduce the size

    # Action Field as Radio Buttons in a Group Box
    action_group = QGroupBox("Action")
    action_layout = QHBoxLayout()
    buy_radio = QRadioButton("Buy")
    sell_radio = QRadioButton("Sell")
    spot_price=QLineEdit()
    price_input = QLineEdit()
    #best_bid_input=QLineEdit()
    #best_offer_input=QLineEdit()
    action_layout.addWidget(buy_radio)
    action_layout.addWidget(sell_radio)
    action_group.setLayout(action_layout)
    action_group.setMaximumWidth(150)  # Set maximum width to reduce the size


    query_layout.addWidget(QLabel("Stock Code"), 0, 0,Qt.AlignmentFlag.AlignTop)
    query_layout.addWidget(stock_code_input, 0, 1,Qt.AlignmentFlag.AlignTop)
    query_layout.addWidget(QLabel("Lot Size"), 0, 2,Qt.AlignmentFlag.AlignTop)
    lot_size_input.setEnabled(False)  # Read-only
    query_layout.addWidget(lot_size_input, 0, 3,Qt.AlignmentFlag.AlignTop)
    
    query_layout.addWidget(QLabel("Expiry Date"), 0, 4)
    expiry_date_input.setFixedWidth(100)  # Default height, adjust as needed
    if expiry_date_input.count() > 0:
        # Calculate size for at least one row
        item_height = expiry_date_input.sizeHintForRow(0)  # Safe to use sizeHintForRow(0) as it should exist
        expiry_date_input.setFixedHeight(item_height * 5 + 2 * expiry_date_input.frameWidth())  # Set the desired height
    else:
        # Fallback to a default height if there are no items
        expiry_date_input.setFixedHeight(100)  # Default height, adjust as needed
    #query_layout.setColumnMinimumWidth(5, 100)
    expiry_date_input.setStyleSheet("""
        QListWidget::item:selected {
            background-color: #ffcc00;  /* Yellow background for selected item */
            color: black;  /* Black text for selected item */
        }
    """)
    selected_expiry_date = QLineEdit()
    selected_expiry_date.setReadOnly(True)  # Make it read-only
    query_layout.addWidget(expiry_date_input, 0, 5)
    query_layout.addWidget(selected_expiry_date, 1, 5)
    #expiry_date_input.itemSelectionChanged.connect(window.update_selection_display)
    expiry_date_input.itemSelectionChanged.connect(lambda: window.update_selection_display(expiry_date_input, selected_expiry_date))
 
    
    query_layout.addWidget(QLabel("Strike Price"), 0, 6)
    strike_price_input.setFixedWidth(100)  # Default height, adjust as needed
    if strike_price_input.count() > 0:
        # Calculate size for at least one row
        item_height = strike_price_input.sizeHintForRow(0)  # Safe to use sizeHintForRow(0) as it should exist
        strike_price_input.setFixedHeight(item_height * 5 + 2 * expiry_date_input.frameWidth())  # Set the desired height
    else:
        # Fallback to a default height if there are no items
        strike_price_input.setFixedHeight(100)  # Default height, adjust as needed
    #query_layout.setColumnMinimumWidth(5, 100)
    strike_price_input.setStyleSheet("""
        QListWidget::item:selected {
            background-color: #ffcc00;  /* Yellow background for selected item */
            color: black;  /* Black text for selected item */
        }
    """)  
    
    selected_strike_price = QLineEdit()
    selected_strike_price.setReadOnly(True)  # Make it read-only
    query_layout.addWidget(selected_strike_price, 1, 7)
    strike_price_input.itemSelectionChanged.connect(lambda: window.update_selection_display(strike_price_input, selected_strike_price))
    
    query_layout.addWidget(strike_price_input, 0, 7)
    query_layout.addWidget(right_group, 1, 0)  # Right radio buttons group box
    query_layout.addWidget(action_group, 1, 1)  # Action radio buttons group box
    query_layout.addWidget(QLabel("Spot Price"), 1, 2)
    query_layout.addWidget(spot_price, 1, 3)
  

    # Grid Layout 3: Order Type, Price, StopLoss, Validity, Validity Date, Disclosed Quantity
 

    order_type_input = QComboBox()
    order_type_input.addItems(["Market", "Limit"])

    stoploss_input = QLineEdit()
    validity_input = QComboBox()
    validity_input.addItems(["Day", "IOC", "GTD"])
    validity_date_input = QDateEdit()
    validity_date_input.setCalendarPopup(True)
    validity_date_input.setDisplayFormat("yyyy-MM-dd")
    disclosed_quantity_input = QLineEdit()

    trx_layout.addWidget(QLabel("Price"), 0, 0)
    trx_layout.addWidget(price_input, 0, 1)
    trx_layout.addWidget(QLabel("Order Type"), 0, 2)
    trx_layout.addWidget(order_type_input, 0, 3)
    trx_layout.addWidget(QLabel("Quantity"), 0, 4)
    trx_layout.addWidget(quantity_input, 0, 5)
    trx_layout.addWidget(QLabel("StopLoss"), 0, 6)
    trx_layout.addWidget(stoploss_input, 0, 7)
    trx_layout.addWidget(QLabel("Validity"), 1, 0)
    trx_layout.addWidget(validity_input, 1, 1)
    trx_layout.addWidget(QLabel("Validity Date"), 1, 2)
    trx_layout.addWidget(validity_date_input, 1, 3)
    trx_layout.addWidget(QLabel("Disclosed Quantity"), 1, 4)
    trx_layout.addWidget(disclosed_quantity_input, 1, 5)
    trx_layout.setRowMinimumHeight=25

    # Connect signals to window's methods
    call_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'call', window) if checked else None)
    put_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'put', window) if checked else None)

    # Connecting the Buy/Sell radio buttons
    buy_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'buy', window) if checked else None)
    sell_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'sell', window) if checked else None)
        # Place Order Button
    place_order_button = QPushButton("Place Order")
    place_order_button.clicked.connect(lambda: window.place_order())

    # Add all grid layouts to the main layout
    place_order_section = QVBoxLayout()
    place_order_section.addLayout(grid_layout1)
    # place_order_section.addLayout(query_layout)
    place_order_section.addWidget(group_box)
    place_order_section.addWidget(group_trx_box)
    place_order_section.addWidget(place_order_button)
   
    # Return layout and inputs as a dictionary
    order_inputs = {
        'exchange_code': exchange_code_input,
        'product': product_input,
        'stock_code': stock_code_input,
        'strike_price': strike_price_input,
        'expiry_date': expiry_date_input,
        'spot_price':spot_price,
        'right': 'call' if call_radio.isChecked() else 'put',
        'action': 'buy' if buy_radio.isChecked() else 'sell',
        'quantity': quantity_input,
        'lot_size': lot_size_input,
        'order_type': order_type_input,
        'price': price_input,
        'stoploss': stoploss_input,
        'validity': validity_input,
        'validity_date': validity_date_input,
        'disclosed_quantity': disclosed_quantity_input
    }
    
    return place_order_section,  order_inputs

def create_positions_table(window):
    positions_table = QTableWidget(0, 25)
    positions_table.setHorizontalHeaderLabels(['Square Off', 'Calculated P&L', 'BEP', 'Spot Price', 'stock_code', 'expiry_date', 'strike_price', 'right', 'action', 'quantity', 'average_price', 'ltp', 'price', 'Total Cost', 'stock_index_indicator', 'cover_quantity', 'Current Value', 'stoploss_trigger', 'stoploss', 'take_profit', 'available_margin', 'squareoff_mode', 'order_id', 'pledge_status', 'pnl', 'underlying', 'settlement_id', 'segment'])
    
     # Refresh Button
    refresh_button = QPushButton("Refresh Positions")
    refresh_button.clicked.connect(window.refresh_positions)

    return positions_table, refresh_button

def handle_radio_toggle(checked, value, window):
    """
    Handles the toggling of both Call/Put and Buy/Sell radio buttons.
    
    Parameters:
        checked (bool): Whether the radio button was toggled on or off.
        value (str): The value associated with the radio button ('call', 'put', 'buy', or 'sell').
        window: The main window or the class instance that contains order_inputs.
    """
    # Only handle the toggle if 'checked' is True (i.e., the button is toggled on)
    if not checked:
        return

    # Handle Call/Put radio buttons (Right)
    if value in ['call', 'put']:
        window.order_inputs['right'] = value
        print(f"Right Option Selected: {value}")

    # Handle Buy/Sell radio buttons (Action)
    if value in ['buy', 'sell']:
        window.order_inputs['action'] = value
        print(f"Action Selected: {value}")
    window.auto_populate_price()
