import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import subprocess
import mysql.connector


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def manage_sales():
    root.withdraw()
    # Open the login page window
    subprocess.run(["python", "sales_report_c.py"])


def fetch_product(tree):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    # Select products with quantity greater than zero
    cursor.execute(
        "SELECT product_id, product_name, quantity, price FROM product WHERE quantity >= 1"
    )
    rows = cursor.fetchall()

    # Clear existing items in the tree
    tree.delete(*tree.get_children())

    # Insert new data into the tree
    for row in rows:
        product_id, product_name, quantity, price = row
        tree.insert("", "end", values=(
            product_id, product_name, quantity, price
        ))

    conn.close()


def fetch_cart(tree_cart):
    global total2
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cart_id, customer_name, product_name, price, quantity, total FROM cart")
    rows = cursor.fetchall()
    tree_cart.delete(*tree_cart.get_children())
    for row in rows:
        cart_id, customer_name,  product_name, price, quantity, total = row
        tree_cart.insert("", "end", values=(
            cart_id, customer_name,  product_name, price, quantity, total))
    conn.close()
    update_total_cart()


def update_total_cart():
    global total2
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_sales"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total) FROM cart")
        total_sum = cursor.fetchone()[0]
        if total_sum is None:
            total_sum = 0.0
        total2.config(state=tk.NORMAL)
        total2.delete(0, tk.END)
        # Format the total as 0.00
        total2.insert(0, "{:.2f}".format(total_sum))
        total2.config(state='readonly')
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def on_tree_select(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")
    entry_2.config(state=tk.NORMAL)  # Enable the field to update the value
    entry_2.delete(0, tk.END)
    entry_2.insert(0, values[1])
    entry_2.config(state='readonly')  # Make the field read-only again
    entry_3.config(state=tk.NORMAL)  # Enable the field to update the value
    entry_3.delete(0, tk.END)
    entry_3.insert(0, values[3])
    entry_3.config(state='readonly')


def add_cart():
    try:
        customer_name = entry_1.get()
        product_name = entry_2.get()
        price = float(entry_3.get())
        quantity = int(entry_4.get())
        total = price * quantity

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_sales"
        )
        cursor = conn.cursor()

        # Check current stock
        cursor.execute(
            "SELECT quantity FROM product WHERE product_name = %s", (product_name,))
        current_stock = cursor.fetchone()[0]

        if current_stock < quantity:
            messagebox.showwarning("Stock Error", "Stock is not enough.")
            return

        # Subtract quantity from stock
        new_stock = current_stock - quantity
        cursor.execute(
            "UPDATE product SET quantity = %s WHERE product_name = %s", (new_stock, product_name))

        # Add to cart
        cursor.execute("INSERT INTO cart (customer_name, product_name, price, quantity, total) VALUES (%s, %s, %s, %s, %s)",
                       (customer_name, product_name, price, quantity, total))

        # Commit changes to database
        conn.commit()

        # Fetch updated cart
        fetch_cart(tree_cart)

        # Fetch updated product list
        fetch_product(tree)

        conn.close()

    except ValueError:
        messagebox.showwarning(
            "Error", "Please enter valid numbers for quantity.")
        clear_fields()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")


# truncate


def truncate_table():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_sales"
        )
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE cart")
        conn.commit()
        conn.close()
        print("Table 'cart' truncated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


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
            "SELECT product_id, product_name, quantity, price FROM product WHERE quantity >= 1 and product_name LIKE %s",
            ('%' + search_term + '%',)
        )
    else:
        cursor.execute(
            "SELECT product_id, product_name, quantity, price FROM product WHERE quantity >= 1"
        )
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        product_id, product_name, quantity, price = row
        tree.insert("", "end", values=(
            product_id, product_name, quantity, price))

    conn.close()

# ---------CLEAR-------------------------


def clear_fields():
    entry_1.delete(0, tk.END)
    entry_2.delete(0, tk.END)
    entry_2.config(state='normal')
    entry_2.delete(0, tk.END)
    entry_2.config(state='readonly')
    entry_3.delete(0, tk.END)
    entry_3.config(state='normal')
    entry_3.delete(0, tk.END)
    entry_3.config(state='readonly')
    entry_4.delete(0, tk.END)
    entry_5.config(state=tk.NORMAL)
    entry_5.delete(0, tk.END)
    entry_5.config(state='readonly')


def add_clear():
    add_cart()
    entry_2.delete(0, tk.END)
    entry_2.config(state='normal')
    entry_2.delete(0, tk.END)
    entry_2.config(state='readonly')
    entry_3.delete(0, tk.END)
    entry_3.config(state='normal')
    entry_3.delete(0, tk.END)
    entry_3.config(state='readonly')
    entry_4.delete(0, tk.END)
    entry_5.config(state=tk.NORMAL)
    entry_5.delete(0, tk.END)
    entry_5.config(state='readonly')


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
    90,
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
    80,
    fill="#9C9A9A",
    outline=""
)

bold_font = tkFont.Font(family="Inter Black", size=15, weight="bold")
# Title text
canvas.create_text(
    50.0,
    23.0,
    anchor="nw",
    text="Transaction",
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
    highlightthickness=0,
    command=manage_sales
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
table_canvas.place(x=260, y=90)

# Draw the rectangle
table_canvas.create_rectangle(
    0,
    0,
    600,
    500,
    fill="#9C9A9A",
    outline=""
)

# Create a treeview for product
tree = ttk.Treeview(root, columns=(
    "Product ID", "Product Name", "Quantity", "Price"), height=8)

# Define columns
tree.column("#0", anchor=tk.CENTER, width=10)
tree.heading("Product Name", text="Product Name")
tree.column("Product Name", anchor=tk.CENTER, width=270)
tree.heading("Quantity", text="Quantity")
tree.column("Quantity", anchor=tk.CENTER, width=100)
tree.heading("Price", text="Price")
tree.column("Price", anchor=tk.CENTER, width=200)

tree["displaycolumns"] = ("Product Name", "Quantity", "Price")

tree.place(x=270, y=130)  # Adjust the y-coordinate to align with the header

# Bind the select event to the function
tree.bind("<ButtonRelease-1>", on_tree_select)

# Fetch users automatically when window is opened
fetch_product(tree)


def calculate_total(event):
    try:
        price = float(entry_3.get())
        quantity = int(entry_4.get())
        total = price * quantity
        entry_5.config(state=tk.NORMAL)  # Enable the field to update the value
        entry_5.delete(0, tk.END)
        entry_5.insert(0, str(total))
        entry_5.config(state='readonly')  # Make the field read-only again
    except ValueError:
        entry_5.config(state=tk.NORMAL)  # Enable the field to update the value
        entry_5.delete(0, tk.END)
        entry_5.insert(0, "Error")
        entry_5.config(state='readonly')


def calculate_total_cart(event):
    try:
        total = float(total2.get())
        cash = float(cash2.get())
        change_amount = cash - total
        change.config(state=tk.NORMAL)  # Enable the field to update the value
        change.delete(0, tk.END)
        change.insert(0, str(change_amount))
        change.config(state='readonly')  # Make the field read-only again
    except ValueError:
        change.config(state=tk.NORMAL)  # Enable the field to update the value
        change.delete(0, tk.END)
        change.insert(0, "Error")
        change.config(state='readonly')


# Create a canvas for the rectangle behind the add transaction
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
add_canvas.place(x=870, y=90)

# Draw the rectangle
add_canvas.create_rectangle(
    0,
    0,
    320,
    500,
    fill="#9C9A9A",
    outline=""
)

# Add the text for "Add User" above the rectangle
add_canvas.create_text(
    160.0,
    10.0,
    anchor="n",
    text="Add Transaction",
    fill="#31304D",
    font=font_1
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
    y=98.0,
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
    y=98.0,
    width=220.0,
    height=27.0
)


def search_products(event=None):
    search_term = entry_search.get().strip()
    if not search_term:
        search_term = None  # If search term is empty, set to None to fetch all products
    fetch_products(tree, search_term)


entry_search.bind("<KeyRelease>", search_products)


# Bind the search function to <Return> key press event
entry_search.bind("<Return>", search_products)

# name label
name_label = tk.Label(
    text="Customer Name",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
name_label.place(
    x=890.0,
    y=150.0,
    width=120,
    height=30
)

# name Entry
entry_1 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_1.place(
    x=890.0,
    y=180.0,
    width=280.0,
    height=35.0
)

# product label
product_label = tk.Label(
    text="Product Name",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
product_label.place(
    x=884.0,
    y=230.0,
    width=120,
    height=30
)

# product Entry
entry_2 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12),
    state='readonly'
)
entry_2.place(
    x=890.0,
    y=260.0,
    width=280.0,
    height=35.0
)

# price label
price_label = tk.Label(
    text="Price",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
price_label.place(
    x=888.0,
    y=300.0,
    width=50,
    height=30
)

# price Entry
entry_3 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12),
    state='readonly'
)
entry_3.place(
    x=890.0,
    y=330.0,
    width=280.0,
    height=35.0
)

# qty label
quantity_label = tk.Label(
    text="Quantity (By Sack)",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
quantity_label.place(
    x=880.0,
    y=370.0,
    width=150,
    height=30
)

# qty Entry
entry_4 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_4.place(
    x=890.0,
    y=400.0,
    width=280.0,
    height=35.0
)

entry_4.bind("<KeyRelease>", calculate_total)

# total label
total_label = tk.Label(
    text="Total",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
total_label.place(
    x=890.0,
    y=440.0,
    width=50,
    height=30
)

# total Entry
entry_5 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12),
    state='readonly'
)
entry_5.place(
    x=890.0,
    y=470.0,
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
    y=530.0,
    width=135.0,
    height=35.0
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
    x=1035.0,
    y=530.0,
    width=135.0,
    height=35.0
)

# Create a treeview for cart
tree_cart = ttk.Treeview(root, columns=(
    "Cart ID", "Customer Name", "Product Name", "Price", "Quantity", "Total"), height=7)

# Define columns
tree_cart.column("#0", anchor=tk.CENTER, width=10)
tree_cart.heading("Customer Name", text="Customer Name")
tree_cart.column("Customer Name", anchor=tk.CENTER, width=10)
tree_cart.heading("Product Name", text="Product Name")
tree_cart.column("Product Name", anchor=tk.CENTER, width=169)
tree_cart.heading("Price", text="Price")
tree_cart.column("Price", anchor=tk.CENTER, width=120)
tree_cart.heading("Quantity", text="Quantity (By Sack)")
tree_cart.column("Quantity", anchor=tk.CENTER, width=120)
tree_cart.heading("Total", text="Total")
tree_cart.column("Total", anchor=tk.CENTER, width=160)

tree_cart["displaycolumns"] = ("Product Name", "Price", "Quantity", "Total")

# Adjust the y-coordinate to align with the header
tree_cart.place(x=270, y=320)

# Bind the select event to the function
tree_cart.bind("<ButtonRelease-1>", on_tree_select)

# Fetch users automatically when window is opened
fetch_cart(tree_cart)


# total_cart label
total2_label = tk.Label(
    text="Total:",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12),
)
total2_label.place(
    x=270.0,
    y=490.0,
    width=50,
    height=30
)

# total cart Entry
total2 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12),
    state='readonly'
)
total2.place(
    x=340.0,
    y=490.0,
    width=200.0,
    height=35.0
)

# change label
change_label = tk.Label(
    text="Change:",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
change_label.place(
    x=565.0,
    y=490.0,
    width=80,
    height=30
)

# change Entry
change = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
change.place(
    x=650.0,
    y=490.0,
    width=200.0,
    height=35.0
)

# cash label
cash_label = tk.Label(
    text="Cash:",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
cash_label.place(
    x=270.0,
    y=550.0,
    width=50,
    height=30
)


# cash Entry
cash2 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
cash2.place(
    x=340.0,
    y=550.0,
    width=200.0,
    height=35.0
)

cash2.bind("<KeyRelease>", calculate_total_cart)


def pay_and_generate_report():
    try:
        total_amount = float(total2.get())
        cash = float(cash2.get())
        change_amount = cash - total_amount

        if change_amount < 0:
            change.config(state=tk.NORMAL)
            change.delete(0, tk.END)
            change.insert(0, "Invalid")
            change.config(state='readonly')
            messagebox.showwarning(
                "Error", "Insufficient Cash.")
            cash2.delete(0, tk.END)
            return

        change.config(state=tk.NORMAL)
        change.delete(0, tk.END)
        change.insert(0, str(change_amount))
        change.config(state='readonly')

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_sales"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cart")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("INSERT INTO report (customer_name, product_name, price, quantity, total) VALUES (%s, %s, %s, %s, %s)",
                           (row[1], row[2], row[3], row[4], row[5]))
        conn.commit()
        conn.close()

        truncate_table()  # Clear the cart after adding to report
        fetch_cart(tree_cart)  # Refresh the cart display
        clear_fields()  # Clear input fields
        update_total_cart()  # Update total amount in cart
        cash2.delete(0, tk.END)  # Clear cash input
        change.config(state=tk.NORMAL)
        change.delete(0, tk.END)
        change.config(state='readonly')
    except ValueError:
        print("Please enter valid numbers for total and cash.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


pay_button = tk.Button(
    text="Pay",
    bg="#31304D",
    fg="#D3D3D3",
    font=("Inter Black", 15),
    borderwidth=2,
    relief=tk.RAISED,
    highlightthickness=0,
    command=pay_and_generate_report
)

pay_button.place(
    x=580.0,
    y=550.0,
    width=270.0,
    height=35.0
)


root.mainloop()
