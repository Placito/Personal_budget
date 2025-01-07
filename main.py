import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtGui import QPixmap
import os

# Colors
c0 = "#2e2d2b"  # black
c1 = "#feffff"  # white
c2 = "#4fa882"  # green
c3 = "#38576b"  # value
c4 = "#403d3d"  # letter
c5 = "#e06636"  # profit
c6 = "#038cfc"  # blue
c7 = "#3fbfb9"  # another green
c8 = "#263238"  # another green
c9 = "#e9edf5"  # another green

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up window
        self.setWindowTitle('PyQt Example')
        self.setGeometry(100, 100, 800, 600)
        
        # Set theme (background color)
        self.setStyleSheet(f"background-color: {c9};")

        # Create a layout
        layout = QVBoxLayout(self)

        # Create Frames
        frame_up = QFrame(self)
        frame_up.setStyleSheet(f"background-color: {c1};")
        frame_up.setFixedHeight(50)
        layout.addWidget(frame_up)

        frame_middle = QFrame(self)
        frame_middle.setStyleSheet(f"background-color: {c1};")
        frame_middle.setFixedHeight(100)
        layout.addWidget(frame_middle)

        frame_down = QFrame(self)
        frame_down.setStyleSheet(f"background-color: {c1};")
        frame_down.setFixedHeight(100)
        layout.addWidget(frame_down)

        # Add content to the top frame (frame_up)
        try:
            img_path = os.path.join(os.path.dirname(__file__), "log.png")
            if os.path.exists(img_path):  # Ensure file exists
                app_img = QPixmap(img_path).scaled(45, 45)  # Load and resize the image
                if app_img.isNull():
                    print("Error: Image could not be loaded.")
                else:
                    label_logo = QLabel(self)
                    label_logo.setPixmap(app_img)
                    label_logo.setText("  Personal budget management")
                    label_logo.setStyleSheet(f"font: bold 20px Verdana; color: {c4};")
                    frame_up_layout = QVBoxLayout(frame_up)
                    frame_up_layout.addWidget(label_logo)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("Error: 'log.png' not found. Skipping image setup.")
            label_logo = QLabel("  Personal budget management", self)
            label_logo.setStyleSheet(f"font: bold 20px Verdana; color: {c4};")
            frame_up_layout = QVBoxLayout(frame_up)
            frame_up_layout.addWidget(label_logo)

        # Add content to the middle frame (frame_middle)
        frame_middle_layout = QVBoxLayout(frame_middle)


        # Show the window
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
