import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
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
        # Set theme (background color)
        self.setStyleSheet(f"background-color: {c9};")

        # Create a layout
        layout = QVBoxLayout(self)

        # Create Frame up
        frame_up = QFrame(self)
        frame_up.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )
        frame_up.setFixedHeight(80)
        layout.addWidget(frame_up)

        # Add content to the top frame (frame_up)
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

        # Frame middle
        frame_middle = QFrame(self)
        frame_middle.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"  
        )
        frame_middle.setFixedHeight(300)
        layout.addWidget(frame_middle)

        # Create the main layout for frame_middle (HBoxLayout)
        frame_middle_layout = QHBoxLayout(frame_middle)

        # Container for Progress Bar and Chart
        progress_chart_container = QWidget(self)
        progress_chart_container.setFixedWidth(200)
        progress_chart_container.setStyleSheet("border: none;")
        progress_chart_layout = QVBoxLayout(progress_chart_container)

        top_left_layout = QVBoxLayout()
        top_left_layout.setContentsMargins(10, 10, 10, 0)
        top_left_layout.setSpacing(5)

        label_percentage = QLabel("Percentage of income spent:", self)
        label_percentage.setStyleSheet(f"font: bold 10px Verdana; color: {c4}; border: none;")
        top_left_layout.addWidget(label_percentage)

       # Progress Bar layout
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)

        bar = QProgressBar(frame_middle)
        bar.setRange(0, 100)
        bar.setValue(50)
        bar.setTextVisible(False)

        # Set a simpler style for the progress bar
        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {c9};  /* Background color */
                border: 1px solid {c0};  /* Border color */
                border-radius: 5px;      /* Rounded corners */
            }}
            QProgressBar::chunk {{
                background-color: {c7};  /* Progress color */
                border-radius: 5px;      /* Rounded corners for progress */
            }}
            """
        )

        # Set the width and height of the progress bar
        bar.setFixedWidth(120)  # Adjust as needed
        bar.setFixedHeight(20)  # Adjust height to fit

        # Add the progress bar and percentage label to the layout
        percentage_label = QLabel("50%", frame_middle)
        percentage_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0}; border: none;")
        progress_layout.addWidget(bar)
        progress_layout.addWidget(percentage_label)

        # Add this layout to the parent container layout
        top_left_layout.addLayout(progress_layout)
        progress_chart_layout.addLayout(top_left_layout)

        # Chart
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

        ax.set_xticks(range(len(list_categories)))  # Define tick positions
        ax.set_xticklabels(list_categories, fontsize=10)  # Apply labels            
        ax.patch.set_facecolor(c1)
        ax.spines["bottom"].set_color(c3)
        ax.spines["bottom"].set_linewidth(1)
        ax.spines["left"].set_color(c3)
        ax.spines["left"].set_linewidth(1)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color="#EEEEEE")
        ax.xaxis.grid(False)

        canvas = FigureCanvas(figure)

        # Wrap the canvas in a QWidget to apply margins
        canvas_container = QWidget(self)
        canvas_container.setFixedWidth(200)
        canvas_container.setStyleSheet("border: none;") 
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.addWidget(canvas)

        # Add the canvas container to the progress chart container
        progress_chart_layout.addWidget(canvas_container)

        # Container for the Totals
        totals_container = QWidget(self)
        totals_container.setFixedWidth(200)
        totals_container.setFixedHeight(180)
        totals_container.setStyleSheet("border: none;") 
        totals_layout = QVBoxLayout(totals_container)

        # Values to display
        values = [500, 600, 420]

        # Total Monthly Income
        income_label = QLabel(f"Total Monthly Income".upper(), self)
        income_label.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; background-color: {c1}; border: none")
        income_value_label = QLabel(f"€ {values[0]:,.2f}".upper(), self)
        income_value_label.setStyleSheet(f"font: bold 17px Arial; color: #545454; background-color: {c1}; border-top: 1px solid {c0};")

        # Total Monthly Expenses
        expenses_label = QLabel(f"Total Monthly Expenses".upper(), self)
        expenses_label.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; background-color: {c1}; border: none")
        expenses_value_label = QLabel(f"€ {values[1]:,.2f}".upper(), self)
        expenses_value_label.setStyleSheet(f"font: bold 17px Arial; color: #545454; background-color: {c1}; border-top: 1px solid {c0};")

        # Total Cash Balance
        balance_label = QLabel(f"Total Cash Balance".upper(), self)
        balance_label.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; background-color: {c1}; border: none")
        balance_value_label = QLabel(f"€ {values[2]:,.2f}".upper(), self)
        balance_value_label.setStyleSheet(f"font: bold 17px Arial; color: #545454; background-color: {c1}; border-top: 1px solid {c0};")

        # Add the labels and rows to the totals layout
        totals_layout.addWidget(income_label)
        totals_layout.addWidget(income_value_label)

        totals_layout.addWidget(expenses_label)
        totals_layout.addWidget(expenses_value_label)

        totals_layout.addWidget(balance_label)
        totals_layout.addWidget(balance_value_label)

        # Container for Donut Chart
        circular_container = QWidget(self)
        circular_container.setFixedWidth(500)
        circular_container.setStyleSheet("border: none;") 
        circular_layout = QVBoxLayout(circular_container)

        # Donut Chart
        chart_figure = plt.Figure(figsize=(3.5, 3), dpi=100)
        chart_ax = chart_figure.add_subplot(111)

        values = [345, 225, 534]
        categories = ["Income", "Expenses", "Balance"]
        colors = ["#4fa882", "#038cfc", "#e06636"]
        explode = [0.05, 0.05, 0.05]

        wedges, _, autotexts = chart_ax.pie(
            values,
            autopct="%1.1f%%",
            colors=colors,
            explode=explode,
            startangle=90,
            wedgeprops={"width": 0.4, "edgecolor": "white"},
        )

        chart_ax.legend(
            wedges, categories, title="Categories:", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
        )

        chart_canvas = FigureCanvas(chart_figure)
        circular_layout.addWidget(chart_canvas)

        # Add layouts to frame_middle
        frame_middle_layout.addWidget(progress_chart_container)
        frame_middle_layout.addWidget(totals_container)
        frame_middle_layout.addWidget(circular_container)

        # Frame down
        frame_down = QFrame(self)
        frame_down.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )
        frame_down.setFixedHeight(300)
        layout.addWidget(frame_down)

        frame_down_layout = QHBoxLayout(frame_down)
        
        # Container for the tables
        tables_container = QWidget(self)
        tables_container.setFixedWidth(300)
        tables_container.setStyleSheet("border: none;") 
        tables_layout = QVBoxLayout(tables_container)

        # Add table label to the tables layout
        table_label = QLabel(f"Income and Expense table:", self)
        table_label.setStyleSheet(f"font: bold 12px Verdana; color: #83a9e6; background-color: {c1}; border: none")
        tables_layout.addWidget(table_label)  # Add the label to the layout

        # Set the layout for tables_container
        tables_container.setLayout(tables_layout)

        # Container for the CRUD
        crud_container = QWidget(self)
        crud_container.setFixedWidth(100)
        crud_container.setStyleSheet("border: none;") 
        crud_layout = QVBoxLayout(crud_container)

        # Container for the expenses
        expenses_container = QWidget(self)
        expenses_container.setFixedWidth(100)
        expenses_container.setStyleSheet("border: none;") 
        expenses_layout = QVBoxLayout(expenses_container)

        # Add layouts to frame_down
        frame_down_layout.addWidget(tables_container)
        frame_down_layout.addWidget(crud_container)
        frame_down_layout.addWidget(expenses_container)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
