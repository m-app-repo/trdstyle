from breeze_connect import BreezeConnect

class BreezeAPI:
    def __init__(self, logger):
        self.breeze = None
        self.logged_in = False
        self.logger = logger


    def login(self, api_key, api_secret, session_token):
        self.breeze = BreezeConnect(api_key=api_key)
        try:
            self.breeze.generate_session(api_secret=api_secret, session_token=session_token)
            self.logged_in = True
            # Log successful login
            self.logger.log_activity("Login Successful", request={"api_key": api_key}, response="Logged in successfully.")
            return True
        except Exception as e:
            # Log login error
            self.logger.log_activity("Login Error", request={"api_key": api_key}, response=str(e))
            return False

    def get_open_positions(self):
        try:
            # Replace with the correct API method for fetching open positions
            response = self.breeze.get_portfolio_positions()
            return response
        except Exception as e:
            print(f"Error fetching open positions: {e}")
            return None

    def get_positions(self):
        if self.logged_in:
            try:
                response = self.breeze.get_portfolio_positions()
                # Log the request and response
                self.logger.log_activity("Get Positions", request={}, response=response)
                return response.get('Success', [])
            except Exception as e:
                # Log the exception
                self.logger.log_activity("Error Fetching Positions", request={}, response=str(e))
                return None
        else:
            # Log that user is not logged in
            self.logger.log_activity("Get Positions Failed", request={}, response="User not logged in.")
        return None


    def place_order(self, order_data):
        if self.logged_in:
            try:
                #if(order_data['transaction_type'].lower()=="buy"):
                # # Prepare request data (avoid logging sensitive data)
                #     request_data = {
                #         "stock_code": order_data['stock_code'],
                #         "exchange_code": "NFO",
                #         "product": "optionplus",
                #         "action": order_data['transaction_type'].lower(),
                #         "order_type": order_data['order_type'].lower(),
                #         "quantity": order_data['quantity'],
                #         "expiry_date": order_data['expiry_date'],
                #         "right": order_data['right'].lower(),
                #         "strike_price": order_data['strike_price'],
                #         "stoploss": order_data.get('stoploss', ''),
                #         "price": order_data.get('price', ''),
                #         "validity": order_data.get('validity', 'day').lower(),
                #         "validity_date": order_data.get('validity_date', ''),
                #         "disclosed_quantity": order_data.get('disclosed_quantity', '0'),
                #         "order_type_fresh" :"Limit",
                #         "order_rate_fresh": "20",
                #         "user_remark":"Test"                        
                #     }
                # else:
                request_data = {
                    "stock_code": order_data['stock_code'],
                    "exchange_code": "NFO",
                    "product": "options",
                    "action": order_data['transaction_type'].lower(),
                    "order_type": order_data['order_type'].lower(),
                    "quantity": order_data['quantity'],
                    "expiry_date": order_data['expiry_date'],
                    "right": order_data['right'].lower(),
                    "strike_price": order_data['strike_price'],
                    "stoploss": order_data.get('stoploss', ''),
                    "price": order_data.get('price', ''),
                    "validity": order_data.get('validity', 'day').lower(),
                    "validity_date": order_data.get('validity_date', ''),
                    "disclosed_quantity": order_data.get('disclosed_quantity', '0')
                }

                # Log the order request
                self.logger.log_activity("Place Order Request", request=request_data, response=None)

                order_response = self.breeze.place_order(**request_data)

                # Log the order response
                self.logger.log_activity("Place Order Response", request=request_data, response=order_response)

                return order_response
            except Exception as e:
                # Log the exception
                self.logger.log_activity("Error Placing Order", request=order_data, response=str(e))
                return None
        else:
            # Log that user is not logged in
            self.logger.log_activity("Place Order Failed", request=order_data, response="User not logged in.")
        return None


    def square_off_position(self, position):
        if self.logged_in:
            try:
                action = "buy" if position["action"].lower() == "sell" else "sell"
                request_data = {
                    "stock_code": position["stock_code"],
                    "exchange_code": position["exchange_code"],
                    "product": "options",
                    "action": action,
                    "order_type": "market",
                    "quantity": position["quantity"],
                    "expiry_date": position["expiry_date"],
                    "right": position["right"].lower(),
                    "strike_price": position["strike_price"],
                    "validity": "day"
                }

                # Log the square off request
                self.logger.log_activity("Square Off Request", request=request_data, response=None)

                response = self.breeze.place_order(**request_data)

                # Log the square off response
                self.logger.log_activity("Square Off Response", request=request_data, response=response)

                return response
            except Exception as e:
                # Log the exception
                self.logger.log_activity("Error Squaring Off Position", request=position, response=str(e))
                return None
        else:
            # Log that user is not logged in
            self.logger.log_activity("Square Off Failed", request=position, response="User not logged in.")
        return None

    def get_quotes(self, stock_code, exchange_code, expiry_date, product_type, right, strike_price):
        try:
            request_data = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "expiry_date": expiry_date,
                "product_type": product_type,
                "right": right,
                "strike_price": strike_price
            }

            # Log the quotes request
            self.logger.log_activity("Get Quotes Request", request=request_data, response=None)

            response = self.breeze.get_quotes(**request_data)

            # Log the quotes response
            self.logger.log_activity("Get Quotes Response", request=request_data, response=response)

            return response
        except Exception as e:
            # Log the exception
            self.logger.log_activity("Error Fetching Quotes", request=request_data, response=str(e))
            return None

    
    def get_spot_price(self, stock_code):
        try:
            request_data = {
                "stock_code": stock_code,
                "exchange_code": "NSE",
                "product_type": "cash",
                "right": "others",
                "strike_price": "0"
            }

            # Log the spot price request
            self.logger.log_activity("Get Spot Price Request", request=request_data, response=None)

            response = self.breeze.get_quotes(**request_data)

            # Log the spot price response
            self.logger.log_activity("Get Spot Price Response", request=request_data, response=response)

            if response.get("Success"):
                spot_price = response["Success"][0].get("ltp", 0.0)
                spot_price = float(spot_price)
            else:
                spot_price = 0.0
        except Exception as e:
            spot_price = 0.0
            # Log the exception
            self.logger.log_activity("Error Fetching Spot Price", request=request_data, response=str(e))

        return {"spot_price": spot_price}
