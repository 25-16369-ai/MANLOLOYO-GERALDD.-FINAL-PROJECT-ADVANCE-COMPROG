import tkinter as tk
from tkinter import messagebox
import json
import os

inventory = []

# ------------------- SAVE & LOAD FUNCTIONS -------------------
DATA_FILE = "inventory_data.txt"

def load_inventory():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_inventory():
    with open(DATA_FILE, 'w') as f:
        json.dump(inventory, f)

inventory = load_inventory()

# ------------------- MAIN WINDOW -------------------
root = tk.Tk()
root.title("Inventory Management System")

root.geometry("1200x700")
root.configure(bg="#f0f4f7")
root.resizable(False, False)

# ------------------- COLORS -------------------
BG = "#f0f4f7"
GREEN = "#2ecc71"
DARK = "#2c3e50"
BLUE = "#3498db"
RED = "#e74c3c"
WHITE = "#ffffff"

# ------------------- COMMON -------------------
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def header(title, back=None):
    top = tk.Frame(root, bg=DARK, height=70)
    top.pack(fill="x")

    if back:
        tk.Button(
            top,
            text="← BACK",
            command=back,
            bg=GREEN,
            fg="white",
            font=("Arial", 11, "bold"),
            width=10
        ).place(x=20, y=18)

    tk.Label(
        top,
        text=title.upper(),
        bg=DARK,
        fg="white",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

def exit_btn():
    tk.Button(
        root,
        text="EXIT",
        command=root.quit,
        bg=RED,
        fg="white",
        font=("Arial", 12, "bold"),
        width=20,
        height=2
    ).pack(side="bottom", pady=20)

# ------------------- INTRO SCREEN -------------------
def intro_screen():
    clear_screen()

    frame = tk.Frame(root, bg=BG)
    frame.pack(expand=True)

    tk.Label(
        frame,
        text="INVENTORY MANAGEMENT SYSTEM",
        bg=BG,
        fg=DARK,
        font=("Arial", 32, "bold")
    ).pack(pady=30)

    # ROBOT LABEL
    robot = tk.Label(
        frame,
        bg=BG,
        fg=DARK,
        font=("Arial", 40)
    )
    robot.pack(pady=20)

    # START BUTTON
    tk.Button(
        frame,
        text="START",
        command=dashboard,
        bg=GREEN,
        fg="white",
        font=("Arial", 16, "bold"),
        width=20,
        height=2
    ).pack(pady=30)

    # ROBOT ANIMATION FRAMES
    robot_frames = [
        """
           ("_")
          /|✓
          / \\
        """,

        """
           (*_*)
          <|\\
          / \\
        """
    ]

    current = 0

    # ANIMATION FUNCTION
    def animate_robot():
        nonlocal current

        robot.config(text=robot_frames[current])

        current += 1

        if current >= len(robot_frames):
            current = 0

        root.after(500, animate_robot)

    animate_robot()

# ------------------- DASHBOARD -------------------
def dashboard():
    clear_screen()
    header("Inventory Dashboard")

    center = tk.Frame(root, bg=BG)
    center.pack(expand=True)

    buttons = [
        ("ADD PRODUCT", add_product),
        ("VIEW INVENTORY", view_inventory),
        ("UPDATE STOCK", update_stock),
        ("DELETE PRODUCT", delete_product),
        ("ALERTS", alerts),
        ("REPORTS", reports)
    ]

    row = 0
    col = 0

    for text, command in buttons:
        btn = tk.Button(
            center,
            text=text,
            command=command,
            bg=BLUE,
            fg="white",
            font=("Arial", 14, "bold"),
            width=25,
            height=3
        )

        btn.grid(row=row, column=col, padx=20, pady=20)

        col += 1
        if col > 1:
            col = 0
            row += 1

    exit_btn()

# ------------------- ADD PRODUCT -------------------
def add_product():
    clear_screen()
    header("Add Product", dashboard)

    form = tk.Frame(root, bg=WHITE, padx=40, pady=40)
    form.pack(pady=50)

    tk.Label(
        form,
        text="Product Name",
        bg=WHITE,
        font=("Arial", 13)
    ).pack(anchor="w")

    name = tk.Entry(form, width=40, font=("Arial", 12))
    name.pack(pady=10)

    tk.Label(
        form,
        text="Price",
        bg=WHITE,
        font=("Arial", 13)
    ).pack(anchor="w")

    price = tk.Entry(form, width=40, font=("Arial", 12))
    price.pack(pady=10)

    tk.Label(
        form,
        text="Quantity",
        bg=WHITE,
        font=("Arial", 13)
    ).pack(anchor="w")

    qty = tk.Entry(form, width=40, font=("Arial", 12))
    qty.pack(pady=10)

    def save():
        try:
            inventory.append({
                "name": name.get(),
                "price": float(price.get()),
                "qty": int(qty.get())
            })

            save_inventory()

            messagebox.showinfo("Success", "Product Added")
            dashboard()

        except:
            messagebox.showerror("Error", "Invalid Input")

    tk.Button(
        root,
        text="ADD PRODUCT",
        command=save,
        bg=GREEN,
        fg="white",
        font=("Arial", 13, "bold"),
        width=20,
        height=2
    ).pack()

    exit_btn()

# ------------------- VIEW INVENTORY -------------------
def view_inventory():
    clear_screen()
    header("View Inventory", dashboard)

    table_frame = tk.Frame(root, bg=WHITE)
    table_frame.pack(pady=40)

    headers = ["PRODUCT NAME", "PRICE", "QUANTITY"]

    for col, h in enumerate(headers):
        tk.Label(
            table_frame,
            text=h,
            bg=DARK,
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2
        ).grid(row=0, column=col)

    for row, item in enumerate(inventory, start=1):
        tk.Label(
            table_frame,
            text=item["name"],
            width=25,
            height=2
        ).grid(row=row, column=0)

        tk.Label(
            table_frame,
            text=item["price"],
            width=25,
            height=2
        ).grid(row=row, column=1)

        tk.Label(
            table_frame,
            text=item["qty"],
            width=25,
            height=2
        ).grid(row=row, column=2)

    if not inventory:
        tk.Label(
            root,
            text="NO INVENTORY DATA",
            bg=BG,
            fg=RED,
            font=("Arial", 16, "bold")
        ).pack(pady=30)

    exit_btn()

# ------------------- UPDATE STOCK -------------------
def update_stock():
    clear_screen()
    header("Update Stock", dashboard)

    if not inventory:
        tk.Label(
            root,
            text="NO PRODUCTS AVAILABLE",
            bg=BG,
            fg=RED,
            font=("Arial", 16)
        ).pack(pady=50)

        exit_btn()
        return

    tk.Label(
        root,
        text="SELECT PRODUCT",
        bg=BG,
        fg=DARK,
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    for item in inventory:
        tk.Button(
            root,
            text=item["name"],
            command=lambda i=item: update_stock_reports(i),
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=30,
            height=2
        ).pack(pady=8)

    exit_btn()

# ------------------- UPDATE STOCK FORM -------------------
def update_stock_reports(selected_item):
    clear_screen()
    header("Update Stock", update_stock)

    frame = tk.Frame(root, bg=WHITE, padx=40, pady=40)
    frame.pack(pady=60)

    tk.Label(
        frame,
        text="Select Product",
        bg=WHITE,
        font=("Arial", 13)
    ).pack(anchor="w")

    selected = tk.StringVar()
    selected.set(selected_item["name"])

    option = tk.OptionMenu(
        frame,
        selected,
        *[i["name"] for i in inventory]
    )

    option.config(bg=BLUE, fg="white", width=30)
    option.pack(pady=10)

    tk.Label(
        frame,
        text="New Quantity",
        bg=WHITE,
        font=("Arial", 13)
    ).pack(anchor="w")

    qty = tk.Entry(frame, width=35, font=("Arial", 12))
    qty.pack(pady=10)

    def update():
        try:
            for item in inventory:
                if item["name"] == selected.get():
                    item["qty"] = int(qty.get())

            save_inventory()

            messagebox.showinfo("Updated", "Stock Updated")
            dashboard()

        except:
            messagebox.showerror("Error", "Invalid Input")

    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=20)

    tk.Button(
        btn_frame,
        text="UPDATE",
        command=update,
        bg=GREEN,
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        height=2
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        btn_frame,
        text="CANCEL",
        command=update_stock,
        bg=RED,
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        height=2
    ).grid(row=0, column=1, padx=10)

    exit_btn()

# ------------------- ALERTS -------------------
def alerts():
    clear_screen()
    header("Alerts", dashboard)

    found = False

    for item in inventory:
        if item["qty"] <= 5:
            tk.Label(
                root,
                text=f"⚠ LOW STOCK: {item['name']} | Qty: {item['qty']}",
                bg=BG,
                fg=RED,
                font=("Arial", 14, "bold")
            ).pack(pady=10)

            found = True

    if not found:
        tk.Label(
            root,
            text="NO ALERTS",
            bg=BG,
            fg=GREEN,
            font=("Arial", 16, "bold")
        ).pack(pady=50)

    exit_btn()

# ------------------- REPORTS -------------------
def reports():
    clear_screen()
    header("Reports", dashboard)

    total = sum(i["price"] * i["qty"] for i in inventory)

    frame = tk.Frame(root, bg=WHITE, padx=50, pady=50)
    frame.pack(pady=100)

    tk.Label(
        frame,
        text="TOTAL INVENTORY VALUE",
        bg=WHITE,
        fg=DARK,
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        frame,
        text=f"${total:.2f}",
        bg=WHITE,
        fg=GREEN,
        font=("Arial", 35, "bold")
    ).pack()

    exit_btn()

# ------------------- DELETE PRODUCT -------------------
def delete_product():
    clear_screen()
    header("Delete Product", dashboard)

    if not inventory:
        tk.Label(
            root,
            text="NO PRODUCTS AVAILABLE",
            bg=BG,
            fg=RED,
            font=("Arial", 16)
        ).pack(pady=50)

        exit_btn()
        return

    tk.Label(
        root,
        text="SELECT PRODUCT TO DELETE",
        bg=BG,
        fg=DARK,
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    def remove_product(item):
        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete {item['name']}?"
        ):

            inventory.remove(item)
            save_inventory()

            messagebox.showinfo(
                "Deleted",
                "Product Deleted Successfully"
            )

            delete_product()

    for item in inventory:
        tk.Button(
            root,
            text=item["name"],
            command=lambda i=item: remove_product(i),
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=30,
            height=2
        ).pack(pady=8)

    exit_btn()

# ------------------- START PROGRAM -------------------
intro_screen()
root.mainloop()
