import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import subprocess
import mysql.connector


def return_to_login():
    root.withdraw()
    subprocess.run(["python", "login.py"])


def manage_products():
    root.withdraw()
    subprocess.run(["python", "manage_products.py"])


def manage_sales():
    root.withdraw()
    subprocess.run(["python", "sales_report.py"])


def fetch_users(tree):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, name, username, password, user_type FROM users")
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        user_id, name, username, password, user_type = row
        # Inserting data into the treeview
        tree.insert("", "end", values=(
            user_id, name, username, password, user_type))

    conn.close()


def on_tree_select(event):
    selected_item = tree.selection()[0]  # Get selected item
    values = tree.item(selected_item, "values")

    entry_1.delete(0, tk.END)
    entry_1.insert(0, values[1])
    entry_2.delete(0, tk.END)
    entry_2.insert(0, values[2])
    entry_3.delete(0, tk.END)
    entry_3.insert(0, values[3])
    user_type_combobox.set(values[4])

# ---------ADD USERS---------------


def add_user():
    name = entry_1.get()
    username = entry_2.get()
    password = entry_3.get()
    user_type = user_type_combobox.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, username, password, user_type) VALUES (%s, %s, %s, %s)",
                   (name, username, password, user_type))

    conn.commit()
    conn.close()

    fetch_users(tree)


# --------------UPDATE USERS------------------------------

def update_user():
    selected_item = tree.selection()
    if not selected_item:
        return  # No item selected

    user_id = tree.item(selected_item[0], 'values')[0]
    name = entry_1.get()
    username = entry_2.get()
    password = entry_3.get()
    user_type = user_type_combobox.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    # Update the user in the database
    cursor.execute(
        "UPDATE users SET name = %s, username = %s, password = %s, user_type = %s WHERE user_id = %s",
        (name, username, password, user_type, user_id)
    )

    conn.commit()
    conn.close()

    fetch_users(tree)


# ----------DELETE USER------------------

def delete_user():
    selected_item = tree.selection()
    if not selected_item:
        return  # No item selected

    # Get the user_id of the selected item
    user_id = tree.item(selected_item[0], 'values')[0]

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_sales"
    )
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

    conn.commit()
    conn.close()

    fetch_users(tree)

# ---------CLEAR-------------------------


def clear_fields():
    entry_1.delete(0, tk.END)
    entry_2.delete(0, tk.END)
    entry_3.delete(0, tk.END)
    user_type_combobox.set('admin')


def add_clear():
    add_user()
    clear_fields()


def update_clear():
    update_user()
    clear_fields()


def delete_clear():
    delete_user()
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
    text="Manage Users",
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
    highlightthickness=0
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
tree = ttk.Treeview(root, columns=("ID", "Name", "Username",
                    "Password", "User Type"), height=20)

# Define columns
tree.column("#0", anchor=tk.CENTER, width=10)
tree.heading("Name", text="Name")
tree.column("Name", anchor=tk.CENTER, width=168)
tree.heading("Username", text="Username")
tree.column("Username", anchor=tk.CENTER, width=100)
tree.heading("Password", text="Password")
tree.column("Password", anchor=tk.CENTER, width=100)
tree.heading("User Type", text="User Type")
tree.column("User Type", anchor=tk.CENTER, width=200)

tree["displaycolumns"] = ("Name", "Username", "Password", "User Type")

tree.place(x=270, y=140)  # Adjust the y-coordinate to align with the header

# Bind the select event to the function
tree.bind("<ButtonRelease-1>", on_tree_select)

# Fetch users automatically when window is opened
fetch_users(tree)

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


# name label
name_label = tk.Label(
    text="Fullname",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
name_label.place(
    x=875.0,
    y=140.0,
    width=100,
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
    y=170.0,
    width=280.0,
    height=35.0
)

# username label
username_label = tk.Label(
    text="Username",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
username_label.place(
    x=875.0,
    y=220.0,
    width=100,
    height=30
)

# username Entry
entry_2 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_2.place(
    x=890.0,
    y=250.0,
    width=280.0,
    height=35.0
)

# password label
password_label = tk.Label(
    text="Password",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
password_label.place(
    x=875.0,
    y=300.0,
    width=100,
    height=30
)

# password Entry
entry_3 = tk.Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter", 12)
)
entry_3.place(
    x=890.0,
    y=330.0,
    width=280.0,
    height=35.0
)

# user type label
usertype_label = tk.Label(
    text="User Type",
    bg="#9C9A9A",
    fg="#31304D",
    font=("Inter", 12)
)
usertype_label.place(
    x=875.0,
    y=380.0,
    width=100,
    height=30
)

# user type dropdown
user_type_combobox = ttk.Combobox(
    root,
    values=["admin", "cashier"],
    font=("Inter", 12),
    state="readonly"
)
user_type_combobox.place(
    x=890.0,
    y=410.0,
    width=280.0,
    height=35.0
)
user_type_combobox.current(0)

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
    y=480.0,
    width=135.0,
    height=35.0
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
    x=1035.0,
    y=480.0,
    width=135.0,
    height=35.0
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
    y=540.0,
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
    y=540.0,
    width=135.0,
    height=35.0
)


root.mainloop()
