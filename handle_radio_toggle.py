def handle_radio_toggle(checked, value, window):
    """
    Handles the toggling of both Call/Put and Buy/Sell radio buttons.
    
    Parameters:
        checked (bool): Whether the radio button was toggled on or off.
        value (str): The value associated with the radio button ('call', 'put', 'buy', or 'sell').
        window: The main window or the class instance that contains order_inputs.
    """
    if not checked:
        return

    if value in ['call', 'put']:
        window.order_inputs['right'] = value
        print(f"Right Option Selected: {value}")

    if value in ['buy', 'sell']:
        window.order_inputs['action'] = value
        print(f"Action Selected: {value}")
    window.auto_populate_price()