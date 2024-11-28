import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QComboBox, QDateEdit, QListWidget,QRadioButton
from ui_components import create_credentials_section, create_positions_table, create_place_order_section
from breeze_api import BreezeAPI
from logger import Logger
from stock_code_operations import StockCodeOperations
from position_management import PositionManagement
from order_operations import OrderOperations

class TradingPlatform(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trading Platform - v1.1")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize BreezeAPI and Logger
        self.logger = Logger()
        self.breeze_api = BreezeAPI(logger=self.logger)

        # Initialize empty order_inputs dictionary
        self.order_inputs = {}

        # Initialize log_book early
        self.log_book = QTextEdit()
        self.log_book.setReadOnly(True)

        self.csv_data = self.load_csv_data()
        # Create UI components
        self.create_ui()
        self.populate_stock_codes()

        # Initialize trading logic
        self.stock_operations = StockCodeOperations(self.breeze_api, self.logger, self.order_inputs, self.log_book)
        self.position_management = PositionManagement(self.breeze_api, self.logger, self.positions_table, self.order_inputs, self.log_book)
        self.order_operations = OrderOperations(self.breeze_api, self.logger, self.order_inputs, self.log_book)
    
    def create_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Credentials Section
        self.credentials_section, self.api_inputs = create_credentials_section(self)
        main_layout.addLayout(self.credentials_section)

        # Open Positions Section
        self.positions_table, self.refresh_button = create_positions_table(self)
        main_layout.addWidget(self.refresh_button)
        main_layout.addWidget(self.positions_table)

        # Place Order Section
        self.place_order_section, order_inputs = create_place_order_section(self)
        self.order_inputs.update(order_inputs)  # Store inputs in self.order_inputs
        main_layout.addLayout(self.place_order_section)

        # Log Book Section (already initialized in __init__)
        main_layout.addWidget(self.log_book)

        # Set the main layout
        self.setLayout(main_layout)
    
    def load_csv_data(self):
        """Loads CSV data from the FONSEScripMaster.txt file."""
        try:
            # Load the CSV data into a pandas dataframe
            df = pd.read_csv("FONSEScripMaster.txt", delimiter=",")  # Adjust the delimiter if needed
            return df
        except FileNotFoundError:
            print("FONSEScripMaster.txt file not found.")
            return pd.DataFrame()
    
    def populate_stock_codes(self):
        """Populates the stock_code combo box with unique exchangecode values."""
        unique_stock_codes = self.csv_data["ShortName"].unique()
        self.order_inputs['stock_code'].addItems(unique_stock_codes)

        # Connect stock_code selection to field population
        self.order_inputs['stock_code'].currentTextChanged.connect(self.on_stock_code_selected)
    
    def on_stock_code_selected(self, selected_stock_code):
        """Populates StrikePrice, ExpiryDate, Right (radio buttons), and Lot Size when a stock code is selected."""
        self.stock_operations.populate_stock_code_details(self.csv_data, selected_stock_code)
    
    def auto_populate_price(self):
        """Automatically populates the price based on selected inputs by fetching data from Breeze API."""
        print("Auto-populate price function called.")

        # Prepare the request data for the API
        premium_data = {}
        for key, input_field in self.order_inputs.items():
            print(f"Processing input: {key}, Type: {type(input_field)}")
            
            if isinstance(input_field, QLineEdit):
                premium_data[key] = input_field.text()
            elif isinstance(input_field, QComboBox):
                premium_data[key] = input_field.currentText()
            elif isinstance(input_field, QDateEdit):
                date_value = input_field.date().toString("yyyy-MM-dd") + "T06:00:00.000Z"
                premium_data[key] = date_value
            elif isinstance(input_field, QListWidget):  # Handling QListWidget for strike_price and expiry_date
                selected_items = input_field.selectedItems()
                if selected_items:
                    premium_data[key] = selected_items[0].text()
                else:
                    premium_data[key] = None  # If nothing is selected, assign None or a default value
            elif key == 'right':  # Handling the 'right' field using radio buttons
                premium_data[key] = 'call' if self.order_inputs['call_radio'].isChecked() else 'put'
                print(f"Radio Button for 'right' selected: {premium_data[key]}")
            elif key == 'action':  # Handling the 'action' field using radio buttons
                premium_data[key] = 'buy' if self.order_inputs['buy_radio'].isChecked() else 'sell'
                print(f"Radio Button for 'action' selected: {premium_data[key]}")
            elif isinstance(input_field, QRadioButton):
                # Skip adding QRadioButton instances to premium_data
                continue
            else:
                print(f"Unhandled input type: {key} -> {input_field}, Type: {type(input_field)}")

        # Create price request data
        print("Collected premium data:", premium_data)
        price_request_data = {
            "stock_code": premium_data['stock_code'],
            "exchange_code": premium_data['exchange_code'],
            "expiry_date": premium_data['expiry_date'],
            "product_type": premium_data['product'],
            "right": premium_data['right'],
            "strike_price": premium_data['strike_price'],
            "action": premium_data['action']
        }

        try:
            # Fetch the latest price using the Breeze API
            quotes_response = self.breeze_api.get_quotes(
                stock_code=premium_data['stock_code'],
                exchange_code=premium_data['exchange_code'],
                expiry_date=premium_data['expiry_date'],
                product_type=premium_data['product'],
                right=premium_data['right'],
                strike_price=premium_data['strike_price']
            )

            # Log the price response
            self.log_activity("Price Response", request=price_request_data, response=quotes_response)

            # Extract the price from the response and update the price field
            if quotes_response and "Success" in quotes_response and quotes_response["Success"]:
                # Ensure that 'ltp' (last traded price) is available and set the price field
                if premium_data['action'] == 'buy':
                    latest_price = quotes_response["Success"][0].get("best_offer_price", "0.00")
                else:
                    latest_price = quotes_response["Success"][0].get("best_bid_price", "0.00")

                # Ensure that 'ltp' is a valid number before setting it
                if latest_price and latest_price != "None":
                    self.order_inputs['price'].setText(str(latest_price))
                    self.order_inputs['stoploss'].setText(str(float(latest_price) - 5))
                else:
                    self.order_inputs['price'].setText("0.00")
            else:
                # Set default price if API fails or returns no price
                self.order_inputs['price'].setText("0.00")
                error_message = quotes_response.get('Error', 'Unknown error') if quotes_response else 'No response'
                self.log_activity("Error fetching price:", error_message)
                print("Error fetching price:", error_message)

        except Exception as e:
            # Handle any unexpected exceptions during the API call
            self.order_inputs['price'].setText("0.00")
            self.log_activity("Error during price fetch", str(e))
            print("Exception occurred during price fetch:", str(e))


    
    def log_activity(self, action, request=None, response=None):
        self.logger.log_activity(action, request, response, log_book=self.log_book)
    
    def login(self):
        """Handles the login process."""
        api_key = self.api_inputs['api_key'].text()
        api_secret = self.api_inputs['api_secret'].text()
        session_token = self.api_inputs['session_token'].text()

        # Perform login via BreezeAPI
        success = self.breeze_api.login(api_key, api_secret, session_token)

        if success:
            self.logger.log_activity(action="Login Successful", log_book=self.log_book)
        else:
            self.logger.log_activity(action="Login Failed", log_book=self.log_book)
    
    def refresh_positions(self):
        self.position_management.refresh_positions()
    
    def place_order(self):
        self.order_operations.place_order()

    def square_off_position(self, position):
        self.order_operations.square_off_position(position)

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingPlatform()
    window.show()
    sys.exit(app.exec())
