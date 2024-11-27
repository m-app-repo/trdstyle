# ui_components.py
from PySide6.QtWidgets import QVBoxLayout, QWidget

from credentials_section import create_credentials_section
from place_order_section import create_place_order_section
from positions_table import create_positions_table

class MainUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QVBoxLayout()

        # Create and add credentials section
        credentials_layout, credentials_inputs = create_credentials_section(self)
        main_layout.addLayout(credentials_layout)

        # Create and add place order section
        place_order_section, order_inputs = create_place_order_section(self)
        main_layout.addLayout(place_order_section)

        # Create and add positions table
        positions_table, refresh_button = create_positions_table(self)
        main_layout.addWidget(positions_table)
        main_layout.addWidget(refresh_button)

        # Set main layout
        self.setLayout(main_layout)

        # Reference to input fields
        self.credentials_inputs = credentials_inputs
        self.order_inputs = order_inputs

    def login(self):
        # Handle login logic using self.credentials_inputs
        print("Login logic here")

    def place_order(self):
        # Handle placing an order using self.order_inputs
        print("Place order logic here")

    def update_selection_display(self, source_widget, target_widget):
        # Updates the selection display logic
        selected_items = source_widget.selectedItems()
        if selected_items:
            target_widget.setText(selected_items[0].text())

    def refresh_positions(self):
        # Refresh logic for positions table
        print("Refresh positions logic here")
