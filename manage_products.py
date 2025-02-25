import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk
import tkinter.font as tkFont
import subprocess
import mysql.connector


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def manage_users():
    root.withdraw()
    subprocess.run(["python", "manage_users.py"])


def manage_sales():
    root.withdraw()
    subprocess.run(["python", "sales_report.py"])


def on_tree_select(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")

    entry_1.delete(0, tk.END)
    entry_1.insert(0, values[1])
    current.delete(0, tk.END)
    current.insert(0, values[2])
    entry_3.delete(0, tk.END)
    entry_3.insert(0, values[3])


# ---------ADD products---------------

def add_product():
    try:
        # retrieve
        product_name = entry_1.get()
        quantity = int(entry_2.get())
        price = float(entry_3.get())

        if quantity < 0 or price < 0:
            messagebox.showwarning("Error", "Negative values are not allowed.")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_sales"
        )
        cursor = conn.cursor()

        cursor.execute("INSERT INTO product (product_name, quantity, price) VALUES (%s, %s, %s)",
                       (product_name, quantity, price))

        conn.commit()
        conn.close()

    except ValueError:
        messagebox.showwarning(
            "Error", "Please enter valid numbers for price and quantity.")
        clear_fields()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    fetch_products(tree)


# --------------UPDATE products------------------------------

def update_product():
    selected_item = tree.selection()
    if not selected_item:
        return  # No item selected

    # Get id
    product_id = tree.item(selected_item[0], 'values')[0]
    product_name = entry_1.get()

    # currentquantity
    current_quantity = int(current.get())

    # inputquantity
    new_quantity = int(entry_2.get())

    quantity = current_quantity + new_quantity

    price = float(entry_3.get())

    if new_quantity < 0 or price < 0:
        messagebox.showwarning("Error", "Negative values are not allowed.")
        return

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE product SET product_name = %s, quantity = %s, price = %s WHERE product_id = %s",
        (product_name, quantity, price, product_id)
    )

    conn.commit()
    conn.close()

    fetch_products(tree)


# ----------DELETE USER------------------

def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        return

    product_id = tree.item(selected_item[0], 'values')[0]

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))

    conn.commit()
    conn.close()

    fetch_products(tree)


# ---------CLEAR-------------------------


def clear_fields():
    entry_1.delete(0, tk.END)
    entry_2.delete(0, tk.END)
    entry_3.delete(0, tk.END)
    current.delete(0, tk.END)


def add_clear():
    add_product()
    clear_fields()


def update_clear():
    update_product()
    clear_fields()


def delete_clear():
    delete_product()
    clear_fields()


# center window

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 4) - (height / 4))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


root = tk.Tk()
root_width = 1200
root_height = 600
center_window(root, root_width, root_height)
root.configure(bg="#FFFFFF")
root.resizable(False, False)

font_title = tkFont.Font(family="Inter Black", size=25, weight="bold")
font_1 = tkFont.Font(family="Inter Black", size=20, weight="bold")


def fetch_products(tree, search_term=None):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    if search_term:
        cursor.execute(
            "SELECT product_id, product_name, quantity, price FROM product WHERE product_name LIKE %s",
            ('%' + search_term + '%',)
        )
    else:
        cursor.execute(
            "SELECT product_id, product_name, quantity, price FROM product"
        )
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        product_id, product_name, quantity, price = row
        tree.insert("", "end", values=(
            product_id, product_name, quantity, price))

    conn.close()

# Function to search products based on the entry in the search box


canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=3000,  # Increase canvas height
    width=3000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Gray background rectangle (sidebar)
canvas.create_rectangle(
    0,
    120,
    250,
    600,
    fill="#9C9A9A",
    outline=""
)

# head
canvas.create_rectangle(
    0,
    0,
    1200,
    110,
    fill="#9C9A9A",
    outline=""
)

# Title text
canvas.create_text(
    50.0,
    40.0,
    anchor="nw",
    text="Manage Products",
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
    highlightthickness=0
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
    highlightthickness=0,
    command=manage_sales
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

# Create a canvas for the rectangle behind the table
table_canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=1000,  # Adjust the height as needed
    width=1000,   # Adjust the width as needed
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
# Adjust the y-coordinate to align with the header
table_canvas.place(x=260, y=120)

# Draw the rectangle
table_canvas.create_rectangle(
    0,
    0,
    600,
    470,
    fill="#9C9A9A",
    outline=""
)

# Create a treeview
tree = ttk.Treeview(root, columns=(
    "ID", "Product Name", "Quantity", "Price"), height=20)

# Define columns
tree.column("#0", anchor=tk.CENTER, width=10)
tree.heading("Product Name", text="Product Name")
tree.column("Product Name", anchor=tk.CENTER, width=250)
tree.heading("Quantity", text="Quantity (By Sack)")
tree.column("Quantity", anchor=tk.CENTER, width=120)
tree.heading("Price", text="Price")
tree.column("Price", anchor=tk.CENTER, width=200)

tree["displaycolumns"] = ("Product Name", "Quantity", "Price")

tree.place(x=270, y=160)  # Adjust the y-coordinate to align with the header

# Bind the select event to the function
tree.bind("<ButtonRelease-1>", on_tree_select)

# Fetch products automatically when window is opened
fetch_products(tree)

# Create a canvas for the rectangle behind the table
add_canvas = tk.Canvas(
    root,
    bg="#FFFFFF",
    height=1000,  # Adjust the height as needed
    width=1000,   # Adjust the width as needed
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
# Adjust the y-coordinate to align with the header
add_canvas.place(x=870, y=120)

# Draw the rectangle
add_canvas.create_rectangle(
    0,
    0,
    320,
    470,
    fill="#9C9A9A",
    outline=""
)

# search

label = tk.Label(
    text="Search:",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
label.place(
    x=270.0,
    y=126.0,
    width=100,
    height=30
)

entry_search = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_search.place(
    x=360.0,
    y=126.0,
    width=220.0,
    height=27.0
)


def search_products(event=None):
    search_term = entry_search.get().strip()
    if not search_term:
        search_term = None  # if empty, return all
    fetch_products(tree, search_term)


entry_search.bind("<KeyRelease>", search_products)

entry_search.bind("<Return>", search_products)


# product name label
name_label = tk.Label(
    text="Product Name",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
name_label.place(
    x=890.0,
    y=140.0,
    width=100,
    height=30
)

# product name Entry
entry_1 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_1.place(
    x=890.0,
    y=168.0,
    width=280.0,
    height=35.0
)

# quantity

label = tk.Label(
    text="Quantity",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
label.place(
    x=890.0,
    y=220.0,
    width=60,
    height=30
)

# new quantity Entry
entry_2 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_2.place(
    x=890.0,
    y=248.0,
    width=280.0,
    height=35.0
)

# curr quan
current = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
current.place(
    x=2000.0,
    y=300.0,
    width=50.0,
    height=35.0
)

# Price label
username_label = tk.Label(
    text="Price",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
username_label.place(
    x=890.0,
    y=290.0,
    width=40,
    height=30
)

# Price Entry
entry_3 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_3.place(
    x=890.0,
    y=320.0,
    width=280.0,
    height=35.0
)

# add Button
button_1 = tk.Button(
    text="Add",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    command=add_clear,
    borderwidth=0,
    highlightthickness=0
)
button_1.place(
    x=890.0,
    y=380.0,
    width=280.0,
    height=42.0
)

# update Button
button_2 = tk.Button(
    text="Update",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    command=update_clear,
    borderwidth=0,
    highlightthickness=0
)
button_2.place(
    x=890.0,
    y=430.0,
    width=280.0,
    height=42.0
)

# delete Button
button_3 = tk.Button(
    text="Delete",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    command=delete_clear,
    borderwidth=0,
    highlightthickness=0
)
button_3.place(
    x=890.0,
    y=480.0,
    width=280.0,
    height=42.0
)

# clear Button
button_4 = tk.Button(
    text="Clear",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    command=clear_fields,
    borderwidth=0,
    highlightthickness=0
)
button_4.place(
    x=890.0,
    y=530.0,
    width=280.0,
    height=42.0
)


root.mainloop()
