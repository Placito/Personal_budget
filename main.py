import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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

        frame_middle_layout = QVBoxLayout(frame_middle)
        frame_middle_layout.setContentsMargins(0, 0, 0, 0)
        frame_middle_layout.setSpacing(0)

        top_left_layout = QVBoxLayout()
        top_left_layout.setContentsMargins(10, 10, 10, 0)
        top_left_layout.setSpacing(5)

        label_percentage = QLabel("Percentage of income spent:", self)
        label_percentage.setStyleSheet(f"font: bold 10px Verdana; color: {c4}; border: none;")
        top_left_layout.addWidget(label_percentage)

        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)

        bar = QProgressBar(frame_middle)
        bar.setRange(0, 100)
        bar.setValue(50)
        bar.setTextVisible(False)
        bar.setFixedWidth(120)
        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {c1};
                border: 2px solid {c2};
                border-radius: 5px;
                color: {c0};
            }}
            QProgressBar::chunk {{
                background-color: {c7};
                border-radius: 5px;
            }}
        """
        )
        progress_layout.addWidget(bar)

        percentage_label = QLabel("50%", frame_middle)
        percentage_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0}; border: none;")
        progress_layout.addWidget(percentage_label)

        top_left_layout.addLayout(progress_layout)
        frame_middle_layout.addLayout(top_left_layout)
        frame_middle_layout.addStretch()

        # Chart
        list_categories = ["Income", "Expenses", "Balance"]
        list_values = [3000, 200, 6236]
        colors = [c2, c5, c6]

        figure = plt.Figure(figsize=(4, 3.45), dpi=60)
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

        ax.set_xticklabels(list_categories, fontsize=10)
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
        canvas_container.setContentsMargins(5, 5, 5, 5)
        canvas_container.setFixedWidth(180)
        canvas_container.setStyleSheet("border: none;") 
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.addWidget(canvas)

        # Add the canvas container to the layout
        frame_middle_layout.addWidget(canvas_container)

        # Frame down
        frame_down = QFrame(self)
        frame_down.setStyleSheet(
            f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;"
        )
        frame_down.setFixedHeight(300)
        layout.addWidget(frame_down)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
