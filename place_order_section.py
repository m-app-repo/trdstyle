from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QGridLayout, QGroupBox, QListWidget, QRadioButton
from PySide6.QtCore import Qt
from handle_radio_toggle import handle_radio_toggle



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
    strike_price_input = QListWidget()
    group_box = QGroupBox("Select Derivative")  # Optional: Set a title for the group
    group_box.setLayout(query_layout)

    group_trx_box = QGroupBox("Transact Derivative")  # Optional: Set a title for the group
    group_trx_box.setLayout(trx_layout)

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
    spot_price = QLineEdit()
    price_input = QLineEdit()
    action_layout.addWidget(buy_radio)
    action_layout.addWidget(sell_radio)
    action_group.setLayout(action_layout)
    action_group.setMaximumWidth(150)  # Set maximum width to reduce the size

    query_layout.addWidget(QLabel("Stock Code"), 0, 0, Qt.AlignmentFlag.AlignTop)
    query_layout.addWidget(stock_code_input, 0, 1, Qt.AlignmentFlag.AlignTop)
    query_layout.addWidget(QLabel("Lot Size"), 0, 2, Qt.AlignmentFlag.AlignTop)
    lot_size_input.setEnabled(False)  # Read-only
    query_layout.addWidget(lot_size_input, 0, 3, Qt.AlignmentFlag.AlignTop)
    
    query_layout.addWidget(QLabel("Expiry Date"), 0, 4)
    expiry_date_input.setFixedWidth(100)  # Default height, adjust as needed
    if expiry_date_input.count() > 0:
        item_height = expiry_date_input.sizeHintForRow(0)  # Safe to use sizeHintForRow(0) as it should exist
        expiry_date_input.setFixedHeight(item_height * 5 + 2 * expiry_date_input.frameWidth())  # Set the desired height
    else:
        expiry_date_input.setFixedHeight(100)  # Default height, adjust as needed
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
    expiry_date_input.itemSelectionChanged.connect(lambda: window.update_selection_display(expiry_date_input, selected_expiry_date))
 
    query_layout.addWidget(QLabel("Strike Price"), 0, 6)
    strike_price_input.setFixedWidth(100)
    if strike_price_input.count() > 0:
        item_height = strike_price_input.sizeHintForRow(0)
        strike_price_input.setFixedHeight(item_height * 5 + 2 * expiry_date_input.frameWidth())
    else:
        strike_price_input.setFixedHeight(100)
    strike_price_input.setStyleSheet("""
        QListWidget::item:selected {
            background-color: #ffcc00;
            color: black;
        }
    """)  
    
    selected_strike_price = QLineEdit()
    selected_strike_price.setReadOnly(True)
    query_layout.addWidget(strike_price_input, 0, 7)
    query_layout.addWidget(selected_strike_price, 1, 7)
    strike_price_input.itemSelectionChanged.connect(lambda: window.update_selection_display(strike_price_input, selected_strike_price))
    
    query_layout.addWidget(right_group, 1, 0)
    query_layout.addWidget(action_group, 1, 1)
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
    trx_layout.setRowMinimumHeight = 25

    call_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'call', window) if checked else None)
    put_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'put', window) if checked else None)

    buy_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'buy', window) if checked else None)
    sell_radio.toggled.connect(lambda checked: handle_radio_toggle(checked, 'sell', window) if checked else None)
    place_order_button = QPushButton("Place Order")
    place_order_button.clicked.connect(lambda: window.place_order())

    place_order_section = QVBoxLayout()
    place_order_section.addLayout(grid_layout1)
    place_order_section.addWidget(group_box)
    place_order_section.addWidget(group_trx_box)
    place_order_section.addWidget(place_order_button)
   
    order_inputs = {
        'exchange_code': exchange_code_input,
        'product': product_input,
        'stock_code': stock_code_input,
        'strike_price': strike_price_input,
        'expiry_date': expiry_date_input,
        'spot_price': spot_price,
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
    
    return place_order_section, order_inputs