from PySide6.QtCore import Qt

class HandleRadioToggle:
    def __init__(self, logger, order_inputs, log_book):
        self.logger = logger
        self.order_inputs = order_inputs
        self.log_book = log_book

    def handle_radio_toggle(self, checked, toggle_type, window):
        """Handles the radio button toggles for call/put or buy/sell."""
        if checked:
            # Update the order_inputs dictionary with the selected value
            if toggle_type == 'call':
                self.order_inputs['right'] = 'call'
            elif toggle_type == 'put':
                self.order_inputs['right'] = 'put'
            elif toggle_type == 'buy':
                self.order_inputs['action'] = 'buy'
            elif toggle_type == 'sell':
                self.order_inputs['action'] = 'sell'

            # Call the auto_populate_price method to update the price
            window.auto_populate_price()

