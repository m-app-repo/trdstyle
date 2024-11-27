# Trading Platform Application

## Overview

This project is a desktop trading platform application designed to interact with the Breeze API for trading options and futures. It provides a user-friendly interface for viewing positions, placing orders, and managing options trading through an integrated GUI. The application is built using Python and the PySide6 framework for the GUI.

## Features

1. **Login Integration**: Users can log in to the Breeze API using API credentials (API Key, API Secret, and Session Token).
2. **Real-time Data Retrieval**: The application allows users to fetch open positions, place new orders, and get live quotes and spot prices.
3. **Order Management**: Users can place buy or sell orders, as well as square off positions directly from the platform.
4. **Live Logging**: All user activities, including API requests and responses, are logged in real-time and displayed in the log book for better traceability.
5. **Real-time JSON Viewer**: A separate component allows users to view live JSON data with automatic scrolling capabilities.

## Files Description

1. **breeze_api.py**
   - This file contains the `BreezeAPI` class, which is responsible for managing API communication with the Breeze Connect API.
   - Key methods include:
     - `login()`: Logs in to the Breeze API.
     - `get_open_positions()`, `get_positions()`: Retrieve open positions.
     - `place_order()`: Place a new trading order.
     - `square_off_position()`: Square off an existing position.
     - `get_quotes()`, `get_spot_price()`: Fetch live quotes and spot prices.

2. **jsonviewer.py**
   - Implements a GUI-based JSON viewer using Tkinter.
   - Continuously monitors and displays JSON data from a specified file, allowing users to inspect trading logs or other relevant data.

3. **logger.py**
   - Defines the `Logger` class for logging API activities, such as user actions, requests, and responses.
   - Logs are saved to `tradelog.json` and also updated in the main GUI log section.

4. **main.py**
   - This is the main entry point of the application. It initializes the `TradingPlatform` class and sets up the GUI using PySide6.
   - It integrates the `BreezeAPI` and `Logger` classes to provide a cohesive user experience for trading.
   - Key components include:
     - Credentials Section: Handles user login.
     - Positions Section: Displays open positions.
     - Order Placement Section: Allows users to create new trading orders.
     - Log Book: Displays log messages for all actions taken.

5. **ui_components.py**
   - Contains functions for creating different UI sections used in the application.
   - UI sections include credentials, order placement, and open positions tables.
   - Utilizes PySide6 widgets to create a visually structured layout for managing trades.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Run `setup.bat` to install dependencies:
  ```bash
  setup.bat
  ```
- The setup script will install required packages, including:
  - `PySide6` for GUI elements
  - `BreezeConnect` for API communication

### Running the Application
- Run the `main.py` file to launch the trading platform GUI:
  ```bash
  python main.py
  ```
- The `setup.bat` can be used to configure initial environment settings if required on a Windows platform.

## Usage

1. **Login**: Enter your API Key, API Secret, and Session Token, then click "Login".
2. **View Open Positions**: Click "Refresh Positions" to see your current open positions.
3. **Place an Order**:
   - Fill in the stock code, quantity, expiry date, strike price, etc.
   - Select "Buy" or "Sell" and click "Place Order".
4. **Log Book**: All actions are logged and can be reviewed in the log section at the bottom of the interface.

## Logging
- Logs are saved in `tradelog.json` for future reference.
- The `Logger` class in `logger.py` manages the logging mechanism, recording both requests and responses.

## JSON Viewer
- The JSON viewer allows you to see real-time updates of the `tradelog.json` file.
- To run the viewer, execute the `jsonviewer.py` file.

## Dependencies
- `PySide6`: For GUI development.
- `BreezeConnect`: For interacting with Breeze API.
- `tkinter`: Used in `jsonviewer.py` for viewing logs.
- `pandas`: To manipulate CSV data for stock codes and other trading-related information.

## Future Enhancements
- Implement error handling for network connectivity issues.
- Enhance the UI for better user experience with more charts and analytics.
- Add support for managing multiple accounts and brokers.

## License
This project is licensed under the MIT License.

