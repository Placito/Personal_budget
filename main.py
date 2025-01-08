import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
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
        self.setWindowTitle('PyQt Example')
        self.setGeometry(0, 0, 800, 600)
        
        # Set theme (background color)
        self.setStyleSheet(f"background-color: {c9};")

        # Create a layout
        layout = QVBoxLayout(self)

        # Create Frame up
        frame_up = QFrame(self)
        frame_up.setStyleSheet(f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;")
        frame_up.setFixedHeight(80)
        layout.addWidget(frame_up)

        # Add content to the top frame (frame_up)
        try:
            img_path = os.path.join(os.path.dirname(__file__), "log.png")
            print(f"Image path: {img_path}")  # Debugging info
            if os.path.exists(img_path):
                app_img = QPixmap(img_path).scaled(45, 45)  # Load and resize the image
                if app_img.isNull():
                    print("Error: Image could not be loaded.")
                else:
                    # Create QLabel for image and text
                    label_logo = QLabel(self)
                    label_logo.setPixmap(app_img)
                    label_logo.setStyleSheet(f"border: none;")
                    
                    label_text = QLabel("Personal Budget Management", self)
                    label_text.setStyleSheet(f"font: bold 20px Verdana; color: {c4}; border: none;")
                    
                    # Create a horizontal layout for image and text
                    frame_up_layout = QHBoxLayout(frame_up)
                    frame_up_layout.addWidget(label_logo)
                    frame_up_layout.addWidget(label_text)
                    frame_up_layout.setSpacing(10)  # Add spacing between logo and text
                    frame_up_layout.addStretch()  # Push content to the left
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("Error: 'log.png' not found. Skipping image setup.")
            label_logo = QLabel("  Personal budget management", self)
            label_logo.setStyleSheet(f"font: bold 20px Verdana; color: {c4};")
            frame_up_layout = QVBoxLayout(frame_up)
            frame_up_layout.addWidget(label_logo)

        # Frame middle
        frame_middle = QFrame(self)
        frame_middle.setStyleSheet(f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;")
        frame_middle.setFixedHeight(300)
        layout.addWidget(frame_middle)

        # Layouts for positioning
        frame_middle_layout = QVBoxLayout(frame_middle)
        frame_middle_layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
        frame_middle_layout.setSpacing(0)  # Remove any extra spacing

        # Container for label and progress bar
        top_left_layout = QVBoxLayout()  # Vertical layout for the label and progress bar
        top_left_layout.setContentsMargins(10, 10, 10, 0)  # Add padding from the top-left corner
        top_left_layout.setSpacing(5)  # Spacing between the label and progress bar

        # Label
        label_percentage = QLabel("Percentage of income spent:", self)
        label_percentage.setStyleSheet(f"font: bold 10px Verdana; color: {c4}; border: none;")
        top_left_layout.addWidget(label_percentage)

       # Layout for the progress bar and percentage label
        progress_layout = QHBoxLayout()  # Horizontal layout for the bar and percentage
        progress_layout.setSpacing(10)  # Add spacing between the bar and label

        # Progress bar
        bar = QProgressBar(frame_middle)
        bar.setRange(0, 100)  # Set range
        bar.setValue(50)  # Example: Set value to 50%
        bar.setTextVisible(False)  # Hide the text inside the progress bar
        bar.setFixedWidth(120)  # Explicitly set the width of the progress bar
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {c1};  /* Background color */
                border: 2px solid {c2};  /* Border color */
                border-radius: 5px;      /* Rounded corners */
                text-align: center;      /* Align text in the center of the bar */
                color: {c0};             /* Color of the text inside the bar */
            }}
            QProgressBar::chunk {{
                background-color: {c7};  /* Color of the filled portion (chunk) */
                border-radius: 5px;      /* Rounded corners for the chunk */
            }}
        """)
        progress_layout.addWidget(bar)  # Add the bar to the layout

        # Percentage label
        percentage_label = QLabel("50%", frame_middle)  # Display the value as text
        percentage_label.setStyleSheet(f"font: bold 12px Verdana; color: {c0}; border: none;")
        progress_layout.addWidget(percentage_label)  # Add the label next to the bar

        # Add the progress_layout to the main layout
        top_left_layout.addLayout(progress_layout)


        # Add the top-left layout to the frame_middle_layout
        frame_middle_layout.addLayout(top_left_layout)
        frame_middle_layout.addStretch()  # Push remaining content down (if any)

        # Create Frame down
        frame_down = QFrame(self)
        frame_down.setStyleSheet(f"background-color: {c1}; border: 3px solid {c2}; border-radius: 6px;")
        frame_down.setFixedHeight(300)
        layout.addWidget(frame_down)

        # Show the window
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
