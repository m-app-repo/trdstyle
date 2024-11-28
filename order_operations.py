class OrderOperations:
    def __init__(self, breeze_api, logger, order_inputs, log_book):
        self.breeze_api = breeze_api
        self.logger = logger
        self.order_inputs = order_inputs
        self.log_book = log_book

    def place_order(self):
        order_details = self.get_order_details()
        try:
            response = self.breeze_api.place_order(order_details)
            self.log_activity("Place Order", request=order_details, response=response)
        except Exception as e:
            self.log_activity("Error placing order", response=str(e))

    def get_order_details(self):
        return {
            "exchange_code": self.order_inputs['exchange_code'].currentText(),
            "stock_code": self.order_inputs['stock_code'].currentText(),
            "action": self.order_inputs['action'],
            "quantity": self.order_inputs['quantity'].text(),
        }

    def square_off_position(self, position):
        self.log_activity("Square Off Position", request=position)

    def log_activity(self, action, request=None, response=None):
        self.logger.log_activity(action, request, response, log_book=self.log_book)
