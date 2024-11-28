import pandas as pd
from PySide6.QtCore import Qt

class StockCodeOperations:
    def __init__(self, breeze_api, logger, order_inputs, log_book):
        self.breeze_api = breeze_api
        self.logger = logger
        self.order_inputs = order_inputs
        self.log_book = log_book

    def populate_stock_code_details(self, csv_data, selected_stock_code):
        """Populates StrikePrice, ExpiryDate, Right (radio buttons), and Lot Size when a stock code is selected."""
        filtered_data = self.filter_data_by_stock_code(csv_data, selected_stock_code)
        self.populate_strike_prices(filtered_data)
        self.populate_expiry_dates(filtered_data)
        self.populate_lot_size(filtered_data)
        self.set_spot_price(selected_stock_code)
        self.set_closest_strike_price()

    def filter_data_by_stock_code(self, csv_data, selected_stock_code):
        return csv_data[csv_data["ShortName"] == selected_stock_code]

    def populate_strike_prices(self, filtered_data):
        sorted_strike_prices = sorted(filtered_data["StrikePrice"].unique())
        self.order_inputs['strike_price'].clear()
        self.order_inputs['strike_price'].addItems([str(price) for price in sorted_strike_prices])

    def populate_expiry_dates(self, filtered_data):
        unique_expiry_dates = pd.to_datetime(filtered_data["ExpiryDate"].unique(), format='%d-%b-%Y')
        sorted_expiry_dates = sorted(unique_expiry_dates)
        self.order_inputs['expiry_date'].clear()
        self.order_inputs['expiry_date'].addItems([date.strftime('%d-%b-%Y') for date in sorted_expiry_dates])

    def populate_lot_size(self, filtered_data):
        lot_size = filtered_data["LotSize"].values[0] if not filtered_data.empty else 0
        self.order_inputs['lot_size'].setText(str(lot_size))

    def set_spot_price(self, selected_stock_code):
        try:
            spot_price_request = {"Stock Code": selected_stock_code}
            spot_price_response = self.breeze_api.get_spot_price(selected_stock_code)
            spot_price = float(spot_price_response.get("spot_price", 0.0))
            self.order_inputs['spot_price'].setText(str(spot_price))
            self.log_activity("Spot Price Response", request=spot_price_request, response=spot_price_response)
        except Exception as e:
            self.order_inputs['spot_price'].setText("0.0")
            self.log_activity("Error fetching spot price", response=str(e))

    def set_closest_strike_price(self):
        try:
            spot_price = float(self.order_inputs['spot_price'].text())
        except ValueError:
            spot_price = 0.0

        strike_prices = [float(self.order_inputs['strike_price'].item(i).text()) for i in range(self.order_inputs['strike_price'].count())]
        if strike_prices:
            closest_strike_price = min(strike_prices, key=lambda x: abs(x - spot_price))
            closest_item = self.order_inputs['strike_price'].findItems(str(closest_strike_price), Qt.MatchExactly)
            if closest_item:
                self.order_inputs['strike_price'].setCurrentItem(closest_item[0])

    def update_selection_display(self, source_widget, target_widget):
        """Updates the target widget with the currently selected item's text from the source widget."""
        selected_items = source_widget.selectedItems()
        if selected_items:
            target_widget.setText(selected_items[0].text())
        else:
            target_widget.clear()

    def log_activity(self, action, request=None, response=None):
        self.logger.log_activity(action, request, response, log_book=self.log_book)
