import os
from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk

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

# Create a window
janela = Tk()
janela.title("Theme Test")
janela.geometry("900x650")

# Set theme
style = ttk.Style()
style.theme_use("clam")  # Use a preferred theme

# Use the background color from the current theme
theme_background = style.lookup("TLabel", "background")
if not theme_background:
    theme_background = c9  # Fallback if theme background is not found

# Configure the main window's background color
janela.configure(background=theme_background)

# Frames (to structure the layout)
frameUp = Frame(janela, width=900, height=50, bg=c1, relief="flat")
frameUp.grid(row=0, column=0, sticky="ew")

frameMiddle = Frame(janela, width=900, height=361, bg=c1, pady=20, relief="raised")
frameMiddle.grid(row=1, column=0, pady=1, padx=0, sticky="nsew")

frameDown = Frame(janela, width=900, height=300, bg=c1, relief="flat")
frameDown.grid(row=2, column=0, pady=1, padx=10, sticky="nsew")

# Ensure layout configuration for frames
janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)
janela.grid_rowconfigure(2, weight=1)
janela.grid_columnconfigure(0, weight=1)

# Add a button to the window
button = ttk.Button(frameMiddle, text="Click Me")
button.grid(row=1, column=0, pady=20)

# Add a label to the window
label = Label(frameMiddle, text="Hello, Tkinter!", bg=theme_background, font=("Arial", 16))
label.grid(row=2, column=0)

# Image and Label for app logo (inside frameUp)
try:
    img_path = os.path.join(os.path.dirname(__file__), "log.png")
    app_img = Image.open(img_path).resize((45, 45))  # Load and resize the image
    app_img = ImageTk.PhotoImage(app_img)

    app_logo = Label(
        frameUp,
        image=app_img,
        text="  Personal budget",
        width=900,
        compound=LEFT,
        padx=5,
        relief=RAISED,
        anchor=NW,
        font=("Verdana", 20, "bold"),
        bg=c1,
        fg=c4
    )
    app_logo.image = app_img  # Keep a reference to the image
    app_logo.grid(row=0, column=0, sticky="w")  # Position the image and text on the left side of the frame

except FileNotFoundError:
    print("Error: 'log.png' not found. Skipping image setup.")
    app_logo = Label(
        frameUp,
        text="  Personal budget",
        width=900,
        padx=5,
        relief=RAISED,
        anchor=NW,
        font=("Verdana", 20, "bold"),
        bg=c1,
        fg=c4
    )
    app_logo.grid(row=0, column=0, sticky="w")  # If no image, just display text

# Debug output
print(f"App logo text: {app_logo.cget('text')}")
print(f"App logo background: {app_logo.cget('background')}")
print(f"App logo image: {app_logo.cget('image')}")

# Run the window
print("Starting the main loop...")
janela.update()  # Ensure the window updates after changes
janela.mainloop()
print("Main loop exited.")
