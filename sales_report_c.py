import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter.font as tkFont
import mysql.connector
import subprocess
from datetime import datetime


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def manage_transaction():
    root.withdraw()
    subprocess.run(["python", "transaction.py"])


def fetch_report(tree, selected_date=None):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    if selected_date:
        query = "SELECT report_id, date, customer_name, product_name, quantity, price, total FROM report WHERE DATE(date) = %s"
        cursor.execute(query, (selected_date,))
    else:
        query = "SELECT report_id, date, customer_name, product_name, quantity, price, total FROM report"
        cursor.execute(query)

    rows = cursor.fetchall()
    tree.delete(*tree.get_children())

    for row in rows:
        report_id, date, customer_name, product_name, quantity, price, total = row
        tree.insert("", "end", values=(
            report_id, date, customer_name, product_name, quantity, price, total))

    conn.close()


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 4) - (height / 4))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def on_date_selected(event):
    selected_date = date_entry.get_date().strftime("%Y-%m-%d")
    fetch_report(tree, selected_date)


root = tk.Tk()
root_width = 1200
root_height = 600
center_window(root, root_width, root_height)
root.configure(bg="#FFFFFF")
root.resizable(False, False)

font_title = tkFont.Font(family="Inter Black", size=25, weight="bold")
font_1 = tkFont.Font(family="Inter Black", size=20, weight="bold")

canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=3000,
    width=3000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(
    0,
    120,
    250,
    600,
    fill="#9C9A9A",
    outline=""
)

canvas.create_rectangle(
    0,
    0,
    1200,
    110,
    fill="#9C9A9A",
    outline=""
)

canvas.create_text(
    50.0,
    40.0,
    anchor="nw",
    text="Sales Reports",
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
    command=manage_transaction
)
button_1.place(
    x=0.0,
    y=150.0,
    width=250.0,
    height=49.0
)

button_2 = tk.Button(
    text="Sales Reports",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0
)
button_2.place(
    x=0.0,
    y=250.0,
    width=250.0,
    height=49.0
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
    x=0.0,
    y=530.0,
    width=250.0,
    height=49.0
)

table_canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=1000,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
table_canvas.place(x=260, y=120)

table_canvas.create_rectangle(
    0,
    0,
    930,
    472,
    fill="#9C9A9A",
    outline=""
)

tree = ttk.Treeview(root, columns=("ID", "Date", "Customer Name", "Product Name", "Quantity",
                    "Price", "Total"), height=21)

tree.column("#0", anchor=tk.CENTER, width=10)
tree.heading("Date", text="Date")
tree.column("Date", anchor=tk.CENTER, width=110)
tree.heading("Customer Name", text="Customer Name")
tree.column("Customer Name", anchor=tk.CENTER, width=180)
tree.heading("Product Name", text="Product Name")
tree.column("Product Name", anchor=tk.CENTER, width=150)
tree.heading("Quantity", text="Quantity (By Sack)")
tree.column("Quantity", anchor=tk.CENTER, width=110)
tree.heading("Price", text="Price")
tree.column("Price", anchor=tk.CENTER, width=170)
tree.heading("Total", text="Total")
tree.column("Total", anchor=tk.CENTER, width=180)

tree["displaycolumns"] = (
    "Date", "Customer Name", "Product Name", "Quantity", "Price", "Total")

tree.place(x=270, y=135)


# Fetch today's data automatically when window is opened
today = datetime.today().strftime("%Y-%m-%d")
fetch_report(tree, today)

root.mainloop()
