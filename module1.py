# ==========================================================
# INVENTORY MANAGEMENT SYSTEM
# ==========================================================

import sqlite3
import hashlib
#
from datetime import datetime

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

DATABASE_NAME = "inventory.db"

def connect():

    return sqlite3.connect(DATABASE_NAME)

# ==========================================================
# PRESS ENTER TO CONTINUE
# ==========================================================

def pause():

    input("\nPress Enter to Continue...")

# ==========================================================
# PASSWORD HASHING
# ==========================================================

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()

# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

def create_tables():

    conn = connect()

    cursor = conn.cursor()

    # ---------------- SETTINGS ----------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS settings(

            setting_name TEXT PRIMARY KEY,

            setting_value TEXT NOT NULL

        )

    """)

    # ---------------- CATEGORIES ----------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS categories(

            category_id INTEGER PRIMARY KEY AUTOINCREMENT,

            category_name TEXT UNIQUE NOT NULL

        )

    """)

    # ---------------- PRODUCTS ----------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS products(

            product_id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_name TEXT NOT NULL,

            brand TEXT NOT NULL,

            category_id INTEGER,

            buying_price REAL NOT NULL,

            selling_price REAL NOT NULL,

            best_price REAL NOT NULL,

            quantity INTEGER NOT NULL,

            minimum_stock INTEGER NOT NULL,

            FOREIGN KEY(category_id)

            REFERENCES categories(category_id)

        )

    """)

    # ---------------- SALES ----------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS sales(

            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id INTEGER,

            product_name TEXT NOT NULL,

            brand TEXT NOT NULL,

            cashier_name TEXT NOT NULL,
                   
            customer_name TEXT NOT NULL,       

            quantity INTEGER NOT NULL,

            buying_price REAL NOT NULL,

            selling_price REAL NOT NULL,

            total_amount REAL NOT NULL,

            sale_date TEXT NOT NULL,

            FOREIGN KEY(product_id)

            REFERENCES products(product_id)

        )

    """)

    conn.commit()

    conn.close()

# ==========================================================
# INITIALIZE DEFAULT PASSWORDS
# ==========================================================

def initialize_passwords():

    conn = connect()

    cursor = conn.cursor()

    passwords = {

        "admin_password": "admin123",

        "cashier_password": "cashier123"

    }

    for key, value in passwords.items():

        cursor.execute("""

            SELECT *

            FROM settings

            WHERE setting_name=?

        """, (key,))

        if cursor.fetchone() is None:

            cursor.execute("""

                INSERT INTO settings

                VALUES(?,?)

            """,

            (

                key,

                hash_password(value)

            ))

    conn.commit()

    conn.close()

# ==========================================================
# VERIFY PASSWORD
# ==========================================================

def verify_password(setting_name, entered_password):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT setting_value

        FROM settings

        WHERE setting_name=?

    """,(setting_name,))

    result = cursor.fetchone()

    conn.close()

    if result is None:

        return False

    return result[0] == hash_password(entered_password)



#PHASE 2 – LOGIN, MENUS & PASSWORD MANAGEMENT
# ==========================================================
# LOGIN
# ==========================================================

def login():

    while True:

        print("\n")
        print("=" * 50)
        print("      INVENTORY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Administrator")
        print("2. Cashier")
        print("3. Exit")
        print("=" * 50)

        choice = input("Select Role: ")

        # ---------------- ADMINISTRATOR ----------------

        if choice == "1":

            attempts = 3

            while attempts > 0:

                password = input("Administrator Password: ")

                if verify_password("admin_password", password):

                    print("\nLogin Successful.")

                    return {"role": "admin"}

                attempts -= 1

                if attempts > 0:

                    print(f"\nIncorrect Password. {attempts} attempt(s) remaining.")

                else:

                    print("\nToo many failed attempts.")
                    print("Returning to Role Selection...")

        # ---------------- CASHIER ----------------

        elif choice == "2":

            attempts = 3

            while attempts > 0:

                password = input("Cashier Password: ")

                if verify_password("cashier_password", password):

                    print("\nLogin Successful.")

                    return {"role": "cashier"}

                attempts -= 1

                if attempts > 0:

                    print(f"\nIncorrect Password. {attempts} attempt(s) remaining.")

                else:

                    print("\nToo many failed attempts.")
                    print("Returning to Role Selection...")

        # ---------------- EXIT ----------------

        elif choice == "3":

            return None

        else:

            print("Invalid Choice.")

            pause()

# ==========================================================
# ADMINISTRATOR MENU
# ==========================================================

def admin_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("          ADMINISTRATOR MENU")
        print("=" * 50)

        print("1. Category Management")
        print("2. Product Management")
        print("3. Sales Management")
        print("4. Reports")
        print("5. Password Management")
        print("6. Logout")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            category_menu()

        elif choice == "2":

            admin_product_menu()

        elif choice == "3":

            sales_menu()

        elif choice == "4":

            reports_menu()

        elif choice == "5":

            password_management_menu()

        elif choice == "6":

            print("\nLogging Out...")

            break

        else:

            print("Invalid Choice.")

            pause()

# ==========================================================
# CASHIER MENU
# ==========================================================

def cashier_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("             CASHIER MENU")
        print("=" * 50)

        print("1. Product Management")
        print("2. Sales Management")
        print("3. Reports")
        print("4. Logout")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            cashier_product_menu()

        elif choice == "2":

            sales_menu()

        elif choice == "3":

            reports_menu()

        elif choice == "4":

            print("\nLogging Out...")

            break

        else:

            print("Invalid Choice.")

            pause()

# ==========================================================
# PASSWORD MANAGEMENT MENU
# ==========================================================

def password_management_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("        PASSWORD MANAGEMENT")
        print("=" * 50)

        print("1. Change Administrator Password")
        print("2. Change Cashier Password")
        print("3. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            change_admin_password()

        elif choice == "2":

            change_cashier_password()

        elif choice == "3":

            break

        else:

            print("Invalid Choice.")

            pause()

# ==========================================================
# CHANGE ADMINISTRATOR PASSWORD
# ==========================================================

def change_admin_password():

    current = input("Current Administrator Password: ")

    if not verify_password("admin_password", current):

        print("Incorrect Password.")

        pause()

        return

    new_password = input("New Administrator Password: ")

    confirm = input("Confirm Password: ")

    if new_password != confirm:

        print("Passwords do not match.")

        pause()

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE settings

        SET setting_value=?

        WHERE setting_name='admin_password'

    """,

    (

        hash_password(new_password),

    ))

    conn.commit()

    conn.close()

    print("Administrator Password Updated Successfully.")

    pause()

# ==========================================================
# CHANGE CASHIER PASSWORD
# ==========================================================

def change_cashier_password():

    current = input("Current Cashier Password: ")

    if not verify_password("cashier_password", current):

        print("Incorrect Password.")

        pause()

        return

    new_password = input("New Cashier Password: ")

    confirm = input("Confirm Password: ")

    if new_password != confirm:

        print("Passwords do not match.")

        pause()

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE settings

        SET setting_value=?

        WHERE setting_name='cashier_password'

    """,

    (

        hash_password(new_password),

    ))

    conn.commit()

    conn.close()

    print("Cashier Password Updated Successfully.")

    pause()

# ==========================================================
# CATEGORY MANAGEMENT MENU
# ==========================================================

def category_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("         CATEGORY MANAGEMENT")
        print("=" * 50)

        print("1. Add Category")
        print("2. View Categories")
        print("3. Search Category")
        print("4. Update Category")
        print("5. Delete Category")
        print("6. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            add_category()

        elif choice == "2":

            view_categories()

        elif choice == "3":

            search_category()

        elif choice == "4":

            update_category()

        elif choice == "5":

            delete_category()

        elif choice == "6":

            break

        else:

            print("Invalid Choice.")

            pause()

# ==========================================================
# ADD CATEGORY
# ==========================================================

def add_category():

    category = input("\nEnter Category Name: ").strip().title()

    if category == "":

        print("Category name cannot be empty.")

        pause()

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM categories

        WHERE category_name=?

    """,(category,))

    if cursor.fetchone():

        print("Category already exists.")

        conn.close()

        pause()

        return

    cursor.execute("""

        INSERT INTO categories(category_name)

        VALUES(?)

    """,(category,))

    conn.commit()

    conn.close()

    print("Category added successfully.")

    pause()

# ==========================================================
# VIEW CATEGORIES
# ==========================================================

def view_categories():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        category_id,

        category_name

        FROM categories

        ORDER BY category_name

    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("\nNo categories found.")

        pause()

        return

    print("\n")
    print("=" * 40)
    print(f"{'ID':<10}{'CATEGORY'}")
    print("=" * 40)

    for row in rows:

        print(f"{row[0]:<10}{row[1]}")

    print("=" * 40)

    pause()

# ==========================================================
# SEARCH CATEGORY
# ==========================================================

def search_category():

    keyword = input("\nEnter Category Name: ").strip()

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        category_id,

        category_name

        FROM categories

        WHERE category_name LIKE ?

        ORDER BY category_name

    """,("%"+keyword+"%",))

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("No matching categories found.")

        pause()

        return

    print("\n")
    print("=" * 40)
    print(f"{'ID':<10}{'CATEGORY'}")
    print("=" * 40)

    for row in rows:

        print(f"{row[0]:<10}{row[1]}")

    print("=" * 40)

    pause()

# ==========================================================
# UPDATE CATEGORY
# ==========================================================

def update_category():

    view_categories()

    category_id = input("\nEnter Category ID to Update: ")

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM categories

        WHERE category_id=?

    """,(category_id,))

    if not cursor.fetchone():

        print("Category not found.")

        conn.close()

        pause()

        return

    new_name = input("Enter New Category Name: ").strip().title()

    cursor.execute("""

        UPDATE categories

        SET category_name=?

        WHERE category_id=?

    """,(new_name,category_id))

    conn.commit()

    conn.close()

    print("Category updated successfully.")

    pause()

#DELETE CATEGORY    

def delete_category():

    view_categories()

    category_id = input("\nEnter Category ID to Delete: ")

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM categories

        WHERE category_id=?

    """,(category_id,))

    if not cursor.fetchone():

        print("Category not found.")

        conn.close()

        pause()

        return

    confirm = input("Are you sure? (Y/N): ").upper()

    if confirm == "Y":

        cursor.execute("""

            DELETE FROM categories

            WHERE category_id=?

        """,(category_id,))

        conn.commit()

        print("Category deleted successfully.")

    else:

        print("Deletion cancelled.")

    conn.close()

    pause()

# ==========================================
# PRODUCTS
# ==========================================
def add_product():

    conn = connect()
    cursor = conn.cursor()

    print("\n------ ADD PRODUCT ------")

    product_name = input("Product Name : ")

    brand = input("Brand : ")
    view_categories()

    category_id = int(input("\nCategory ID : "))

    buying_price = float(input("Buying Price : "))

    selling_price = float(input("Selling Price : "))

    best_price = float(
        input("best_price : ")
    )

    quantity = int(input("Quantity : "))

    minimum_stock = int(input("Minimum Stock Level : "))

    cursor.execute("""

    INSERT INTO products(

    product_name,

    brand,

    category_id,

    buying_price,

    selling_price,

    best_price,

    quantity,

    minimum_stock

    )

    VALUES(?,?,?,?,?,?,?,?)

    """, (

        product_name,

        brand,

        category_id,

        buying_price,

        selling_price,

        best_price,

        quantity,

        minimum_stock

    ))

    conn.commit()

    conn.close()

    print("\nProduct Added Successfully.")


# ==========================================

def view_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    product_id,

    product_name,

    brand,

    category_name,

    buying_price,

    selling_price,

    best_price,

    quantity,

    minimum_stock

    FROM products

    JOIN categories

    ON products.category_id = categories.category_id

    """)

    products = cursor.fetchall()

    conn.close()

    print("\n========== PRODUCTS ==========\n")

    if not products:

        print("No Products Available.")

    else:

        for p in products:

            print(f"""
ID : {p[0]}
Product : {p[1]}
Brand : {p[2]}
Category : {p[3]}
Buying Price : {p[4]}
Selling Price : {p[5]}
Best Price : {p[6]}
Quantity : {p[7]}
Minimum Stock : {p[8]}
--------------------------------------------
""")


# ==========================================

def search_product():

    conn = connect()
    cursor = conn.cursor()

    search = input("\nEnter Product Name : ")

    cursor.execute("""

    SELECT

    product_name,

    brand,

    selling_price,

    quantity

    FROM products

    WHERE product_name LIKE ?

    """, ('%' + search + '%',))

    products = cursor.fetchall()

    conn.close()

    if not products:

        print("\nProduct Not Found.")

    else:

        print("\n------ SEARCH RESULTS ------")

        for product in products:

            print(f"""
Product : {product[0]}

Brand : {product[1]}

Best Price : {product[2]}

Quantity Available : {product[3]}

--------------------------
""")


# ==========================================

def refill_stock():

    conn = connect()
    cursor = conn.cursor()

    view_products()

    product_id = int(input("\nProduct ID : "))

    quantity = int(input("Quantity to Add : "))

    cursor.execute("""

    UPDATE products

    SET quantity = quantity + ?

    WHERE product_id = ?

    """, (

        quantity,

        product_id

    ))

    conn.commit()

    conn.close()

    print("\nStock Updated Successfully.")


# ==========================================

def low_stock_alert():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    product_name,

    quantity,

    minimum_stock

    FROM products

    """)

    products = cursor.fetchall()

    conn.close()

    print("\n====== LOW STOCK ALERTS ======\n")

    low = False

    for product in products:

        if product[1] <= product[2]:

            low = True

            print(f"""
WARNING!

{product[0]}

Remaining Stock : {product[1]}

Minimum Stock : {product[2]}
""")

    if not low:

        print("All Products Have Sufficient Stock.")


# ==========================================
# PRODUCT MENU
# ==========================================

def product_menu():

    while True:

        print("""
========== PRODUCT MENU ==========

1. Add Product

2. View Products

3. Search Product

4. Refill Stock

5. Low Stock Alerts

6. Back

==================================
""")

        choice = input("Choose Option : ")

        if choice == "1":

            add_product()

        elif choice == "2":

            view_products()

        elif choice == "3":

            search_product()

        elif choice == "4":

            refill_stock()

        elif choice == "5":

            low_stock_alert()

        elif choice == "6":

            break

        else:

            print("\nInvalid Choice.")
            # ==========================================
# ADMIN MENU
# ==========================================

def admin_menu():

    while True:

        print("""

========================================
      STOCK MANAGEMENT SYSTEM
========================================

1. Categories

2. Products

3. Sales (Coming Soon)

4. Reports (Coming Soon)

5. Logout

========================================

""")

        choice = input("Choose Option : ")

        if choice == "1":

            category_menu()

        elif choice == "2":

            product_menu()

        elif choice == "3":

            print("\nSales Module Coming Soon.")

        elif choice == "4":

            print("\nReports Module Coming Soon.")

        elif choice == "5":

            print("\nLogging Out...\n")

            break

        else:

            print("\nInvalid Choice.")


# ==========================================
# CASHIER MENU
# ==========================================

def cashier_menu():

    while True:

        print("""

========================================
          CASHIER MENU
========================================

1. Search Product

2. Sales (Coming Soon)

3. Logout

========================================

""")

        choice = input("Choose Option : ")

        if choice == "1":

            search_product()

        elif choice == "2":

            print("\nSales Module Coming Soon.")

        elif choice == "3":

            print("\nLogging Out...\n")

            break

        else:

            print("\nInvalid Choice.")

# ==========================================================
# VIEW PRODUCTS
# ==========================================================

def view_products():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        p.product_id,
        p.product_name,
        p.brand,
        c.category_name,
        p.buying_price,
        p.selling_price,
        p.best_price,
        p.quantity,
        p.minimum_stock

        FROM products p

        LEFT JOIN categories c

        ON p.category_id = c.category_id

        ORDER BY p.product_name, p.brand

    """)

    products = cursor.fetchall()

    conn.close()

    if not products:

        print("\nNo products available.")

        pause()

        return

    print("\n")

    print("=" * 140)

    print(f"{'ID':<5}{'PRODUCT':<20}{'BRAND':<20}{'CATEGORY':<18}"
          f"{'BUY':<10}{'SELL':<10}{'BEST':<10}{'QTY':<8}{'MIN'}")

    print("=" * 140)

    for product in products:

        print(f"{product[0]:<5}"
              f"{product[1]:<20}"
              f"{product[2]:<20}"
              f"{product[3]:<18}"
              f"{product[4]:<10.2f}"
              f"{product[5]:<10.2f}"
              f"{product[6]:<10.2f}"
              f"{product[7]:<8}"
              f"{product[8]}")

    print("=" * 140)

    pause()

# ==========================================================
# SEARCH PRODUCT
# ==========================================================

def search_product():

    keyword = input("\nEnter Product Name: ").strip()

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        p.product_id,
        p.product_name,
        p.brand,
        c.category_name,
        p.selling_price,
        p.best_price,
        p.quantity

        FROM products p

        LEFT JOIN categories c

        ON p.category_id = c.category_id

        WHERE p.product_name LIKE ?

        ORDER BY p.brand

    """, ("%" + keyword + "%",))

    products = cursor.fetchall()

    conn.close()

    if not products:

        print("\nNo matching products found.")

        pause()

        return

    print("\n")

    print("=" * 120)

    print(f"{'ID':<5}{'PRODUCT':<20}{'BRAND':<20}"
          f"{'CATEGORY':<20}{'SELL':<12}{'BEST':<12}{'STOCK'}")

    print("=" * 120)

    for product in products:

        print(f"{product[0]:<5}"
              f"{product[1]:<20}"
              f"{product[2]:<20}"
              f"{product[3]:<20}"
              f"{product[4]:<12.2f}"
              f"{product[5]:<12.2f}"
              f"{product[6]}")

    print("=" * 120)

    print("\nBest Price is the minimum selling price allowed.")

    pause()


# ==========================================================
# SELECT PRODUCT
# ==========================================================

def select_product():

    while True:

        keyword = input("\nEnter Product Name (0 to Cancel): ").strip()

        if keyword == "0":

            return None

        conn = connect()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

            product_id,
            product_name,
            brand,
            selling_price,
            best_price,
            quantity

            FROM products

            WHERE product_name LIKE ?

            ORDER BY brand

        """, ("%" + keyword + "%",))

        products = cursor.fetchall()

        conn.close()

        if not products:

            print("\nNo matching products found.")

            continue

        print("\n")

        print("=" * 95)

        print(f"{'NO':<5}{'PRODUCT':<20}{'BRAND':<20}"
              f"{'SELL':<12}{'BEST':<12}{'STOCK'}")

        print("=" * 95)

        for index, product in enumerate(products, start=1):

            print(f"{index:<5}"
                  f"{product[1]:<20}"
                  f"{product[2]:<20}"
                  f"{product[3]:<12.2f}"
                  f"{product[4]:<12.2f}"
                  f"{product[5]}")

        print("=" * 95)

        choice = input("\nSelect Product Number (0 to Search Again): ")

        if not choice.isdigit():

            print("Invalid selection.")

            continue

        choice = int(choice)

        if choice == 0:

            continue

        if 1 <= choice <= len(products):

            return products[choice - 1][0]

        print("Invalid selection.")

# ==========================================================
# UPDATE PRODUCT
# ==========================================================

def update_product():

    product_id = select_product()

    if product_id is None:

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            product_name,
            brand,
            category_id,
            buying_price,
            selling_price,
            best_price,
            quantity,
            minimum_stock

        FROM products

        WHERE product_id=?

    """, (product_id,))

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")

        conn.close()

        pause()

        return

    print("\nLeave blank to keep the current value.\n")

    # ---------------- CATEGORY ----------------

    cursor.execute("""

        SELECT category_id, category_name

        FROM categories

        ORDER BY category_name

    """)

    categories = cursor.fetchall()

    print("\nAVAILABLE CATEGORIES")

    print("=" * 40)

    for category in categories:

        print(f"{category[0]:<5}{category[1]}")

    print("=" * 40)

    category = input(f"Category ID [{product[2]}]: ").strip()

    if category == "":

        category_id = product[2]

    else:

        category_id = int(category)

    # ---------------- PRODUCT NAME ----------------

    product_name = input(f"Product Name [{product[0]}]: ").strip().title()

    if product_name == "":

        product_name = product[0]

    # ---------------- BRAND ----------------

    brand = input(f"Brand [{product[1]}]: ").strip().title()

    if brand == "":

        brand = product[1]

    # ---------------- BUYING PRICE ----------------

    buying = input(f"Buying Price [{product[3]}]: ").strip()

    buying_price = product[3] if buying == "" else float(buying)

    # ---------------- SELLING PRICE ----------------

    selling = input(f"Selling Price [{product[4]}]: ").strip()

    selling_price = product[4] if selling == "" else float(selling)

    if selling_price < buying_price:

        print("Selling price cannot be below buying price.")

        conn.close()

        pause()

        return

    # ---------------- BEST PRICE ----------------

    best = input(f"Best Price [{product[5]}]: ").strip()

    best_price = product[5] if best == "" else float(best)

    if best_price < buying_price:

        print("Best price cannot be below buying price.")

        conn.close()

        pause()

        return

    if best_price > selling_price:

        print("Best price cannot exceed selling price.")

        conn.close()

        pause()

        return

    # ---------------- QUANTITY ----------------

    quantity = input(f"Quantity [{product[6]}]: ").strip()

    quantity = product[6] if quantity == "" else int(quantity)

    # ---------------- MINIMUM STOCK ----------------

    minimum_stock = input(f"Minimum Stock [{product[7]}]: ").strip()

    minimum_stock = product[7] if minimum_stock == "" else int(minimum_stock)

    cursor.execute("""

        UPDATE products

        SET

        product_name=?,
        brand=?,
        category_id=?,
        buying_price=?,
        selling_price=?,
        best_price=?,
        quantity=?,
        minimum_stock=?

        WHERE product_id=?

    """,

    (

        product_name,
        brand,
        category_id,
        buying_price,
        selling_price,
        best_price,
        quantity,
        minimum_stock,
        product_id

    ))

    conn.commit()

    conn.close()

    print("\nProduct updated successfully.")

    pause()


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_product():

    product_id = select_product()

    if product_id is None:

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand

        FROM products

        WHERE product_id=?

    """, (product_id,))

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")

        conn.close()

        pause()

        return

    print("\nSelected Product")

    print(f"Product : {product[0]}")

    print(f"Brand   : {product[1]}")

    confirm = input("\nDelete this product? (Y/N): ").upper()

    if confirm == "Y":

        cursor.execute("""

            DELETE

            FROM products

            WHERE product_id=?

        """, (product_id,))

        conn.commit()

        print("\nProduct deleted successfully.")

    else:

        print("\nDeletion cancelled.")

    conn.close()

    pause()

# ==========================================================
# REFILL STOCK
# ==========================================================

def refill_stock():

    product_id = select_product()

    if product_id is None:

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand,
        quantity

        FROM products

        WHERE product_id=?

    """,(product_id,))

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")

        conn.close()

        pause()

        return

    print("\nCurrent Stock Information")
    print("=" * 40)
    print(f"Product : {product[0]}")
    print(f"Brand   : {product[1]}")
    print(f"Current Stock : {product[2]}")
    print("=" * 40)

    while True:

        try:

            added_quantity = int(input("Quantity to Add: "))

            if added_quantity <= 0:

                print("Quantity must be greater than zero.")

                continue

            break

        except ValueError:

            print("Enter a valid whole number.")

    new_quantity = product[2] + added_quantity

    cursor.execute("""

        UPDATE products

        SET quantity=?

        WHERE product_id=?

    """,(new_quantity, product_id))

    conn.commit()

    conn.close()

    print("\nStock updated successfully.")

    print(f"New Stock Level : {new_quantity}")

    pause()


# ==========================================================
# LOW STOCK PRODUCTS
# ==========================================================

def low_stock_products():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand,
        quantity,
        minimum_stock

        FROM products

        WHERE quantity <= minimum_stock

        ORDER BY quantity ASC

    """)

    products = cursor.fetchall()

    conn.close()

    if not products:

        print("\nAll products have sufficient stock.")

        pause()

        return

    print("\n")
    print("=" * 75)
    print("             LOW STOCK PRODUCTS")
    print("=" * 75)

    print(f"{'PRODUCT':<20}"
          f"{'BRAND':<20}"
          f"{'CURRENT':<15}"
          f"{'MINIMUM'}")

    print("=" * 75)

    for product in products:

        print(f"{product[0]:<20}"
              f"{product[1]:<20}"
              f"{product[2]:<15}"
              f"{product[3]}")

    print("=" * 75)

    print("\nThese products should be reordered soon.")

    pause()
# SALES MENU
# ==========================================================

def sales_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("             SALES MENU")
        print("=" * 50)

        print("1. Sell Product")
        print("2. View Sales")
        print("3. Search Sales")
        print("4. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            sell_product()

        elif choice == "2":

            view_sales()

        elif choice == "3":

            search_sales()

        elif choice == "4":

            break

        else:

            print("Invalid Choice.")




# ==========================================================
# SELL PRODUCT
# ==========================================================

from datetime import datetime

def sell_product():

    product_id = select_product()

    if product_id is None:

        pause()

        return

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_id,
        product_name,
        brand,
        buying_price,
        selling_price,
        best_price,
        quantity

        FROM products

        WHERE product_id=?

    """, (product_id,))

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")

        conn.close()

        pause()

        return


    cashier = input("Cashier Name: ").strip().title()
    customer = input("Customer Name: ").strip().title()
    print(f"\nSelling Price : Ksh {product[4]:.2f}")
    print(f"Best Price    : Ksh {product[5]:.2f}")

    try:

        agreed_price = float(input("Selling Price Agreed: "))

    except ValueError:

        print("Invalid Price.")

        conn.close()

        pause()

        return

    if agreed_price < product[5]:

        print("Price cannot be below the Best Price.")

        conn.close()

        pause()

        return

    try:

        quantity = int(input("Quantity: "))

    except ValueError:

        print("Invalid Quantity.")

        conn.close()

        pause()

        return

    if quantity <= 0:

        print("Quantity must be greater than zero.")

        conn.close()

        pause()

        return

    if quantity > product[6]:

        print("Insufficient Stock.")

        conn.close()

        pause()

        return

    total = agreed_price * quantity



    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

        INSERT INTO sales(
            product_id,
            product_name,
            brand,
            cashier_name,
            customer_name,
            quantity,
            buying_price,
            selling_price,
            total_amount,
            sale_date

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

    """, (

        product[0],
        product[1],
        product[2],
        cashier,
        customer,
        quantity,
        product[3],
        agreed_price,
        total,
        sale_date

    ))

    cursor.execute("""

        UPDATE products

        SET quantity = quantity - ?

        WHERE product_id=?

    """, (quantity, product[0]))

    conn.commit()

    conn.close()

    print("\nSale Recorded Successfully.")

    print_receipt(

        
        product[1],
        product[2],
        cashier,
        customer,
        quantity,
        agreed_price,
        total

    )

    pause()

# ==========================================================
# VIEW SALES
# ==========================================================

def view_sales():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand,
        customer_name,
        cashier_name,
        quantity,
        selling_price,
        total_amount,
        sale_date

        FROM sales

        ORDER BY sale_date DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("\nNo sales found.")

        pause()

        return

    print("\n")

    print("=" * 150)

    print(f"{'PRODUCT':<18}{'BRAND':<15}{'CUSTOMER':<18}{'CASHIER':<15}{'QTY':<6}{'PRICE':<12}{'TOTAL':<12}{'DATE'}")

    print("=" * 150)

    for row in rows:

        print(f"{row[0]:<18}"
              f"{row[1]:<15}"
              f"{row[2]:<18}"
              f"{row[3]:<15}"
              f"{row[4]:<6}"
              f"Ksh {row[5]:<8.2f}"
              f"Ksh {row[6]:<8.2f}"
              f"{row[7]}")

    print("=" * 150)

    pause()

# ==========================================================
# SEARCH SALES
# ==========================================================
def search_sales():

    keyword = input("Customer Name: ").strip()

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand,
        quantity,
        total_amount,
        sale_date

        FROM sales

        WHERE LOWER(customer_name) LIKE LOWER(?)

        ORDER BY sale_date DESC

    """, ('%' + keyword + '%',))

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("\nNo Sales Found.")

        pause()

        return

    print("\n")

    print("=" * 110)

    print(f"{'PRODUCT':<20}{'BRAND':<18}{'QTY':<8}{'TOTAL':<15}{'DATE'}")

    print("=" * 110)

    for row in rows:

        print(f"{row[0]:<20}"
              f"{row[1]:<18}"
              f"{row[2]:<8}"
              f"Ksh {row[3]:<10.2f}"
              f"{row[4]}")

    print("=" * 110)

    pause()

    

# ==========================================================
# PRINT RECEIPT
# ==========================================================

from datetime import datetime

def print_receipt(product, brand, customer,
                  cashier, quantity, price, total):

    print("\n")
    print("="*50)
    print("           SALES RECEIPT")
    print("="*50)

    print(f"Date        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Cashier     : {cashier}")
    print(f"Customer    : {customer}")

    print("-"*50)

    print(f"Product     : {product}")
    print(f"Brand       : {brand}")
    print(f"Quantity    : {quantity}")
    print(f"Unit Price  : Ksh {price:.2f}")

    print("-"*50)

    print(f"TOTAL       : Ksh {total:.2f}")

    print("="*50)
    print("      THANK YOU FOR SHOPPING!")
    print("="*50)

# ==========================================================
# REPORTS MENU
# ==========================================================

def reports_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("              REPORTS")
        print("=" * 50)

        print("1. Current Stock Value")
        print("2. Weekly Sales Report")
        print("3. Highest Profit Products (This Week)")
        print("4. Lowest Profit Products (This Week)")
        print("5. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            current_stock_value()

        elif choice == "2":

            weekly_sales_report()

        elif choice == "3":

            highest_profit_products()

        elif choice == "4":

            lowest_profit_products()

        elif choice == "5":

            break

        else:

            print("Invalid Choice.")

# ==========================================================
# CURRENT STOCK VALUE
# ==========================================================

def current_stock_value():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,
        brand,
        buying_price,
        quantity,
        buying_price * quantity

        FROM products

        ORDER BY product_name

    """)

    rows = cursor.fetchall()

    cursor.execute("""

        SELECT

        SUM(buying_price * quantity)

        FROM products

    """)

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:

        total = 0

    print("\n")
    print("=" * 90)

    print(f"{'PRODUCT':<20}{'BRAND':<20}{'BUY PRICE':<15}{'STOCK':<10}{'VALUE'}")

    print("=" * 90)

    for row in rows:

        print(f"{row[0]:<20}{row[1]:<20}{row[2]:<15.2f}{row[3]:<10}{row[4]:.2f}")

    print("=" * 90)

    print(f"TOTAL STOCK VALUE : Ksh {total:.2f}")

    print("=" * 90)

    pause()

# ==========================================================
# WEEKLY SALES REPORT
# ==========================================================

def weekly_sales_report():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        sale_date,
        cashier_name,
        total_amount

        FROM sales

        WHERE

        date(sale_date) >= date('now','-7 days')

        ORDER BY sale_date DESC

    """)

    rows = cursor.fetchall()

    cursor.execute("""

        SELECT

        SUM(total_amount)

        FROM sales

        WHERE

        date(sale_date)>=date('now','-7 days')

    """)

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:

        total = 0

    print("\n")

    print("="*100)

    print(f"{'DATE':<22}{'CODE':<12}{'CUSTOMER':<20}{'CASHIER':<20}{'TOTAL'}")

    print("="*100)

    for row in rows:

        print(f"{row[0]:<22}{row[1]:<12}{row[2]:<20}{row[3]:<20}Ksh {row[4]:.2f}")

    print("="*100)

    print(f"TOTAL SALES THIS WEEK : Ksh {total:.2f}")

    print("="*100)

    pause()


# ==========================================================
# HIGHEST PROFIT PRODUCTS
# ==========================================================

def highest_profit_products():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,

        brand,

        SUM(

        (selling_price-buying_price)

        * quantity

        ) AS profit

        FROM sales

        WHERE

        date(sale_date)>=date('now','-7 days')

        GROUP BY

        product_name,

        brand

        ORDER BY

        profit DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("\nNo sales recorded this week.")

        pause()

        return

    print("\n")

    print("="*70)

    print(f"{'PRODUCT':<20}{'BRAND':<20}{'PROFIT'}")

    print("="*70)

    for row in rows:

        print(f"{row[0]:<20}{row[1]:<20}Ksh {row[2]:.2f}")

    print("="*70)

    pause()

# ==========================================================
# LOWEST PROFIT PRODUCTS
# ==========================================================

def lowest_profit_products():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        product_name,

        brand,

        SUM(

        (selling_price-buying_price)

        * quantity

        ) AS profit

        FROM sales

        WHERE

        date(sale_date)>=date('now','-7 days')

        GROUP BY

        product_name,

        brand

        ORDER BY

        profit ASC

    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        print("\nNo sales recorded this week.")

        pause()

        return

    print("\n")

    print("="*70)

    print(f"{'PRODUCT':<20}{'BRAND':<20}{'PROFIT'}")

    print("="*70)

    for row in rows:

        print(f"{row[0]:<20}{row[1]:<20}Ksh {row[2]:.2f}")

    print("="*70)

    pause()

# ==========================================================
# ADMINISTRATOR MENU
# ==========================================================

def admin_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("          ADMINISTRATOR MENU")
        print("=" * 50)

        print("1. Category Management")
        print("2. Product Management")
        print("3. Sales Management")
        print("4. Reports")
        print("5. Password Management")
        print("6. Logout")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            category_menu()

        elif choice == "2":

            admin_product_menu()

        elif choice == "3":

            sales_menu()

        elif choice == "4":

            reports_menu()

        elif choice == "5":

            password_management_menu()

        elif choice == "6":

            print("\nLogging Out...")

            break

        else:

            print("Invalid Choice.")

            pause()


# ==========================================================
# CASHIER MENU
# ==========================================================

def cashier_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("             CASHIER MENU")
        print("=" * 50)

        print("1. Product Management")
        print("2. Sales Management")
        print("3. Reports")
        print("4. Logout")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            cashier_product_menu()

        elif choice == "2":

            sales_menu()

        elif choice == "3":

            reports_menu()

        elif choice == "4":

            print("\nLogging Out...")

            break

        else:

            print("Invalid Choice.")

            pause()

 # ==========================================================
# ADMINISTRATOR PRODUCT MENU
# ==========================================================

def admin_product_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("         PRODUCT MANAGEMENT")
        print("=" * 50)

        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Refill Stock")
        print("7. Low Stock Products")
        print("8. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            add_product()

        elif choice == "2":

            view_products()

        elif choice == "3":

            search_product()

        elif choice == "4":

            update_product()

        elif choice == "5":

            delete_product()

        elif choice == "6":

            refill_stock()

        elif choice == "7":

            low_stock_products()

        elif choice == "8":

            break

        else:

            print("Invalid Choice.")

            pause()          

# ==========================================================
# CASHIER PRODUCT MENU
# ==========================================================

def cashier_product_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("         PRODUCT MANAGEMENT")
        print("=" * 50)

        print("1. View Products")
        print("2. Search Product")
        print("3. Low Stock Products")
        print("4. Back")

        print("=" * 50)

        choice = input("Choose Option: ")

        if choice == "1":

            view_products()

        elif choice == "2":

            search_product()

        elif choice == "3":

            low_stock_products()

        elif choice == "4":

            break

        else:

            print("Invalid Choice.")

            pause()



# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    create_tables()

    initialize_passwords()

    while True:

        user = login()

        if user is None:

            print("\nThank you for using the Inventory Management System.")

            break

        if user["role"] == "admin":

            admin_menu()

        elif user["role"] == "cashier":

            cashier_menu()

# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    main()
