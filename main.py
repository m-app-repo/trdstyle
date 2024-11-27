import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication,QTableWidgetItem, QVBoxLayout, QWidget, QTextEdit, QPushButton,QListWidget,
    QGridLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QRadioButton, QHBoxLayout, QGroupBox,QSizePolicy,QSpacerItem
)
from ui_components import create_credentials_section, create_positions_table,create_place_order_section
from breeze_api import BreezeAPI
from logger import Logger
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QColor
from PySide6.QtCore import QDate
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt

class TradingPlatform(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trading Platform - v1.1")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize BreezeAPI and Logger
        self.logger = Logger()
        self.breeze_api = BreezeAPI(logger=self.logger)

        self.csv_data = self.load_csv_data()
        # Create UI components
        self.create_ui()
        self.populate_stock_codes()
    
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
        self.place_order_section, self.order_inputs = create_place_order_section(self)  # Store inputs in self.order_inputs
        main_layout.addLayout(self.place_order_section)

        # Log Book Section
        self.log_book = QTextEdit()
        self.log_book.setReadOnly(True)
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
    
    def update_selection_display(self, list_widget, display_widget):
        selected_items = list_widget.selectedItems()
        if selected_items:
            selected_text = selected_items[0].text()  # Get the first selected item
            display_widget.setText(selected_text)  # Update the display widget (e.g., QLineEdit)
        else:
            display_widget.clear()  # Clear the display widget if no item is selected
    
    def on_stock_code_selected(self, selected_stock_code):
        """Populates StrikePrice, ExpiryDate, Right (radio buttons), and Lot Size when a stock code is selected."""
        # Filter data for the selected stock code
        filtered_data = self.csv_data[self.csv_data["ShortName"] == selected_stock_code]

        # Sort StrikePrice by ascending order and populate it
        sorted_strike_prices = sorted(filtered_data["StrikePrice"].unique())
        #unique_expiry_dates = filtered_data["ExpiryDate"].unique()
        unique_expiry_dates = pd.to_datetime(filtered_data["ExpiryDate"].unique(), format='%d-%b-%Y')
        sorted_expiry_dates = sorted(unique_expiry_dates)



        unique_option_types = filtered_data["OptionType"].unique()
        #lot_size = filtered_data["LotSize"].unique()  # Assuming all rows for this stock code have the same lot size
        lot_size = filtered_data["LotSize"].values[0] if not filtered_data.empty else 0

        # Clear and populate the strike price combo box (sorted)
        self.order_inputs['strike_price'].clear()
        self.order_inputs['strike_price'].addItems([str(price) for price in sorted_strike_prices])
        # Convert strike prices to floats
        strike_prices = [float(price) for price in sorted_strike_prices]




        # Clear and populate the expiry date combo box
        self.order_inputs['expiry_date'].clear()
        #self.order_inputs['expiry_date'].addItems(unique_expiry_dates)
        self.order_inputs['expiry_date'].addItems([date.strftime('%d-%b-%Y') for date in sorted_expiry_dates])
        try:
            spot_price_request={"Stock Code":selected_stock_code}
            spot_price_response = self.breeze_api.get_spot_price(selected_stock_code)
            spot_price = float(spot_price_response.get("spot_price", 0.0))
            self.order_inputs['spot_price'].setText(str(spot_price))
            # Log the price response
            self.log_activity("Spot Price Response", request=spot_price_request, response=spot_price_response)
        except Exception as e:
                spot_price = 0.0
                self.order_inputs['spot_price'].setText(str(spot_price))
                self.log_activity("Error fetching spot price", response=str(e))

        # Ensure spot price is valid
        try:
            spot_price = float(self.order_inputs['spot_price'].text())
        except ValueError:
            spot_price = 0.0  # Default or handle as needed

        # Find the strike price closest to the spot price
        if strike_prices:
            print("spot",spot_price)
            closest_strike_price = min(strike_prices, key=lambda x: abs(x - spot_price))
            print("price",closest_strike_price)
            # Find the index of the closest strike price
            closest_index = strike_prices.index(closest_strike_price)

            # Select the item in the QListWidget
            self.order_inputs['strike_price'].setCurrentRow(closest_index)
        # Set the right (radio buttons)
        # if "CE" in unique_option_types:
        #      self.order_inputs['call_radio'].setChecked(True)
        # else:
        #     self.order_inputs['put_radio'].setChecked(True)
        
        # Automatically populate the lot size field
        self.order_inputs['lot_size'].setText(str(lot_size))
        
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
            self.logger.log_activity(action="Login Successful",log_book=self.log_book)
        else:
            self.logger.log_activity(action="Login Failed",log_book=self.log_book)
    
    def refresh_positions(self):
        positions = self.breeze_api.get_positions()

        if positions:
            self.update_positions_table(positions)
            self.log_activity("Refresh Positions", {}, "Positions fetched successfully")
        else:
            # Clear the table if no positions are found or an error occurs
            self.positions_table.setRowCount(0)  # Clear all rows in the table
            self.log_activity("Error fetching positions", {}, "No positions found or API error")
    
    def add_numeric_item(self,table, row, column, value, decimal_places=2):
        """
        Helper function to add a numeric item to a QTableWidget with right alignment.
        
        :param table: QTableWidget instance
        :param row: Row position to insert the item
        :param column: Column position to insert the item
        :param value: Numeric value to insert
        :param decimal_places: Number of decimal places for formatting
        """
        formatted_value = f"{value:.{decimal_places}f}" if isinstance(value, float) else str(value)
        item = QTableWidgetItem(formatted_value)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        table.setItem(row, column, item)
    
    def calculate_equity(self,buy_price, sell_price, quantity, exchange_type):
        # Calculate trade value
        
        trade = (buy_price * quantity) + (sell_price * quantity)
        
        # Calculate exchange charges
        exchange = 0
        if exchange_type == 'NSE':
            exchange = trade * 0.0005050
        elif exchange_type == 'BSE':
            exchange = trade * 0.0005
        
        # Calculate brokerage
        if buy_price == 0 and sell_price == 0 or quantity == 0:
            brokerage = 0
        elif sell_price == 0 or buy_price == 0:
            #brokerage = 20
            brokerage=0
        else:
            #brokerage = 40
            brokerage=0
        
        # Calculate SEBI charges
        sebi = (buy_price * quantity * 0.000001) + (sell_price * quantity * 0.000001)
        
        # Calculate GST
        gst = (brokerage + exchange + sebi) * 0.18
        
        # Calculate STT
        stt = sell_price * quantity * 0.000625
        
        # Calculate Stamp Duty
        stamp = buy_price * quantity * 0.00003
        
        # Calculate total expenses
        total_expense = brokerage + exchange + sebi + gst + stt + stamp
        

        
        
        # Calculate break-even point (BEP)
        # break_even = 0
        # if quantity == 0:
        #     break_even = 0
        # else:
        #     break_even = total_expense / quantity
        
        # Calculate net profit/loss
        raised_trade_value=buy_price * quantity
        settled_trade_value=sell_price * quantity
        net = (sell_price * quantity) - (buy_price * quantity) - total_expense
        percent= (net/(raised_trade_value+total_expense))*100
        # Return net and break-even point
        return raised_trade_value, settled_trade_value,total_expense, net, percent
    
    def update_positions_table(self, positions):
        # Clear existing rows
        self.positions_table.setRowCount(0)

        # Define the order of the columns based on the specified order
        columns = [
            "stock_code", "expiry_date", 
            "strike_price", "right", "action", "quantity", "average_price", "ltp", "price", 
            "stock_index_indicator", "cover_quantity", "stoploss_trigger", "stoploss", "take_profit", 
            "available_margin", "squareoff_mode", "order_id", "pledge_status", "pnl", 
            "underlying", "settlement_id", "segment", "product_type", "exchange_code"
        ]

        # Adjust the headers to include the new calculated attributes and the "Square Off" button
        headers = ["Square Off", "Calculated P&L", "Percent", "Total Cost", "Current Value", "Total Expense", "Spot Price"] + columns[:22]
        self.positions_table.setColumnCount(len(headers))
        self.positions_table.setHorizontalHeaderLabels(headers)

        # Add positions to the table
        for position in positions:
            if position.get("segment") == "equity":
                continue  # Skip equity positions
            row_position = self.positions_table.rowCount()
            self.positions_table.insertRow(row_position)

            # Fetch relevant data
            quantity = int(position.get("quantity", 0))
            average_price = float(position.get("average_price", 0))
            ltp = float(position.get("ltp", 0))
            try:
                strike_price = position.get("strike_price")
                if strike_price is None:
                    strike_price = 0  # Handle None case
                else:
                    strike_price = float(strike_price)
            except ValueError:
                strike_price = 0  # Handle invalid string cases

            action = position.get("action", "").lower()  # buy or sell
            right = position.get("right", "").lower()  # call or put
            stock_code = position.get("stock_code", "")

            # Fetch the current spot price
            try:
                spot_price_response = self.breeze_api.get_spot_price(stock_code)
                spot_price = float(spot_price_response.get("spot_price", 0.0))
            except Exception:
                spot_price = 0.0

            raised_trade_value, settled_trade_value, total_expense, net, percent = self.calculate_equity(
                average_price, ltp, quantity, 'NSE'
            )

            # Add the Square Off button
            square_off_button = QPushButton("Square Off")
            square_off_button.clicked.connect(lambda _, pos=position: self.square_off_position(pos))
            self.positions_table.setCellWidget(row_position, 0, square_off_button)

            # Add the calculated values using the reusable function
            calculated_pnl_item = QTableWidgetItem(f"{net:.2f}")
            if net < 0:
                calculated_pnl_item.setBackground(QColor(255, 182, 193))  # Light red
            else:
                calculated_pnl_item.setBackground(QColor(144, 238, 144))  # Light green
            calculated_pnl_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.positions_table.setItem(row_position, 1, calculated_pnl_item)

            self.add_numeric_item(self.positions_table, row_position, 2, percent)
            self.add_numeric_item(self.positions_table, row_position, 3, raised_trade_value)
            self.add_numeric_item(self.positions_table, row_position, 4, settled_trade_value)
            self.add_numeric_item(self.positions_table, row_position, 5, total_expense)
            self.add_numeric_item(self.positions_table, row_position, 6, spot_price)

            # Populate the table with the remaining position data in the correct order
            for col, column_name in enumerate(columns):
                value = position.get(column_name, "None")
                self.positions_table.setItem(row_position, col + 7, QTableWidgetItem(str(value)))
    
    def auto_populate_price(self):
     # Prepare the request data for the API
        premium_data={}
        for key, input_field in self.order_inputs.items():
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
            elif isinstance(input_field, str):  # Handle 'right' and 'action' which are already strings
                premium_data[key] = input_field
            else:
                print(f"Unhandled input type: {key} -> {input_field}")

        price_request_data = {
            "stock_code": premium_data['stock_code'],
            "exchange_code": "NFO",
            "expiry_date": premium_data['expiry_date'],
            "product_type": premium_data['product'],
            "right": premium_data['right'],
            "strike_price": premium_data['strike_price'],
            "action":premium_data['action']
        }

        try:
            # Fetch the latest price using the Breeze API
            quotes_response = self.breeze_api.get_quotes(
                stock_code=premium_data['stock_code'],
                exchange_code="NFO",
                expiry_date=premium_data['expiry_date'],
                product_type=premium_data['product'],
                right= premium_data['right'],
                strike_price=premium_data['strike_price']
            )


            # Log the price response
            #self.log_activity("Price Response", request=price_request_data, response=quotes_response)

            # Extract the price from the response and update the price field
            if quotes_response and "Success" in quotes_response and quotes_response["Success"]:
                # Ensure that 'ltp' (last traded price) is available and set the price field
                if(premium_data['action'])=='buy':
                    latest_price = quotes_response["Success"][0].get("best_offer_price", "0.00")
                else:
                    latest_price = quotes_response["Success"][0].get("best_bid_price", "0.00")

                # Ensure that 'ltp' is a valid number before setting it
                if latest_price and latest_price != "None":
                    self.order_inputs['price'].setText(str(latest_price))
                    self.order_inputs['stoploss'].setText(str(latest_price-5))
                else:
                    self.order_inputs['price'].setText("0.00")
                    #self.order_inputs['stoploss'].setText("")
            else:
                # Set default price if API fails or returns no price
                self.order_inputs['price'].setText("0.00")
                #self.order_inputs['stoploss'].setText("")
                error_message = quotes_response.get('Error', 'Unknown error') if quotes_response else 'No response'
                self.log_activity("Error fetching price:", error_message)

        except Exception as e:
            # Handle any unexpected exceptions during the API call
            self.order_inputs['price'].setText("0.00")
            #self.order_inputs['stoploss'].setText("")
            self.log_activity("Error during price fetch", str(e))
    
    def place_order(self):
        order_data = {}

        # Loop through all the input fields to get their values
        for key, input_field in self.order_inputs.items():
            if isinstance(input_field, QLineEdit):
                order_data[key] = input_field.text()
            elif isinstance(input_field, QComboBox):
                order_data[key] = input_field.currentText()
            elif isinstance(input_field, QDateEdit):
                date_value = input_field.date().toString("yyyy-MM-dd") + "T06:00:00.000Z"
                order_data[key] = date_value
            elif isinstance(input_field, QListWidget):  # Handling QListWidget for strike_price and expiry_date
                    selected_items = input_field.selectedItems()
                    if selected_items:
                        order_data[key] = selected_items[0].text()
                    else:
                        order_data[key] = None  # If nothing is selected, assign None or a default value
            elif isinstance(input_field, str):  # Handle 'right' and 'action' which are already strings
                order_data[key] = input_field
            else:
                print(f"Unhandled input type: {key} -> {input_field}")
                self.log_activity(f"Unhandled input type: {key} -> {input_field}")

        # Map 'action' to 'transaction_type' for the Breeze API
        order_data['transaction_type'] = order_data.pop('action', None)
        order_data['action'] = order_data.pop('action', None)
        if 'quantity' in order_data and 'lot_size' in order_data:
            try:
                # Ensure both quantity and lot_size are integers
                quantity = int(order_data['quantity'])
                lot_size = int(order_data['lot_size'])
                order_data['quantity'] = quantity * lot_size
            except (TypeError, ValueError) as e:
                print(f"Error: Invalid quantity or lot size - {e}")
                self.log_activity(f"Error: Invalid quantity or lot size - {e}")
        else:
            print("Error: Missing 'quantity' or 'lot_size' in order_data")
            self.log_activity(f"Error: Missing 'quantity' or 'lot_size' in order_data")
            

        
        # Handle price field for market orders
        if order_data['order_type'].lower() == 'market':
            # Ensure price is 0 for market orders
            order_data['price'] = '0'
            #order_data['order_type']='limit';
        else:
            # Ensure price is provided for limit orders
            if not order_data.get('price'):
                self.log_activity("Error", request=order_data, response="Price must be specified for limit orders.")
                return
       
        
        # Place order using Breeze API
        try:
            order_response = self.breeze_api.place_order(order_data)
            self.log_activity("Place Order", order_data, order_response)
        except Exception as e:
            self.log_activity("Error placing order", request=order_data, response=str(e))
            print(f"Error placing order: {e}")

    def square_off_position(self, position):
        square_off_response = self.breeze_api.square_off_position(position)
        self.log_activity("Square Off Position", position, square_off_response)


# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingPlatform()
    window.show()
    sys.exit(app.exec())
