import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import subprocess
import mysql.connector
from PIL import Image, ImageTk


def open_login_page():
    root.withdraw()
    login_window.deiconify()


def open_admin_page():
    root.withdraw()
    subprocess.run(["python", "admin.py"])


def open_cashier_page():
    root.withdraw()
    subprocess.run(["python", "cashier.py"])


def clear_fields():
    entry_1.delete(0, tk.END)
    entry_2.delete(0, tk.END)


def login():
    username = entry_1.get()
    password = entry_2.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        user_type = user[4]
        print("Login successful. User type:", user_type)
        if user_type == "admin":
            open_admin_page()
        elif user_type == "cashier":
            open_cashier_page()
        else:
            print("Unknown user type:", user_type)
    else:
        messagebox.showwarning(
            "Error", "Incorreect Username or Password.")
        clear_fields()

    conn.close()


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

# Display the background image on the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


bold_font = tkFont.Font(family="Inter Black", size=15, weight="bold")
font_title = tkFont.Font(family="Inter Black", size=25, weight="bold")


# Create username and password labels directly on the canvas

canvas.create_text(
    250.0,
    40.0,
    anchor="nw",
    text="OFW Bigasan POS System",
    fill="#31304D",
    font=font_title
)
canvas.create_text(360, 180, text="Username",
                   fill="#FFF", font=bold_font)
canvas.create_text(360, 290, text="Password",
                   fill="#FFF", font=bold_font)

# Create entry widgets with minimal background and border
entry_1 = tk.Entry(
    bd=0,
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 17),
    bg=canvas.cget("bg"),  # Set the background to match the canvas background
    insertbackground="black"  # Set cursor color
)
entry_1.place(
    x=310,
    y=200,
    width=309,
    height=45
)

entry_2 = tk.Entry(
    bd=0,
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 17),
    bg=canvas.cget("bg"),  # Set the background to match the canvas background
    show='*',
    insertbackground="black"  # Set cursor color
)
entry_2.place(
    x=310,
    y=310,
    width=309,
    height=45
)

bold_font = tkFont.Font(family="Inter Black", size=18, weight="bold")

button_1 = tk.Button(
    text="Log In",
    bg="#31304D",
    fg="#D3D3D3",
    command=login,
    borderwidth=5,
    relief=tk.RAISED,
    highlightthickness=0,
    font=bold_font
)
button_1.place(
    x=310,
    y=430,
    width=309,
    height=49
)

root.mainloop()
