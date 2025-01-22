import os
import sys
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QProgressBar, QTableWidget, QTableWidgetItem, QLineEdit, QDateEdit, QComboBox, QListWidget, QMessageBox, QPushButton
)
from PyQt5.QtGui import QPixmap
from datetime import date 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from view import delete_expense, delete_recipe, insert_expense, insert_recipe, see_expenses, see_recipes
from models import Database

# Colors
c0 = "#2e2d2b"  # black
c1 = "#feffff"  # white
c2 = "#4fa882"  # green
c3 = "#38576b"  # value
c4 = "#403d3d"  # letter
c5 = "#e06636"  # profit (orange)
c6 = "#038cfc"  # blue
c7 = "#3fbfb9"  # another green
c8 = "#263238"  # another green
c9 = "#e9edf5"  # another green

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Define categories and selected_categories
        self.categories = ['Choose a category', 'Travel', 'Food', 'Entertainment', 'Shopping']
        self.selected_categories = []

        # Set up window
        self.setWindowTitle("PyQt Example")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet(f"background-color: {c9};")

        # Create main layout
        layout = QVBoxLayout(self)

        # Top Frame
        frame_up = self.create_top_frame()
        layout.addWidget(frame_up)

        # Middle Frame
        frame_middle = self.create_middle_frame()
        layout.addWidget(frame_middle)

        # Bottom Frame
        frame_down = self.create_bottom_frame()
        layout.addWidget(frame_down)

        # Connect the buttons to their respective methods
        self.add_receipt_button.clicked.connect(self.set_receipt_mode)
        self.add_expense_button.clicked.connect(self.set_expense_mode)

        # Track whether we are adding a receipt or an expense
        self.is_expense = False

        # Set the main layout
        self.setLayout(layout)
        self.show()

    def create_top_frame(self):
        frame_up = QFrame(self)
        frame_up.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )
        frame_up.setFixedHeight(80)

        try:
            img_path = os.path.join(os.path.dirname(__file__), "log.png")
            if os.path.exists(img_path):
                app_img = QPixmap(img_path).scaled(45, 45)
                if not app_img.isNull():
                    label_logo = QLabel(self)
                    label_logo.setPixmap(app_img)
                    label_logo.setStyleSheet("border: none;")

                    label_text = QLabel("Personal Budget Management", self)
                    label_text.setStyleSheet(
                        f"font: bold 20px Verdana; color: {c4}; border: none;"
                    )

                    frame_up_layout = QHBoxLayout(frame_up)
                    frame_up_layout.addWidget(label_logo)
                    frame_up_layout.addWidget(label_text)
                    frame_up_layout.setSpacing(10)
                    frame_up_layout.addStretch()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            label_logo = QLabel("  Personal Budget Management", self)
            label_logo.setStyleSheet(f"font: bold 20px Verdana; color: {c4};")
            frame_up_layout = QVBoxLayout(frame_up)
            frame_up_layout.addWidget(label_logo)

        return frame_up

    def create_middle_frame(self):
        frame_middle = QFrame(self)
        frame_middle.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )
        frame_middle.setFixedHeight(300)
        frame_middle_layout = QHBoxLayout(frame_middle)
        frame_middle_layout.setContentsMargins(0, 0, 0, 0)  # Set margins for this layout
        frame_middle_layout.setSpacing(0) 

        # Progress Bar and Chart Container
        progress_chart_container = self.create_progress_chart_container()
        frame_middle_layout.addWidget(progress_chart_container, alignment=Qt.AlignTop)

        # Totals Container
        totals_container = self.create_totals_container()
        frame_middle_layout.addWidget(totals_container)

        # Circular Chart Container
        circular_container = self.create_circular_container()
        frame_middle_layout.addWidget(circular_container)
        return frame_middle

    def create_bottom_frame(self):
        frame_down = QFrame(self)
        frame_down.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )

        # Create the main horizontal layout for the frame
        frame_down_layout = QHBoxLayout(frame_down)

        # Left Section for tables_container
        tables_container = self.create_tables_container()
        frame_down_layout.addWidget(tables_container, 1)  # 1 indicates it takes flexible space

        # Right Section - for the crud_container, configurations_container, and remove button
        right_layout = QVBoxLayout()

        # Create a horizontal layout to hold the crud_container and configurations_container
        horizontal_layout = QHBoxLayout()

        # CRUD Container
        crud_container = self.create_crud_container("Enter new expenses:")
        horizontal_layout.addWidget(crud_container)

        # Configurations Container
        configurations_container = self.create_configurations_container("Enter new recipes:")
        horizontal_layout.addWidget(configurations_container)

        # Add the horizontal layout to the right_layout
        right_layout.addLayout(horizontal_layout)

        # Remove Rows Button
        remove_button = QPushButton("Remove Selected Row", self)
        remove_button.clicked.connect(self.remove_selected_row)  # Connect to your function to remove rows
        remove_button.setStyleSheet(
            """
            QPushButton {
                font: 10px Verdana;
                background-color: #F44336;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
            """
        )
        right_layout.addWidget(remove_button)  # Add the button under the containers

        # Add the right layout to the frame_down_layout
        frame_down_layout.addLayout(right_layout)

        return frame_down

    def create_progress_chart_container(self):
        container = QWidget(self)
        container.setFixedWidth(200)
        container.setFixedHeight(100)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Progress Bar Section
        label_percentage = QLabel("Percentage of income spent:", self)
        label_percentage.setStyleSheet(f"font: bold 10px Verdana; color: {c4}; border: none;")
        layout.addWidget(label_percentage)

        progress_layout = QHBoxLayout()
        bar = QProgressBar(container)
        bar.setRange(0, 100)
        bar.setValue(50)
        bar.setTextVisible(False)
        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {c9};
                border: 1px solid {c0};
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {c7};
                border-radius: 5px;
            }}
            """
        )
        bar.setFixedSize(120, 20)
        progress_layout.addWidget(bar)

        percentage_label = QLabel("50%", self)
        percentage_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0}; border: none;")
        progress_layout.addWidget(percentage_label)
        layout.addLayout(progress_layout)

        return container

    def create_totals_container(self):
        container = QWidget(self)
        container.setFixedWidth(210)
        container.setFixedHeight(200)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Total Income
        self.add_total_item(layout, "Total Monthly Income", 500)

        # Total Expenses
        self.add_total_item(layout, "Total Monthly Expenses", 600)

        # Total Balance
        self.add_total_item(layout, "Total Cash Balance", 420)

        return container

    def create_circular_container(self):
        container = QWidget(self)
        container.setFixedWidth(500)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Create Matplotlib figure
        figure = plt.Figure(figsize=(4, 3), dpi=100)
        ax = figure.add_subplot(111)

        # Pie chart data
        values = [345, 225, 534]
        categories = ["Income", "Expenses", "Balance"]
        colors = ["#4fa882", "#038cfc", "#e06636"]
        explode = [0.05, 0.05, 0.05]

        # Plot pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            autopct="%1.1f%%",
            colors=colors,
            explode=explode,
            startangle=90,
            wedgeprops={"width": 0.4, "edgecolor": "white"}
        )

        # Add legend to the side
        ax.legend(
            wedges,
            categories,
            title="Categories:",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),  # Positions legend to the right of the chart
            fontsize=10
        )

        # Add Matplotlib figure to Qt widget
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        return container

    def add_total_item(self, layout, title, value):
            label_title = QLabel(title.upper(), self)
            label_title.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; border: none;")
            layout.addWidget(label_title)

            label_value = QLabel(f"€ {value:,.2f}".upper(), self)
            label_value.setStyleSheet(
                f"font: bold 17px Arial; color: #545454; border-top: 1px solid {c0};"
            )
            layout.addWidget(label_value)

    def create_tables_container(self):
        container = QWidget(self)
        container.setFixedWidth(300)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        table_label = QLabel("Income and Expenses table:", self)
        table_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0};")
        layout.addWidget(table_label)

        self.table = QTableWidget(10, 4, self)  # Set self.table here
        self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Date', 'Amount'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Allow row selection

        layout.addWidget(self.table)

        list_Items = [[1, "Salary", "2025-01-01", 3000],
                    [2, "Rent", "2025-01-05", -1200],
                    [3, "Groceries", "2025-01-10", -300],
                    [4, "Freelance Work", "2025-01-15", 800]]

        # Populate the QTableWidget
        for row_idx, row_data in enumerate(list_Items):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Adjust column widths to fit the content
        self.table.resizeColumnsToContents()

        # Apply style to the table
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {c9};  /* Background color */
                border: 1px solid {c2};  /* Border color */
                color: {c0};
                font: 8px Verdana;
            }}
            QTableWidget::item {{
                border: 1px solid {c3};  /* Item border */
                padding: 5px;  /* Cell padding */
            }}
            QHeaderView::section {{
                background-color: {c4};  /* Header background */
                color: {c1};  /* Header text color */
                font: 8px Verdana;
                border: 1px solid {c2};  /* Header border */
                padding: 4px;
            }}
            """
        )
        # Return the container
        return container
    
    def create_crud_container(self, widget_title):
        container = QWidget(self)
        container.setStyleSheet("border: none;")
        container.setFixedWidth(250)
        layout = QVBoxLayout(container)

        # Title Label
        label_crud = QLabel(widget_title.upper(), self)
        label_crud.setStyleSheet("font: bold 10px Verdana; color: black;")
        layout.addWidget(label_crud)

        # Horizontal layout for category label and input
        category_layout = QHBoxLayout()
        category_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for category input
        label_category = QLabel("Category:", self)
        label_category.setStyleSheet("font: 10px Verdana; color: black;")
        category_layout.addWidget(label_category)

        # Dropdown (ComboBox) for selecting a category
        self.input_category = QComboBox(self)
        self.input_category.addItems(self.categories)  # Add categories to the dropdown

        # Set default value (e.g., first category)
        default_index = 0  # Change this to the desired index of the default value"
        self.input_category.setCurrentIndex(default_index)

        self.input_category.setStyleSheet(
            """
            QComboBox {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
                width: 180px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            """
        )

        category_layout.addWidget(self.input_category)

        # Add the horizontal layout to the main container layout
        layout.addLayout(category_layout)

        # Horizontal layout for date input with 10px spacing
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)

        # Label for date input
        label_date = QLabel("Date:", self)
        label_date.setStyleSheet("font: 10px Verdana; color: black; padding: 0px; margin: 0")
        date_layout.addWidget(label_date)

        # Date input field with default current date
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)  # Enable calendar dropdown
        self.date_input.setDisplayFormat("yyyy-MM-dd")  # Format the date
        self.date_input.setStyleSheet(
            """
            QDateEdit {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
                width: 180px;
            }
            QCalendarWidget {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                font-size: 12px;
                color: #333;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #f0f0f0;
                selection-background-color: #4CAF50;
                selection-color: white;
                color: #333;
            }
            QCalendarWidget QTableView {
                background-color: #f0f0f0;
                selection-background-color: #4CAF50;
                selection-color: white;
                color: #333;
                border: none;
            }
            QCalendarWidget QTableView::item {
                border: 1px solid #ddd;
                padding: 5px;
                font-size: 12px;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QCalendarWidget QToolButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #45a049;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #388e3c;
            }
        """)

        # Set the current date as default
        self.date_input.setDate(QDate.currentDate()) # Set current date
        date_layout.addWidget(self.date_input)

        # Add the date layout to the main container layout
        layout.addLayout(date_layout)

        # List Widget to display added categories
        # self.list_widget = QListWidget(self)
        # layout.addWidget(self.list_widget)

        # Horizontal layout for amount label and input with 10px spacing
        amount_layout = QHBoxLayout()
        amount_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for amount input
        label_amount = QLabel("Total:", self)
        label_amount.setStyleSheet("font: 10px Verdana; color: black;")
        amount_layout.addWidget(label_amount)

        # Input field for amount with placeholder
        self.input_amount = QLineEdit(self)
        self.input_amount.setPlaceholderText("Enter amount here...")  # Placeholder text
        self.input_amount.setStyleSheet(
            """
            QLineEdit {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            """
        )
        amount_layout.addWidget(self.input_amount)

        # Add the horizontal layout to the main container layout
        layout.addLayout(amount_layout)

        # Add Button to add the data to the table
        self.add_expense_button = QPushButton("Add", self)
        self.add_expense_button.setStyleSheet(
            """
            QPushButton {
                font: 10px Verdana;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            """
        )
        layout.addWidget(self.add_expense_button)

        return container

    def create_configurations_container(self, widget_title):
        container = QWidget(self)
        container.setStyleSheet("border: none;")
        container.setFixedWidth(250)
        layout = QVBoxLayout(container)

        # Title Label
        label_crud = QLabel(widget_title.upper(), self)
        label_crud.setStyleSheet("font: bold 10px Verdana; color: black;")
        layout.addWidget(label_crud)

        # Horizontal layout for date input with 10px spacing
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for date input
        label_date = QLabel("Date:", self)
        label_date.setStyleSheet("font: 10px Verdana; color: black;")
        date_layout.addWidget(label_date)

        # Date input field with default current date
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)  # Enable calendar dropdown
        self.date_input.setDisplayFormat("yyyy-MM-dd")  # Format the date
        self.date_input.setStyleSheet(
            """
            QDateEdit {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
                width: 180px;
            }
            QCalendarWidget {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                font-size: 12px;
                color: #333;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #f0f0f0;
                selection-background-color: #4CAF50;
                selection-color: white;
                color: #333;
            }
            QCalendarWidget QTableView {
                background-color: #f0f0f0;
                selection-background-color: #4CAF50;
                selection-color: white;
                color: #333;
                border: none;
            }
            QCalendarWidget QTableView::item {
                border: 1px solid #ddd;
                padding: 5px;
                font-size: 12px;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QCalendarWidget QToolButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #45a049;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #388e3c;
            }
        """)

        # Set the current date as default
        self.date_input.setDate(QDate.currentDate()) # Set current date
        date_layout.addWidget(self.date_input)

        # Add the date layout to the main container layout
        layout.addLayout(date_layout)

        # Horizontal layout for Total Amount label and input
        total_amount_layout = QHBoxLayout()
        total_amount_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for Total Amountt input
        label_total_amount = QLabel("Total:", self)
        label_total_amount.setStyleSheet("font: 10px Verdana; color: black;")
        total_amount_layout.addWidget(label_total_amount)

        # Input field for Total Amount with placeholder
        self.input_total_amount = QLineEdit(self)
        self.input_total_amount.setPlaceholderText("Enter amount here...")  # Placeholder text
        self.input_total_amount.setStyleSheet(
            """
            QLineEdit {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            """
        )
        total_amount_layout.addWidget(self.input_total_amount)

        # Add the horizontal layout to the main container layout
        layout.addLayout(total_amount_layout)

         # Horizontal layout for category label and input
        category_layout = QHBoxLayout()
        category_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for category input
        label_category = QLabel("Category:", self)
        label_category.setStyleSheet("font: 10px Verdana; color: black;")
        category_layout.addWidget(label_category)

        # Input field for category with placeholder
        self.input_category = QLineEdit(self)
        self.input_category.setPlaceholderText("Enter category here...")  # Placeholder text
        self.input_category.setStyleSheet(
            """
            QLineEdit {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            """
        )
        category_layout.addWidget(self.input_category)

        # Add the horizontal layout to the main container layout
        layout.addLayout(category_layout)


       # Add Button to add the data to the table
        self.add_receipt_button = QPushButton("Add", self)
        self.add_receipt_button.setStyleSheet(
            """
            QPushButton {
                font: 10px Verdana;
                background-color: #4CAF50; 
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            """
        )
        layout.addWidget(self.add_receipt_button)


        return container

    def set_receipt_mode(self):
        self.is_expense = False  # Set to receipt mode (positive amount)

    def set_expense_mode(self):
        self.is_expense = True  # Set to expense mode (negative amount)

    def add_data_to_table(self):
        category = self.input_category.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")  # Get date as string
        amount = self.input_amount.text().strip()

        if category and date and amount:
            try:
                amount = float(amount)  # Convert amount to a number
            except ValueError:
                return  # Handle the error appropriately here

            # Insert data into the Recipes or Expenses table (depending on your use case)
            if self.is_expense:  # Assuming you have a flag to check whether it's expense or recipe
                insert_expense(category, date, amount)
            else:
                insert_recipe(category, date, amount)

            # Reload the table or UI after adding data
            self.update_table()
            self.clear_inputs()

    def remove_selected_row(self):
        selected_row = self.table.currentRow()  # Get the row index of the selected row
        
        if selected_row >= 0:  # Ensure a row is selected
            # Get the ID of the selected row (assuming ID is in the first column)
            item_id = self.table.item(selected_row, 0).text()
            
            try:
                item_id = int(item_id)  # Convert the ID to an integer for deletion
                
                # Check whether to delete from Expenses or Recipes table
                if self.is_expense:
                    delete_expense(item_id)  # Delete from the Expenses table
                else:
                    delete_recipe(item_id)  # Delete from the Recipes table

                # Remove the row from the table
                self.table.removeRow(selected_row)

                # Optional: Show a confirmation message
                QMessageBox.information(self, "Deleted", "Record deleted successfully.")
            except ValueError:
                QMessageBox.warning(self, "Error", "Failed to delete the selected row. Invalid ID.")
        else:
            # Handle case when no row is selected
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")

    def update_table(self):
        """ Refresh the data shown in the table. """
        # Fetch updated data from the database
        if self.is_expense:
            data = see_expenses()
        else:
            data = see_recipes()
        
        # Populate the table with the updated data
        for row_data in data:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_position, col_idx, QTableWidgetItem(str(col_data)))


# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
