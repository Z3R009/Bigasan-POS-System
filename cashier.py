import tkinter as tk
import tkinter.font as tkFont
import subprocess
from PIL import Image, ImageTk


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def open_transaction():
    root.withdraw()
    subprocess.run(["python", "transaction.py"])


def open_manage_users():
    root.withdraw()
    subprocess.run(["python", "manage_users.py"])


def manage_sales():
    root.withdraw()
    subprocess.run(["python", "sales_report_c.py"])


# center window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 4) - (height / 4))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


root = tk.Tk()
root_width = 928
root_height = 536
center_window(root, root_width, root_height)
root.resizable(False, False)

font_title = tkFont.Font(family="Inter Black", size=25, weight="bold")

# Load the background image
bg_image = Image.open("img/c.png")
bg_image = bg_image.resize((root_width, root_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create the login window
login_window = tk.Toplevel(root)
login_window.geometry("928x536")
login_window.configure(bg="#FFFFFF")
login_window.resizable(False, False)
login_window.protocol("WM_DELETE_WINDOW", root.destroy)
login_window.withdraw()

canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=root_height,
    width=root_width,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Display background image
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


# Title
canvas.create_text(
    400.0,
    40.0,
    anchor="nw",
    text="Cashier",
    fill="#31304D",
    font=font_title
)


button_1 = tk.Button(
    text="Transaction",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=open_transaction
)
button_1.place(
    x=310.0,
    y=160.0,
    width=300.0,
    height=60.0
)

button_3 = tk.Button(
    text="Sales Reports",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=manage_sales
)
button_3.place(
    x=310.0,
    y=300.0,
    width=300.0,
    height=60.0
)

button_4 = tk.Button(
    text="Log Out",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=return_to_login
)
button_4.place(
    x=20.0,
    y=470.0,
    width=100.0,
    height=49.0
)

root.mainloop()
