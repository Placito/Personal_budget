import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import sys
print("Python version:", sys.version, flush=True)
print("Current directory:", os.getcwd(), flush=True)

from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk

# Colors
c1 = "#feffff"  # white
c4 = "#403d3d"  # letter
c6 = "#038cfc"  # blue
c9 = "#e9edf5"  # fallback background color

# Create the main window
print("Initializing Tkinter window...")
janela = Tk()
print("Tkinter window initialized successfully.")
janela.title("Theme Test")
janela.geometry("900x650")

# Set theme
style = ttk.Style()
try:
    style.theme_use("clam")
except Exception as e:
    print(f"Error applying theme: {e}")

# Theme background fallback
theme_background = style.lookup("TLabel", "background")
if not theme_background:
    theme_background = c9
janela.configure(background=theme_background)

# Frames
frameUp = Frame(janela, width=900, height=50, bg=c1, relief="flat")
frameUp.grid(row=0, column=0, sticky="ew")

# Image and Label
try:
    app_img = Image.open('log.png').resize((45, 45))
    app_img = ImageTk.PhotoImage(app_img)
except FileNotFoundError:
    print("Error: 'log.png' not found. Skipping image setup.")
    app_img = None
except Exception as e:
    print(f"Error loading image: {e}")
    app_img = None

if app_img:
    app_logo = Label(
        frameUp,
        image=app_img,
        text="  Personal budget",
        compound=LEFT,
        font=("Verdana", 20, "bold"),
        bg=c1,
        fg=c4
    )
else:
    app_logo = Label(
        frameUp,
        text="  Personal budget (Image Missing)",
        font=("Verdana", 20, "bold"),
        bg=c1,
        fg=c4
    )
app_logo.place(x=0, y=0)

# Main loop
print("Starting the main loop...")
janela.mainloop()
print("Main loop exited.")
