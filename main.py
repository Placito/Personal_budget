import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QProgressBar, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

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
            label_logo = QLabel("  Personal budget management", self)
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

        # Progress Bar and Chart Container
        progress_chart_container = self.create_progress_chart_container()
        frame_middle_layout.addWidget(progress_chart_container)

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
        frame_down.setFixedHeight(300)
        frame_down_layout = QHBoxLayout(frame_down)

        # Tables Container
        tables_container = self.create_tables_container()
        frame_down_layout.addWidget(tables_container)

        # CRUD Container
        crud_container = self.create_crud_container("Enter new expenses:")
        frame_down_layout.addWidget(crud_container)

        # Configurations Container
        configurations_container = self.create_crud_container("Enter new recipes:")
        frame_down_layout.addWidget(configurations_container)

        return frame_down

    def create_progress_chart_container(self):
        container = QWidget(self)
        container.setFixedWidth(200)
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

        # Chart Section
        list_categories = ["Income", "Expenses", "Balance"]
        list_values = [3000, 200, 6000]
        colors = [c2, c5, c6]

        figure = plt.Figure(figsize=(4, 4), dpi=60)
        ax = figure.add_subplot(111)
        ax.bar(list_categories, list_values, color=colors, width=0.9)
        for i, rect in enumerate(ax.patches):
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                rect.get_height() + 50,
                f"{list_values[i]}",
                fontsize=10,
                ha="center",
            )
        ax.set_axisbelow(True)
        ax.yaxis.grid(color="#EEEEEE")
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        return container

    def create_totals_container(self):
        container = QWidget(self)
        container.setFixedWidth(200)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        # Total Income
        self.add_total_item(layout, "Total Monthly Income", 500)

        # Total Expenses
        self.add_total_item(layout, "Total Monthly Expenses", 600)

        # Total Balance
        self.add_total_item(layout, "Total Cash Balance", 420)

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

    def create_tables_container(self):
        container = QWidget(self)
        container.setFixedWidth(210)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        table_label = QLabel("Income and Expense table:", self)
        table_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0};")
        layout.addWidget(table_label)

        table = QTableWidget(10, 4, self)
        table.setHorizontalHeaderLabels(['ID', 'Item', 'Date', 'Amount'])
        layout.addWidget(table)

        # Adjust column widths to fit the content
        table.resizeColumnsToContents()

        # Apply style to the table
        table.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {c9};  /* Background color */
                alternate-background-color: {c1};  /* Alternate row background */
                border: 1px solid {c2};  /* Border color */
                color: black;  /* Text color */
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

        return container

    def create_crud_container(self, label_text):
        container = QWidget(self)
        container.setFixedWidth(240)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        crud_label = QLabel("Enter new Expenses:", self)
        crud_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0};")
        layout.addWidget(crud_label)

        # Add additional components for CRUD functionality here
        # For example, text input fields, buttons, etc.
        return container

    def create_configurations_container(self, label_text):
        container = QWidget(self)
        container.setFixedWidth(240)
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)

        configurations_label = QLabel("Enter new Eecipes:", self)
        configurations_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0};")
        layout.addWidget(configurations_label)

        # Add additional components for CRUD functionality here
        # For example, text input fields, buttons, etc.
        return container


# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
