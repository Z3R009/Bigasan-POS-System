import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import subprocess
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import mysql.connector


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def manage_users():
    root.withdraw()
    subprocess.run(["python", "manage_users.py"])


def manage_products():
    root.withdraw()
    subprocess.run(["python", "manage_products.py"])


def fetch_report(tree, selected_month):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    if selected_month == "Select Month" or not selected_month:
        cursor.execute(
            "SELECT report_id, date, customer_name, product_name, quantity, price, total FROM report")
    else:
        month_number = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }[selected_month]
        cursor.execute(
            f"SELECT report_id, date, customer_name, product_name, quantity, price, total FROM report WHERE MONTH(date) = {month_number}")

    rows = cursor.fetchall()
    tree.delete(*tree.get_children())

    for row in rows:
        report_id, date, customer_name, product_name, quantity, price, total = row
        tree.insert("", "end", values=(
            report_id, date, customer_name, product_name, quantity, price, total))

    conn.close()


def calculate_total(tree, entry_widget):
    total = 0
    for child in tree.get_children():
        total += float(tree.item(child, "values")[-1])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, f"{total:.2f}")


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 4) - (height / 4))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def on_month_selected(event):
    selected_month = month_combobox.get()
    fetch_report(tree, selected_month)
    calculate_total(tree, entry_1)


def print_report():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if not file_path:
        return  # User cancelled the save dialog

    c = pdf_canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 40, "Sales Report")

    c.setFont("Helvetica", 12)
    data = [tree.item(child, "values") for child in tree.get_children()]

    headers = ["Date", "Customer Name",
               "Product Name", "Quantity", "Price", "Total"]
    x_offsets = [10, 100, 220, 350, 450, 550]
    y_offset = height - 80
    row_height = 20

    for i, header in enumerate(headers):
        c.drawString(x_offsets[i], y_offset, header)

    y_offset -= row_height
    for row in data:
        for i, cell in enumerate(row[1:]):  # Adjust indexing to match headers
            c.drawString(x_offsets[i], y_offset, str(cell))
        y_offset -= row_height

    # Add the total value to the PDF
    total_value = entry_1.get()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y_offset - row_height, f"Total Value: {total_value}")

    c.save()


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
    text="Manage Users",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=manage_users
)
button_1.place(
    x=0.0,
    y=150.0,
    width=250.0,
    height=49.0
)

button_2 = tk.Button(
    text="Manage Products",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=manage_products
)
button_2.place(
    x=0.0,
    y=250.0,
    width=250.0,
    height=49.0
)

button_3 = tk.Button(
    text="Sales Reports",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0
)
button_3.place(
    x=0.0,
    y=350.0,
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
    470,
    fill="#9C9A9A",
    outline=""
)

tree = ttk.Treeview(root, columns=("ID", "Date", "Customer Name", "Product Name", "Quantity",
                    "Price", "Total"), height=18)

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

tree["displaycolumns"] = ("Date", "Customer Name",
                          "Product Name", "Quantity", "Price", "Total")

tree.place(x=270, y=140)

fetch_report(tree, None)

label = tk.Label(
    text="Total:",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
label.place(
    x=280.0,
    y=543.0,
    width=60,
    height=30
)

entry_1 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_1.place(
    x=340.0,
    y=540.0,
    width=250.0,
    height=35.0
)

calculate_total(tree, entry_1)

month_combobox = ttk.Combobox(
    root,
    values=["Select Month", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"],
    font=("Inter", 12),
    state="readonly"
)
month_combobox.current(0)
month_combobox.place(
    x=630.0,
    y=540.0,
    width=280.0,
    height=35.0
)

print_button = tk.Button(
    text="Save Report",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=0,
    highlightthickness=0,
    command=print_report
)
print_button.place(
    x=970.0,
    y=540.0,
    width=200.0,
    height=35.0
)

month_combobox.bind("<<ComboboxSelected>>", on_month_selected)

root.mainloop()
