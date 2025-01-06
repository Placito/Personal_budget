import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

from tkinter import *
from tkinter import Tk, ttk

# colors
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

colors = ["#5588bb", "#66bbbb", "#99bb55", "#ee9944", "#444466", "bb5555"]

# Create a window
janela = Tk()
janela.title("Theme Test")
janela.geometry("900x650")

# Set theme
style = ttk.Style()

# Print available themes for debugging
print("Available themes:", style.theme_names())

# Try to use 'clam' or any other available theme
try:
    style.theme_use("clam")  
except Exception as e:
    print(f"Error applying theme: {e}")

# Use the background color from the current theme
theme_background = style.lookup("TLabel", "background")
if not theme_background:
    theme_background = c9  # Fallback to custom color if no theme background is found
janela.configure(background=theme_background)

# Add a sample button
button = ttk.Button(janela, text="Click Me")
button.pack(pady=20)

# Add a label
label = Label(janela, text="Hello, Tkinter!", bg=theme_background, font=("Arial", 16))
label.pack()

# create frames for division of window
frameUp = Frame(janela, width=1043, height=50, bg=c1, relief="flat")
frameUp.grid(row=0, column=0, sticky="ew")

frameMiddle = Frame(janela, width=1043, height=361, bg=c1, pady=20, relief="raised")
frameMiddle.grid(row=1, column=0, pady=1, padx=0, sticky="nsew")

frameDown = Frame(janela, width=1043, height=300, bg=c1, relief="flat")
frameDown.grid(row=2, column=0, pady=1, padx=10, sticky="nsew")

# Allow the grid to expand
janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)
janela.grid_rowconfigure(2, weight=1)
janela.grid_columnconfigure(0, weight=1)

# Run the window
janela.mainloop()
