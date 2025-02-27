import os
import sys
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
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

        # Initialize totals
        self.total_income = 0
        self.total_expenses = 0
        self.total_balance = 0

        # Fetch categories from the database
        self.categories = self.fetch_categories()
        self.selected_categories = []

        # Set up window
        self.setWindowTitle("PyQt Example")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "log.png")))
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

        # Add initial data
        self.add_initial_data()

    def fetch_categories(self):
        db = Database()
        categories = db.fetchall_query("SELECT name FROM Category")
        return ['Choose a category'] + [category['name'] for category in categories]

    def add_initial_data(self):
        initial_data = [
            {"category": "Salary", "date": "2025-01-01", "amount": 3000, "is_expense": False},
            {"category": "Rent", "date": "2025-01-05", "amount": -1200, "is_expense": True},
            {"category": "Groceries", "date": "2025-01-10", "amount": -300, "is_expense": True},
            {"category": "Freelance Work", "date": "2025-01-15", "amount": 800, "is_expense": False}
        ]

        for data in initial_data:
            self.is_expense = data["is_expense"]
            self.add_data_to_table(data["category"], data["date"], str(data["amount"]))

    def create_top_frame(self):
        """
        Create the top frame of the application which includes the logo and title.
        """
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
        """
        Create the middle frame of the application which includes the progress chart,
        totals container, and circular chart.
        """
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
        """
        Create the bottom frame of the application which includes the tables container,
        CRUD container, configurations container, and remove button.
        """
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

        # CRUD Container, for entering new expenses
        crud_container = self.create_crud_container("Enter new expenses:")
        horizontal_layout.addWidget(crud_container)

        # Configurations Container, for entering new recipes
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
                border: none;
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
        remove_button.setFixedWidth(495)  # Explicitly set the width of the button

        # Create a layout to center the button
        center_layout = QVBoxLayout()
        center_layout.addWidget(remove_button, alignment=Qt.AlignCenter)  # Center the button

        # Add the center layout to the right_layout
        right_layout.addLayout(center_layout)

        # Add the right layout to the frame_down_layout
        frame_down_layout.addLayout(right_layout)

        return frame_down

    def create_progress_chart_container(self):
        """
        Create the progress chart container which includes a progress bar and percentage label.
        """
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
        self.progress_bar = QProgressBar(container)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
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
        self.progress_bar.setFixedSize(120, 20)
        progress_layout.addWidget(self.progress_bar)

        self.percentage_label = QLabel("0%", self)
        self.percentage_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0}; border: none;")
        progress_layout.addWidget(self.percentage_label)
        layout.addLayout(progress_layout)

        return container

    def update_progress_bar(self):
        if self.total_income > 0:
            percentage_spent = (self.total_expenses / self.total_income) * 100
        else:
            percentage_spent = 0
        self.progress_bar.setValue(int(percentage_spent))  # Convert to int
        self.percentage_label.setText(f"{percentage_spent:.2f}%")

    def create_totals_container(self):
        """
        Create the totals container which includes total income, total expenses, and total balance.
        """
        container = QWidget(self)
        container.setFixedWidth(210)
        container.setFixedHeight(200)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Total Income
        self.add_total_item(layout, "Total Monthly Income", self.total_income)

        # Total Expenses
        self.add_total_item(layout, "Total Monthly Expenses", self.total_expenses)

        # Total Balance
        self.add_total_item(layout, "Total Cash Balance", self.total_income - self.total_expenses)

        return container

    def create_circular_container(self):
        """
        Create the circular chart container which includes a pie chart showing income, expenses, and balance.
        """
        container = QWidget(self)
        container.setFixedWidth(500)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Create Matplotlib figure
        figure = plt.Figure(figsize=(4, 3), dpi=100)
        ax = figure.add_subplot(111)

        # Ensure values are non-negative
        total_income = max(self.total_income, 0)
        total_expenses = max(self.total_expenses, 0)
        total_balance = max(total_income - total_expenses, 0)

        # Handle the case where all values are zero
        if total_income == 0 and total_expenses == 0 and total_balance == 0:
            values = [1]  # Dummy value to avoid division by zero
            categories = ["No Data"]
            colors = ["#d3d3d3"]
            explode = [0]
        else:
            values = [total_income, total_expenses, total_balance]
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
            wedgeprops={"width": 0.2, "edgecolor": "white"}
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
        """
        Add a total item to the totals container.
        """
        label_title = QLabel(title.upper(), self)
        label_title.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; border: none;")
        layout.addWidget(label_title)

        label_value = QLabel(f"€ {value:,.2f}".upper(), self)
        label_value.setStyleSheet(
            f"font: bold 17px Arial; color: #545454; border-top: 1px solid {c0};"
        )
        layout.addWidget(label_value)

    def create_tables_container(self):
        """
        Create the tables container which includes a table for displaying income and expenses.
        """
        container = QWidget(self)
        container.setFixedWidth(300)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        table_label = QLabel("Income and Expenses table:", self)
        table_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0};")
        layout.addWidget(table_label)

        self.table = QTableWidget(0, 4, self)  # Set self.table here with 0 initial rows
        self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Date', 'Amount'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Allow row selection

        layout.addWidget(self.table)

        list_Items = [[1, "Salary", "2025-01-01", 3000],
                    [2, "Rent", "2025-01-05", -1200],
                    [3, "Groceries", "2025-01-10", -300],
                    [4, "Freelance Work", "2025-01-15", 800]]

        # Populate the QTableWidget
        for row_idx, row_data in enumerate(list_Items):
            self.table.insertRow(row_idx)
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
        """
        Create the CRUD container which includes inputs for category, date, and amount,
        and a button to add the data to the table.
        """
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
        self.input_category_crud = QComboBox(self)
        self.input_category_crud.addItems(self.categories)  # Add categories to the dropdown

        # Set default value
        self.input_category_crud.setCurrentIndex(0)  # Default index
        self.input_category_crud.setStyleSheet(
            """
            QComboBox {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
                width: 180px;
            }
            """
        )
        category_layout.addWidget(self.input_category_crud)
        layout.addLayout(category_layout)

        # Date input
        date_layout = QHBoxLayout()
        label_date = QLabel("Date:", self)
        label_date.setStyleSheet("font: 10px Verdana; color: black;")
        date_layout.addWidget(label_date)

        self.date_input_crud = QDateEdit(self)
        self.date_input_crud.setCalendarPopup(True)
        self.date_input_crud.setDisplayFormat("yyyy-MM-dd")
        self.date_input_crud.setDate(QDate.currentDate())
        self.date_input_crud.setStyleSheet(
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
        date_layout.addWidget(self.date_input_crud)
        layout.addLayout(date_layout)

        # Amount input
        amount_layout = QHBoxLayout()
        label_amount = QLabel("Total:", self)
        label_amount.setStyleSheet("font: 10px Verdana; color: black;")
        amount_layout.addWidget(label_amount)

        self.input_amount_crud = QLineEdit(self)
        self.input_amount_crud.setPlaceholderText("Enter amount here...")
        self.input_amount_crud.setStyleSheet(
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
        amount_layout.addWidget(self.input_amount_crud)
        layout.addLayout(amount_layout)

        # Add Button
        self.add_expense_button = QPushButton("Add", self)
        self.add_expense_button.clicked.connect(
            lambda: self.add_data_to_table(
                category=self.input_category_crud.currentText().strip(),
                date=self.date_input_crud.date().toString("yyyy-MM-dd"),
                amount=self.input_amount_crud.text().strip(),
            )
        )
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
        """
        Create the configurations container which includes inputs for date, total amount, and category,
        and a button to add the data to the table.
        """
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
        self.date_input_configurations = QDateEdit(self)
        self.date_input_configurations.setCalendarPopup(True)  # Enable calendar dropdown
        self.date_input_configurations.setDisplayFormat("yyyy-MM-dd")  # Format the date
        self.date_input_configurations.setStyleSheet(
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
        self.date_input_configurations.setDate(QDate.currentDate()) # Set current date
        date_layout.addWidget(self.date_input_configurations)

        # Add the date layout to the main container layout
        layout.addLayout(date_layout)

        # Horizontal layout for Total Amount label and input
        total_amount_layout = QHBoxLayout()
        total_amount_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for Total Amount input
        label_total_amount = QLabel("Total:", self)
        label_total_amount.setStyleSheet("font: 10px Verdana; color: black;")
        total_amount_layout.addWidget(label_total_amount)

        # Input field for Total Amount with placeholder
        self.input_total_amount_configurations = QLineEdit(self)
        self.input_total_amount_configurations.setPlaceholderText("Enter amount here...")  # Placeholder text
        self.input_total_amount_configurations.setStyleSheet(
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
        total_amount_layout.addWidget(self.input_total_amount_configurations)

        # Add the horizontal layout to the main container layout
        layout.addLayout(total_amount_layout)

         # Horizontal layout for category label and input
        category_layout = QHBoxLayout()
        category_layout.setSpacing(10)  # Set 10px spacing between widgets

        # Label for category input
        label_category = QLabel("Category:", self)
        label_category.setStyleSheet("font: 10px Verdana; color: black;")
        category_layout.addWidget(label_category)

        # Dropdown (ComboBox) for selecting a category
        self.input_category_configurations = QComboBox(self)
        self.input_category_configurations.addItems(self.categories)  # Add categories to the dropdown

        # Set default value
        self.input_category_configurations.setCurrentIndex(0)  # Default index
        self.input_category_configurations.setStyleSheet(
            """
            QComboBox {
                font: 10px Verdana;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                color: black;
                width: 180px;
            }
            """
        )
        category_layout.addWidget(self.input_category_configurations)
        layout.addLayout(category_layout)

       # Add Button to add the data to the table
        self.add_receipt_button = QPushButton("Add", self)
        self.add_receipt_button.clicked.connect(
            lambda: self.add_data_to_table(
                category=self.input_category_configurations.currentText().strip(),
                date=self.date_input_configurations.date().toString("yyyy-MM-dd"),
                amount=self.input_total_amount_configurations.text().strip(),
            )
        )

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
        self.is_expense = False
        self.clear_inputs()
        print("Receipt mode activated")

    def set_expense_mode(self):
        self.is_expense = True
        self.clear_inputs()
        print("Expense mode activated")

    def add_data_to_table(self, category, date, amount):
        if not category or not amount:  # Check for empty inputs
            self.show_warning("Missing Data", "Please fill out all fields.")
            return

        try:
            amount_value = float(amount)  # Convert amount to float
        except ValueError:
            self.show_warning("Invalid Amount", "Amount must be a valid number.")
            return

        # Determine if it's an expense (negative) or receipt (positive)
        amount_value = -amount_value if self.is_expense else amount_value

        # Add data to the database
        if self.is_expense:
            insert_expense(category, date, amount_value)
            self.total_expenses += amount_value
        else:
            insert_recipe(category, date, amount_value)
            self.total_income += amount_value

        # Update total balance
        self.total_balance = self.total_income - self.total_expenses

        # Add data to the table
        self.add_row_to_table(category, date, f"{amount_value:.2f}")

        # Update UI elements
        self.update_totals()
        self.update_progress_bar()
        self.update_circular_chart()

        # Optional: Clear inputs
        self.clear_inputs()
        self.show_message("Success", "Data added to the table successfully.")

    def add_row_to_table(self, category, date, amount):
        print(f"Adding row: Category={category}, Date={date}, Amount={amount}")
        print(f"Current row count before: {self.table.rowCount()}")  # Debugging row count

        # Insert a new row at the end of the table
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Add items to the respective columns
        self.table.setItem(row_count, 0, QTableWidgetItem(str(row_count + 1)))  # Assuming ID is row_count + 1
        self.table.setItem(row_count, 1, QTableWidgetItem(category))
        self.table.setItem(row_count, 2, QTableWidgetItem(date))
        self.table.setItem(row_count, 3, QTableWidgetItem(amount))

        # Adjust column widths to fit the content
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()  # Adjust row sizes

        # Ensure the table is properly refreshed
        self.table.scrollToBottom()

        print(f"Current row count after: {self.table.rowCount()}")  # Debugging row count after

    def clear_inputs(self):
        self.input_category_crud.setCurrentIndex(0)
        self.input_category_configurations.setCurrentIndex(0)
        self.input_amount_crud.clear()
        self.input_total_amount_configurations.clear()
        self.date_input_crud.setDate(QDate.currentDate())
        self.date_input_configurations.setDate(QDate.currentDate())

    def remove_selected_row(self):
        selected_row = self.table.currentRow()  # Get the row index of the selected row

        # Explicitly check if no row is selected
        if selected_row == -1:  
            self.show_warning("No Selection", "Please select a row to delete.")
            return  # Exit the function early

        # Get the ID of the selected row (assuming ID is in the first column)
        item = self.table.item(selected_row, 0)
        
        if item is None:  # Prevent deleting if there's no valid item
            self.show_warning("Error", "Failed to delete the selected row. No valid ID found.")
            return
        
        item_id = item.text().strip()
        
        try:
            item_id = int(item_id)  # Convert the ID to an integer for deletion
            
            # Check whether to delete from Expenses or Recipes table
            if self.is_expense:
                delete_expense(item_id)  # Delete from the Expenses table
                self.total_expenses -= float(self.table.item(selected_row, 3).text())
            else:
                delete_recipe(item_id)  # Delete from the Recipes table
                self.total_income -= float(self.table.item(selected_row, 3).text())

            # Update total balance
            self.total_balance = self.total_income - self.total_expenses

            # Remove the row from the table
            self.table.removeRow(selected_row)

            # Update UI elements
            self.update_totals()
            self.update_progress_bar()
            self.update_circular_chart()

            # Show a confirmation message
            self.show_message("Deleted", "Record deleted successfully.")
        except ValueError:
            self.show_warning("Error", "Failed to delete the selected row. Invalid ID.")

    def update_totals(self):
        # Refresh the totals container
        totals_container = self.create_totals_container()
        middle_frame_layout = self.layout().itemAt(1).widget().layout()
        old_totals_container = middle_frame_layout.itemAt(1).widget()
        middle_frame_layout.replaceWidget(old_totals_container, totals_container)
        old_totals_container.deleteLater()

    def update_circular_chart(self):
        # Refresh the circular chart container
        circular_container = self.create_circular_container()
        middle_frame_layout = self.layout().itemAt(1).widget().layout()
        old_circular_container = middle_frame_layout.itemAt(2).widget()
        middle_frame_layout.replaceWidget(old_circular_container, circular_container)
        old_circular_container.deleteLater()

    # Helper methods to show styled QMessageBox
    def show_message(self, title, text):
        msg = QMessageBox(self)
        msg.setStyleSheet("QLabel { color: black; }")  # Ensure text is black
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def show_warning(self, title, text):
        msg = QMessageBox(self)
        msg.setStyleSheet(
            """
            QLabel {
                color: red;  /* Change this to your desired color */
            }
            """
        )
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()
        
    def update_table(self):
        self.table.setRowCount(0)

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

        # Refresh the table layout
        self.table.update()
        self.table.resizeRowsToContents()

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
