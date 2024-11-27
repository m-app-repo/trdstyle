
from PySide6.QtWidgets import QTableWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

def create_positions_table(window):
    positions_table = QTableWidget(0, 25)
    positions_table.setHorizontalHeaderLabels(['Square Off', 'Calculated P&L', 'Average Price', 'BEP', 'Spot Price', 'stock_code', 'expiry_date', 'strike_price', 'right', 'action', 'quantity', 'ltp', 'price', 'Total Cost', 'stock_index_indicator', 'cover_quantity', 'Current Value', 'stoploss_trigger', 'stoploss', 'take_profit', 'available_margin', 'squareoff_mode', 'order_id', 'pledge_status', 'pnl', 'underlying', 'settlement_id', 'segment'])
    
    refresh_button = QPushButton("Refresh Positions")
    refresh_button.clicked.connect(window.refresh_positions)

    # Mouse hover event to display row details in a pop-up window
    def show_row_details(row):
        row_data = {}
        for col in range(positions_table.columnCount()):
            item = positions_table.item(row, col)
            if item:
                row_data[positions_table.horizontalHeaderItem(col).text()] = item.text()

        popup = QDialog(window)
        popup.setWindowTitle("Row Details")
        layout = QVBoxLayout()
        for key, value in row_data.items():
            layout.addWidget(QLabel(f"{key}: {value}"))
        popup.setLayout(layout)
        popup.setGeometry(QCursor.pos().x(), QCursor.pos().y(), 300, 400)
        popup.show()

        # Close the popup when the mouse moves away
        def close_popup(event):
            popup.close()

        positions_table.viewport().leaveEvent = close_popup

    positions_table.cellEntered.connect(lambda row, col: show_row_details(row))

    return positions_table, refresh_button
