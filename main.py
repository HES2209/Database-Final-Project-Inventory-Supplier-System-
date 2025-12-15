import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import hashlib
import time
import re

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory & Supplier Management System")
        self.root.geometry("1000x700")

        # Initialize Database
        self.conn = sqlite3.connect("datatech.db")
        self.cursor = self.conn.cursor()
        self.init_db()
        self.seed_data() # Add some sample data if empty

        # User session
        self.current_user = None
        self.current_role = None
        self.current_related_id = None

        # Show login first
        self.show_login()

    def show_login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Login")
        login_win.geometry("300x200")
        login_win.transient(self.root)
        login_win.grab_set()
        login_win.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        ttk.Label(login_win, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        ent_username = ttk.Entry(login_win)
        ent_username.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(login_win, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        ent_password = ttk.Entry(login_win, show="*")
        ent_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(login_win, text="Role:").grid(row=2, column=0, padx=10, pady=10)
        role_var = tk.StringVar(value="customer")
        ttk.Radiobutton(login_win, text="Customer", variable=role_var, value="customer").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(login_win, text="Supplier", variable=role_var, value="supplier").grid(row=2, column=1, sticky="e")

        def login():
            username = ent_username.get()
            password = hashlib.sha256(ent_password.get().encode()).hexdigest()
            role = role_var.get()

            self.cursor.execute("SELECT UserID, RelatedID FROM User WHERE Username=? AND PasswordHash=? AND Role=?", (username, password, role))
            user = self.cursor.fetchone()
            if user:
                self.current_user = user[0]
                self.current_role = role
                self.current_related_id = user[1]
                login_win.destroy()
                self.build_ui_based_on_role()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        ttk.Button(login_win, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(login_win, text="Register", command=self.show_registration).grid(row=4, column=0, columnspan=2, pady=10)

    def show_registration(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Register")
        reg_win.geometry("400x400")
        reg_win.transient(self.root)
        reg_win.grab_set()

        ttk.Label(reg_win, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        ent_reg_username = ttk.Entry(reg_win)
        ent_reg_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(reg_win, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        ent_reg_password = ttk.Entry(reg_win, show="*")
        ent_reg_password.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(reg_win, text="Role:").grid(row=2, column=0, padx=10, pady=5)
        role_var = tk.StringVar(value="customer")
        ttk.Radiobutton(reg_win, text="Customer", variable=role_var, value="customer").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(reg_win, text="Supplier", variable=role_var, value="supplier").grid(row=2, column=1, sticky="e")

        # Dynamic fields based on role
        self.reg_entries = {}

        def update_fields():
            # Clear previous fields
            for widget in reg_win.grid_slaves():
                if int(widget.grid_info()["row"]) > 2:
                    widget.destroy()

            role = role_var.get()
            row = 3
            if role == "customer":
                fields = [("First Name:", "firstname"), ("Last Name:", "lastname"), ("Email:", "email"), ("Phone:", "phone"), ("Address:", "address")]
            else:
                fields = [("Supplier Name:", "suppliername"), ("Contact Person:", "contactperson"), ("Email:", "email"), ("Phone:", "phone"), ("Address:", "address")]

            for label_text, key in fields:
                ttk.Label(reg_win, text=label_text).grid(row=row, column=0, padx=10, pady=5)
                entry = ttk.Entry(reg_win)
                entry.grid(row=row, column=1, padx=10, pady=5)
                self.reg_entries[key] = entry
                row += 1

            ttk.Button(reg_win, text="Register", command=lambda: self.register(reg_win, ent_reg_username.get(), ent_reg_password.get(), role_var.get())).grid(row=row, column=0, columnspan=2, pady=10)

        role_var.trace("w", lambda *args: update_fields())
        update_fields()

    def register(self, reg_win, username, password, role):
        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required")
            return

        # Check if username exists
        self.cursor.execute("SELECT Username FROM User WHERE Username=?", (username,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Username already exists")
            return

        # Generate new ID
        if role == "customer":
            self.cursor.execute("SELECT MAX(CAST(SUBSTR(CustomerID, 5) AS INTEGER)) FROM Customer")
            max_id = self.cursor.fetchone()[0] or 0
            new_id = f"CUST{max_id + 1:03d}"
            data = (
                new_id,
                self.reg_entries["firstname"].get(),
                self.reg_entries["lastname"].get(),
                self.reg_entries["email"].get(),
                self.reg_entries["phone"].get(),
                self.reg_entries["address"].get()
            )
            self.cursor.execute("INSERT INTO Customer VALUES (?,?,?,?,?,?)", data)
        else:
            self.cursor.execute("SELECT MAX(CAST(SUBSTR(SupplierID, 4) AS INTEGER)) FROM Supplier")
            max_id = self.cursor.fetchone()[0] or 0
            new_id = f"SUP{max_id + 1:03d}"
            data = (
                new_id,
                self.reg_entries["suppliername"].get(),
                self.reg_entries["contactperson"].get(),
                self.reg_entries["email"].get(),
                self.reg_entries["phone"].get(),
                self.reg_entries["address"].get()
            )
            self.cursor.execute("INSERT INTO Supplier VALUES (?,?,?,?,?,?)", data)

        # Generate UserID
        self.cursor.execute("SELECT MAX(CAST(SUBSTR(UserID, 5) AS INTEGER)) FROM User")
        max_user_id = self.cursor.fetchone()[0] or 0
        user_id = f"USER{max_user_id + 1:03d}"

        # Insert User
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO User VALUES (?,?,?,?,?)", (user_id, username, password_hash, role, new_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        reg_win.destroy()

    def build_ui_based_on_role(self):
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("TLabel", font=('Arial', 10))
        self.style.configure("TButton", font=('Arial', 10))

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Create Frames for Tabs
        self.frame_dashboard = ttk.Frame(self.notebook)
        self.frame_suppliers = ttk.Frame(self.notebook)
        self.frame_products = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_dashboard, text="Dashboard")
        self.notebook.add(self.frame_products, text="Products & Inventory")

        if self.current_role == "supplier":
            self.frame_supplier_log = ttk.Frame(self.notebook)
            self.frame_orders = ttk.Frame(self.notebook)
            self.notebook.add(self.frame_orders, text="Orders")
            self.notebook.add(self.frame_supplier_log, text="Supplier Log")
        elif self.current_role == "customer":
            self.frame_cart = ttk.Frame(self.notebook)
            self.notebook.add(self.frame_cart, text="Shopping Cart")

        # Build UIs
        self.build_dashboard()
        self.build_products_ui()

        if self.current_role == "supplier":
            self.build_orders_ui()
            self.build_supplier_log_ui()
        elif self.current_role == "customer":
            self.build_cart_ui()

        # Show main window after login
        self.root.deiconify()

    def init_db(self):
        """Recreating the User's SQL Schema in SQLite"""
        
        # 1. Supplier Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Supplier (
                SupplierID TEXT PRIMARY KEY,
                SupplierName TEXT NOT NULL,
                ContactPerson TEXT,
                Email TEXT,
                PhoneNumber TEXT,
                Address TEXT
            )
        """)

        # 2. Category Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                CategoryID TEXT PRIMARY KEY,
                SupplierID TEXT,
                CategoryName TEXT,
                FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
            )
        """)

        # 3. Product Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Product (
                ProductID TEXT PRIMARY KEY,
                CategoryID TEXT,
                ProductName TEXT,
                Description TEXT,
                Price REAL,
                Availability TEXT,
                StockQuantity INTEGER DEFAULT 0,
                ImagePath TEXT,
                FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
            )
        """)
        # Add StockQuantity column if not exists
        try:
            self.cursor.execute("ALTER TABLE Product ADD COLUMN StockQuantity INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # Column already exists

        # 4. Shelfloc (Inventory)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Shelfloc (
                Shelfloc TEXT PRIMARY KEY,
                ProductID TEXT,
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 4b. InventorySlot (allows multiple units per shelfloc)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InventorySlot (
                SlotID INTEGER PRIMARY KEY AUTOINCREMENT,
                Shelfloc TEXT,
                ProductID TEXT,
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 5. Customer
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerID TEXT PRIMARY KEY,
                FirstName TEXT,
                LastName TEXT,
                Email TEXT,
                PhoneNumber TEXT,
                Address TEXT
            )
        """)

        # 6. CustomerOrderItem
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS CustomerOrderItem (
                CustomerOrderItemID TEXT PRIMARY KEY,
                CustomerID TEXT,
                ProductID TEXT,
                Shelfloc TEXT,
                CustomerOrderDate TEXT,
                PaymentMethod TEXT,
                CustomerOrderItemStatus TEXT,
                EstimatedTime TEXT,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 6.5. SupplierOrderItem
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SupplierOrderItem (
                SupplierOrderItemID TEXT PRIMARY KEY,
                SupplierID TEXT,
                ProductID TEXT,
                SupplierOrderDate TEXT,
                SupplierOrderItemStatus TEXT,
                EstimatedTime TEXT,
                FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 7. User Table for Login
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                UserID TEXT PRIMARY KEY,
                Username TEXT UNIQUE NOT NULL,
                PasswordHash TEXT NOT NULL,
                Role TEXT NOT NULL,  -- 'supplier' or 'customer'
                RelatedID TEXT,  -- SupplierID or CustomerID
                FOREIGN KEY (RelatedID) REFERENCES Supplier(SupplierID),
                FOREIGN KEY (RelatedID) REFERENCES Customer(CustomerID)
            )
        """)

        # 8. SupplierLog Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SupplierLog (
                LogID INTEGER PRIMARY KEY AUTOINCREMENT,
                SupplierID TEXT,
                ProductID TEXT,
                LogDate TEXT,
                Message TEXT,
                FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 9. Cart Table for Customer Shopping Carts
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cart (
                CartID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID TEXT,
                ProductID TEXT,
                Quantity INTEGER DEFAULT 1,
                AddedDate TEXT,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        # 10. Rating Table for Product Ratings
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rating (
                RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID TEXT,
                ProductID TEXT,
                Rating INTEGER CHECK(Rating >= 1 AND Rating <= 5),
                Review TEXT,
                RatingDate TEXT,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        """)

        self.conn.commit()

        # Backfill InventorySlot from legacy Shelfloc if needed
        self.cursor.execute("SELECT count(*) FROM InventorySlot")
        inv_slots = self.cursor.fetchone()[0]
        if inv_slots == 0:
            self.cursor.execute("SELECT Shelfloc, ProductID FROM Shelfloc")
            legacy_rows = self.cursor.fetchall()
            if legacy_rows:
                self.cursor.executemany(
                    "INSERT INTO InventorySlot (Shelfloc, ProductID) VALUES (?, ?)",
                    legacy_rows,
                )
                self.conn.commit()

    def seed_data(self):
        """Add user's data if tables are empty"""
        self.cursor.execute("SELECT count(*) FROM Supplier")
        if self.cursor.fetchone()[0] == 0:
            # Add Suppliers from user's data
            suppliers = [
                ('1', 'Supplier1', 'Aaron', 'Aaron999@gmail.com', '087771182399', 'Jakarta Barat'),
                ('13', 'Supplier2', 'Mugen', 'MM_000@yahoo.com', '087278982399', 'Jakarta Selatan'),
                ('22', 'Supplier3', 'Chris', 'AChris22@gmail.com', '087770972399', 'Jakarta Utara'),
                ('7', 'Supplier4', 'Simon', 'Simon_Alex@gmail.com', '0877711276290', 'BSD'),
                ('12', 'Supplier5', 'Audrey', 'AudreyM@gmail.com', '0774981182309', 'Alam Sutera'),
                ('9', 'Supplier6', 'Janice', 'JJanice777@gmail.com', '050771184478', 'Jakarta Utara')
            ]
            self.cursor.executemany("INSERT INTO Supplier VALUES (?,?,?,?,?,?)", suppliers)

            # Add Categories
            categories = [
                ('CAT01', '1', 'Laptops and Computers'),
                ('CAT02', '13', 'Printers & Scanners'),
                ('CAT03', '22', 'Stationery'),
                ('CAT04', '7', 'Computer Components')
            ]
            self.cursor.executemany("INSERT INTO Category VALUES (?,?,?)", categories)

            # Add Products
            products = [
                # CAT01 Laptops & Monitors
                ('PROD101', 'CAT01', 'NovaBook Pro 15"', '16GB RAM, 512GB SSD, Silver', 20799000.00, 'In Stock', 0, ''),
                ('PROD102', 'CAT01', 'Zenith Laptop 13"', '8GB RAM, 256GB SSD, Black', 14999000.00, 'In Stock', 0, ''),
                ('PROD103', 'CAT01', 'UltraWide Monitor 34"', 'Curved QHD display for multitasking', 7999000.00, 'In Stock', 0, ''),
                ('PROD104', 'CAT01', 'NovaBook Air 14"', '16GB RAM, 1TB SSD, Graphite', 18999000.00, 'In Stock', 0, ''),
                ('PROD105', 'CAT01', 'Zenith Laptop 15"', '32GB RAM, 1TB SSD, Midnight Blue', 23999000.00, 'In Stock', 0, ''),
                ('PROD106', 'CAT01', 'Creator Display 27"', '4K IPS, 99% sRGB, factory calibrated', 9999000.00, 'In Stock', 0, ''),
                # CAT02 Printers & Scanners
                ('PROD201', 'CAT02', 'All-in-One Printer X5', 'Wireless color printer and scanner', 3999000.00, 'In Stock', 0, ''),
                ('PROD202', 'CAT02', 'Mono Laser Printer L2', 'Fast duplex monochrome printing', 2299000.00, 'In Stock', 0, ''),
                # CAT03 Stationery
                ('PROD301', 'CAT03', 'Premium Gel Pens (12-pack)', 'Assorted colors, smooth writing', 20000.00, 'In Stock', 0, ''),
                ('PROD302', 'CAT03', 'A5 Dotted Notebook', '120gsm ivory paper, lay-flat', 65000.00, 'In Stock', 0, ''),
                ('PROD303', 'CAT03', 'Mechanical Pencil 0.5mm', 'Metal body, knurled grip', 45000.00, 'In Stock', 0, ''),
                # CAT04 Components & Peripherals
                ('PROD401', 'CAT04', 'Gaming Mouse RGB', 'Programmable buttons, 16000 DPI', 150000.00, 'In Stock', 0, ''),
                ('PROD402', 'CAT04', 'Mechanical Keyboard TKL', 'Hot-swap switches, white backlight', 850000.00, 'In Stock', 0, ''),
                ('PROD403', 'CAT04', 'NVMe SSD 1TB Gen4', 'Up to 7000MB/s read', 1499000.00, 'In Stock', 0, '')
            ]
            self.cursor.executemany("INSERT INTO Product VALUES (?,?,?,?,?,?,?,?)", products)

            # Add Shelfloc
            shelflocs = [
                ('A1', 'PROD101'),
                ('A2', 'PROD102'),
                ('A3', 'PROD103'),
                ('A4', 'PROD104'),
                ('A5', 'PROD105'),
                ('A6', 'PROD106'),
                ('B1', 'PROD201'),
                ('B2', 'PROD202'),
                ('C1', 'PROD301'),
                ('C2', 'PROD302'),
                ('C3', 'PROD303'),
                ('D1', 'PROD401'),
                ('D2', 'PROD402'),
                ('D3', 'PROD403')
            ]
            self.cursor.executemany("INSERT INTO Shelfloc VALUES (?,?)", shelflocs)

            # Mirror Shelfloc into InventorySlot (1 unit per entry)
            self.cursor.executemany(
                "INSERT INTO InventorySlot (Shelfloc, ProductID) VALUES (?, ?)",
                shelflocs,
            )

            # Add Customers
            customers = [
                ('CUST501', 'Alice', 'Johnson', 'alice_johnson@gmail.com', '089922010223', 'Jl. Meruya Ilir Raya No. 25, Srengseng, Kecamatan Kembangan, Jakarta Barat'),
                ('CUST502', 'Robert', 'Judaly', 'rodaly@yahoo.com', '087581928033', 'Komplek Taman Ratu Indah Blok B3 No. 7, Duri Kepa, Kecamatan Kebon Jeruk, Jakarta Barat'),
                ('CUST503', 'Mark', 'Revener', 'mark.reven@gmail.com', '085182730486', 'Jl. Bintaro Utama Sektor 3A, Pondok Ranji, Kecamatan Ciputat Timur, Tangerang Selatan'),
                ('CUST504', 'Lizzy', 'Amalka', 'Lizzyamalka@gmail.com', '082193489383', 'Jl. Permata Hijau Blok AA No. 12, Grogol Utara, Kecamatan Kebayoran Lama, Jakarta Selatan')
            ]
            self.cursor.executemany("INSERT INTO Customer VALUES (?,?,?,?,?,?)", customers)

            # Add CustomerOrderItem
            orders = [
                ('COI001', 'CUST501', 'PROD101', 'A1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
                ('COI002', 'CUST501', 'PROD301', 'C1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
                ('COI003', 'CUST502', 'PROD201', 'B1', '2025-12-02', 'Debit Card', 'On the way', '2 Days'),
                ('COI004', 'CUST503', 'PROD401', 'D1', '2025-12-01', 'Transfer', 'Delayed', '7 Days')
            ]
            self.cursor.executemany("INSERT INTO CustomerOrderItem VALUES (?,?,?,?,?,?,?,?)", orders)

            # Add SupplierOrderItem
            supplier_orders = [
                ('SOI001', '1', 'PROD101', '2025-11-20', 'Arrived', '3 Days'),
                ('SOI002', '13', 'PROD201', '2025-11-25', 'On the way', '5 Days')
            ]
            self.cursor.executemany("INSERT INTO SupplierOrderItem VALUES (?,?,?,?,?,?)", supplier_orders)

            # Add Users (sample, since not provided)
            users = [
                ('USER001', 'alice', hashlib.sha256('pass123'.encode()).hexdigest(), 'customer', 'CUST501'),
                ('USER002', 'aaron', hashlib.sha256('pass123'.encode()).hexdigest(), 'supplier', '1')
            ]
            self.cursor.executemany("INSERT INTO User VALUES (?,?,?,?,?)", users)

            self.conn.commit()
            print("Database seeded with user's data.")

    # ================= UI BUILDERS =================

    def build_dashboard(self):
        lbl_title = tk.Label(self.frame_dashboard, text="Inventory & Supplier Dashboard", font=("Arial", 18, "bold"))
        lbl_title.pack(pady=10)

        cards = ttk.Frame(self.frame_dashboard)
        cards.pack(fill="x", padx=12, pady=6)

        # KPI cards
        self.kpi_prod = tk.Label(cards, text="Products\n0", font=("Arial", 12, "bold"), bg="#e0f2fe", width=16, height=3)
        self.kpi_prod.grid(row=0, column=0, padx=6, pady=6)

        self.kpi_stock = tk.Label(cards, text="Total Stock\n0", font=("Arial", 12, "bold"), bg="#ecfdf3", width=16, height=3)
        self.kpi_stock.grid(row=0, column=1, padx=6, pady=6)

        self.kpi_orders = tk.Label(cards, text="Orders\n0", font=("Arial", 12, "bold"), bg="#fef3c7", width=16, height=3)
        self.kpi_orders.grid(row=0, column=2, padx=6, pady=6)

        if self.current_role == "supplier":
            self.kpi_lowstock = tk.Label(cards, text="Low Stock\n0", font=("Arial", 12, "bold"), bg="#fee2e2", width=16, height=3)
            self.kpi_lowstock.grid(row=0, column=3, padx=6, pady=6)

        # Lists: low stock (supplier) or recent orders (customer)
        list_frame = ttk.Frame(self.frame_dashboard)
        list_frame.pack(fill="both", expand=True, padx=12, pady=6)

        if self.current_role == "supplier":
            box_title = "Low Stock (Top 10)"
            self.tree_dash = ttk.Treeview(list_frame, columns=("Product", "Shelf", "Stock"), show="headings", height=10)
            for col, width in [("Product", 200), ("Shelf", 160), ("Stock", 80)]:
                self.tree_dash.heading(col, text=col)
                self.tree_dash.column(col, width=width)
        else:
            box_title = "Recent Orders"
            self.tree_dash = ttk.Treeview(list_frame, columns=("Order", "Product", "Status", "Date"), show="headings", height=10)
            for col, width in [("Order", 120), ("Product", 200), ("Status", 120), ("Date", 140)]:
                self.tree_dash.heading(col, text=col)
                self.tree_dash.column(col, width=width)

        ttk.Label(list_frame, text=box_title, font=("Arial", 12, "bold")).pack(anchor="w", pady=4)
        self.tree_dash.pack(fill="both", expand=True)
        self.bind_mousewheel(self.tree_dash, target="tree")

        actions = ttk.Frame(self.frame_dashboard)
        actions.pack(pady=8)
        ttk.Button(actions, text="Refresh", command=self.refresh_dashboard).grid(row=0, column=0, padx=6)
        ttk.Button(actions, text="Logout", command=self.logout).grid(row=0, column=1, padx=6)

        self.refresh_dashboard()

    def build_suppliers_ui(self):
        # -- Top: Form --
        form_frame = ttk.LabelFrame(self.frame_suppliers, text="Add New Supplier")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_sup_id = ttk.Entry(form_frame)
        self.ent_sup_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_sup_name = ttk.Entry(form_frame)
        self.ent_sup_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact:").grid(row=0, column=4, padx=5, pady=5)
        self.ent_sup_contact = ttk.Entry(form_frame)
        self.ent_sup_contact.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_sup_email = ttk.Entry(form_frame)
        self.ent_sup_email.grid(row=1, column=1, padx=5, pady=5)

        btn_add = ttk.Button(form_frame, text="Save Supplier", command=self.add_supplier)
        btn_add.grid(row=1, column=4, columnspan=2, sticky="ew", padx=5)

        # -- Bottom: Table --
        tree_frame = ttk.Frame(self.frame_suppliers)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID", "Name", "Contact", "Email", "Phone", "Address")
        self.tree_suppliers = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree_suppliers.heading(col, text=col)
            self.tree_suppliers.column(col, width=100)

        self.tree_suppliers.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_suppliers.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_suppliers.configure(yscrollcommand=scrollbar.set)

        self.load_suppliers()

    def build_products_ui(self):
        # Toolbar - search, category, sort (Tokopedia-like discovery controls)
        filter_frame = ttk.LabelFrame(self.frame_products, text="Find Products")
        filter_frame.pack(fill="x", padx=10, pady=5)

        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All Categories")
        self.sort_var = tk.StringVar(value="Most Relevant")

        ttk.Label(filter_frame, text="Search").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ent_search = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        ent_search.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ent_search.bind("<Return>", lambda _e: self.load_products())

        ttk.Label(filter_frame, text="Category").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cmb_category = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly", width=25)
        self.cmb_category.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(filter_frame, text="Sort").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.cmb_sort = ttk.Combobox(filter_frame, textvariable=self.sort_var, state="readonly", width=20)
        self.cmb_sort["values"] = ["Most Relevant", "Price: Low to High", "Price: High to Low", "Top Rated", "Stock: High to Low"]
        self.cmb_sort.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        ttk.Button(filter_frame, text="Apply", command=self.load_products).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(filter_frame, text="Reset", command=self.reset_product_filters).grid(row=0, column=7, padx=5, pady=5)

        # -- Top: Form --
        if self.current_role == "supplier":
            form_frame = ttk.LabelFrame(self.frame_products, text="Add New Product")
            form_frame.pack(fill="x", padx=10, pady=5)

            ttk.Label(form_frame, text="Prod ID:").grid(row=0, column=0)
            self.ent_prod_id = ttk.Entry(form_frame)
            self.ent_prod_id.grid(row=0, column=1)

            ttk.Label(form_frame, text="Name:").grid(row=0, column=2)
            self.ent_prod_name = ttk.Entry(form_frame)
            self.ent_prod_name.grid(row=0, column=3)

            ttk.Label(form_frame, text="Price:").grid(row=0, column=4)
            self.ent_prod_price = ttk.Entry(form_frame)
            self.ent_prod_price.grid(row=0, column=5)

            ttk.Label(form_frame, text="Cat ID:").grid(row=1, column=0)
            self.ent_prod_cat = ttk.Entry(form_frame)
            self.ent_prod_cat.grid(row=1, column=1)

            ttk.Label(form_frame, text="Description:").grid(row=1, column=2)
            self.ent_prod_desc = ttk.Entry(form_frame)
            self.ent_prod_desc.grid(row=1, column=3)

            ttk.Label(form_frame, text="Stock Quantity:").grid(row=2, column=0)
            self.ent_prod_stock = ttk.Entry(form_frame)
            self.ent_prod_stock.grid(row=2, column=1)

            btn_add = ttk.Button(form_frame, text="Save Product", command=self.add_product)
            btn_add.grid(row=3, column=2, columnspan=2, sticky="ew", padx=5)

        # -- Bottom: Scrollable Product List --
        tree_frame = ttk.Frame(self.frame_products)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create canvas and scrollbar for scrollable frame
        self.canvas = tk.Canvas(tree_frame, bg="white")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mouse-wheel scrolling on the canvas
        self.bind_mousewheel(self.canvas, target="canvas")

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_products()

    def build_orders_ui(self):
        lbl = ttk.Label(self.frame_orders, text="Customer Orders Overview", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        tree_frame = ttk.Frame(self.frame_orders)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Order ID", "Customer", "Product", "Shelf", "Date", "Payment", "Status", "Est Time")
        self.tree_orders = ttk.Treeview(tree_frame, columns=cols, show="headings")

        for col in cols:
            self.tree_orders.heading(col, text=col)
            self.tree_orders.column(col, width=100)

        self.tree_orders.pack(fill="both", expand=True)
        self.bind_mousewheel(self.tree_orders, target="tree")
        self.load_orders()

    def build_supplier_log_ui(self):
        lbl = ttk.Label(self.frame_supplier_log, text="Supplier Log - Products Needing Supply", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        form = ttk.LabelFrame(self.frame_supplier_log, text="Add Stock to Low Items")
        form.pack(fill="x", padx=10, pady=5)

        self.log_product_var = tk.StringVar()
        self.log_shelf_var = tk.StringVar()
        self.log_qty_var = tk.IntVar(value=1)

        ttk.Label(form, text="Product").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cmb_log_product = ttk.Combobox(form, textvariable=self.log_product_var, state="readonly", width=35)
        self.cmb_log_product.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Shelfloc").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ent_shelf = ttk.Entry(form, textvariable=self.log_shelf_var, width=10)
        ent_shelf.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Qty").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        spin_qty = ttk.Spinbox(form, from_=1, to=999, width=6, textvariable=self.log_qty_var)
        spin_qty.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        ttk.Button(form, text="Add Stock", command=self.add_stock_from_log).grid(row=0, column=6, padx=10, pady=5, sticky="ew")

        tree_frame = ttk.Frame(self.frame_supplier_log)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Product ID", "Name", "Category", "Stock", "Status", "Shelves")
        self.tree_supplier_log = ttk.Treeview(tree_frame, columns=cols, show="headings")

        widths = [100, 180, 140, 80, 110, 200]
        for col, w in zip(cols, widths):
            self.tree_supplier_log.heading(col, text=col)
            self.tree_supplier_log.column(col, width=w)

        self.tree_supplier_log.pack(fill="both", expand=True)
        self.bind_mousewheel(self.tree_supplier_log, target="tree")
        self.load_supplier_log()

    # ================= LOGIC & DATA =================

    def refresh_dashboard(self):
        # Products
        self.cursor.execute("SELECT count(*) FROM Product")
        count_prod = self.cursor.fetchone()[0]
        self.kpi_prod.config(text=f"Products\n{count_prod}")

        # Stock from InventorySlot
        self.cursor.execute("SELECT count(*) FROM InventorySlot")
        total_stock = self.cursor.fetchone()[0]
        self.kpi_stock.config(text=f"Total Stock\n{total_stock}")

        # Orders by role
        if self.current_role == "customer":
            self.cursor.execute("SELECT count(*) FROM CustomerOrderItem WHERE CustomerID=?", (self.current_related_id,))
        else:
            self.cursor.execute(
                """
                SELECT count(*)
                FROM CustomerOrderItem coi
                JOIN Product p ON coi.ProductID = p.ProductID
                JOIN Category c ON p.CategoryID = c.CategoryID
                WHERE c.SupplierID = ?
                """,
                (self.current_related_id,),
            )
        count_ord = self.cursor.fetchone()[0]
        self.kpi_orders.config(text=f"Orders\n{count_ord}")

        # Low stock (supplier only)
        if self.current_role == "supplier":
            self.cursor.execute(
                """
                SELECT p.ProductName,
                       GROUP_CONCAT(inv.Shelfloc || ' x' || inv.count_per_shelf, ', ') as shelf_summary,
                       SUM(inv.count_per_shelf) as stock_sum
                FROM (
                    SELECT ProductID, Shelfloc, COUNT(*) as count_per_shelf
                    FROM InventorySlot
                    GROUP BY ProductID, Shelfloc
                ) inv
                JOIN Product p ON p.ProductID = inv.ProductID
                JOIN Category c ON p.CategoryID = c.CategoryID
                WHERE c.SupplierID = ?
                GROUP BY inv.ProductID
                ORDER BY stock_sum ASC
                LIMIT 10
                """,
                (self.current_related_id,),
            )
            rows = self.cursor.fetchall()
            for item in self.tree_dash.get_children():
                self.tree_dash.delete(item)
            for prod, shelf_summary, stock_sum in rows:
                self.tree_dash.insert("", "end", values=(prod, shelf_summary or "-", stock_sum))
            low_stock_count = sum(1 for _ in rows)
            self.kpi_lowstock.config(text=f"Low Stock\n{low_stock_count}")
        else:
            # Recent orders for customer
            self.cursor.execute(
                """
                SELECT coi.CustomerOrderItemID, p.ProductName, coi.CustomerOrderItemStatus, coi.CustomerOrderDate
                FROM CustomerOrderItem coi
                JOIN Product p ON coi.ProductID = p.ProductID
                WHERE coi.CustomerID = ?
                ORDER BY coi.CustomerOrderDate DESC
                LIMIT 10
                """,
                (self.current_related_id,),
            )
            rows = self.cursor.fetchall()
            for item in self.tree_dash.get_children():
                self.tree_dash.delete(item)
            for order_id, prod_name, status, date in rows:
                self.tree_dash.insert("", "end", values=(order_id, prod_name, status, date))

    def load_suppliers(self):
        for item in self.tree_suppliers.get_children():
            self.tree_suppliers.delete(item)
        
        self.cursor.execute("SELECT * FROM Supplier")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_suppliers.insert("", "end", values=row)
        self.bind_mousewheel(self.tree_suppliers, target="tree")

    def bind_mousewheel(self, widget, target="tree"):
        """Enable mouse wheel scrolling for Treeview or Canvas."""
        def _on_mousewheel(event):
            delta = int(-1 * (event.delta / 120))
            if target == "tree":
                widget.yview_scroll(delta, "units")
            elif target == "canvas":
                widget.yview_scroll(delta, "units")
            return "break"

        widget.bind_all("<MouseWheel>", _on_mousewheel)

    def get_category_options(self):
        self.cursor.execute("SELECT CategoryName FROM Category ORDER BY CategoryName")
        return [row[0] for row in self.cursor.fetchall()]

    def get_supplier_products_for_log(self):
        self.cursor.execute(
            """
            SELECT p.ProductID, p.ProductName
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            WHERE c.SupplierID = ?
            ORDER BY p.ProductName
            """,
            (self.current_related_id,),
        )
        return self.cursor.fetchall()

    def reset_product_filters(self):
        if hasattr(self, "search_var"):
            self.search_var.set("")
        if hasattr(self, "category_var"):
            self.category_var.set("All Categories")
        if hasattr(self, "sort_var"):
            self.sort_var.set("Most Relevant")
        self.load_products()

    def add_supplier(self):
        try:
            data = (
                self.ent_sup_id.get(),
                self.ent_sup_name.get(),
                self.ent_sup_contact.get(),
                self.ent_sup_email.get(),
                "0000", # Placeholder phone
                "Unknown" # Placeholder Addr
            )
            if not data[0] or not data[1]:
                messagebox.showerror("Error", "ID and Name are required")
                return

            self.cursor.execute("INSERT INTO Supplier VALUES (?,?,?,?,?,?)", data)
            self.conn.commit()
            messagebox.showinfo("Success", "Supplier Added")
            self.load_suppliers()
            self.refresh_dashboard()
            
            # Clear inputs
            self.ent_sup_id.delete(0, tk.END)
            self.ent_sup_name.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Supplier ID already exists")

    def load_products(self):
        # Clear existing product cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Sync category filter options
        if hasattr(self, "cmb_category"):
            options = ["All Categories"] + self.get_category_options()
            self.cmb_category["values"] = options
            if self.category_var.get() not in options:
                self.category_var.set("All Categories")

        # Group by product to count shelfloc as stock
        clauses = []
        params = []

        search_term = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        if search_term:
            like_term = f"%{search_term}%"
            clauses.append("(p.ProductName LIKE ? OR p.Description LIKE ?)")
            params.extend([like_term, like_term])

        category_filter = self.category_var.get() if hasattr(self, "category_var") else "All Categories"
        if category_filter and category_filter != "All Categories":
            clauses.append("c.CategoryName = ?")
            params.append(category_filter)

        base_query = """
            SELECT p.ProductID, p.CategoryID, p.ProductName, p.Description, p.Price, p.Availability,
                   IFNULL(inv.Stock, 0) as Stock,
                   IFNULL(inv.ShelfSummary, '') as ShelfSummary,
                   IFNULL(r.AvgRating, 0) as AvgRating,
                   IFNULL(r.RatingCount, 0) as RatingCount,
                   IFNULL(c.CategoryName, 'Uncategorized') as CategoryName
            FROM Product p
            LEFT JOIN Category c ON p.CategoryID = c.CategoryID
            LEFT JOIN (
                SELECT ProductID,
                       SUM(count_per_shelf) as Stock,
                       GROUP_CONCAT(Shelfloc || ' x' || count_per_shelf, ', ') as ShelfSummary
                FROM (
                    SELECT ProductID, Shelfloc, COUNT(*) as count_per_shelf
                    FROM InventorySlot
                    GROUP BY ProductID, Shelfloc
                )
                GROUP BY ProductID
            ) inv ON p.ProductID = inv.ProductID
            LEFT JOIN (
                SELECT ProductID, AVG(Rating) as AvgRating, COUNT(RatingID) as RatingCount
                FROM Rating
                GROUP BY ProductID
            ) r ON p.ProductID = r.ProductID
        """

        if clauses:
            base_query += " WHERE " + " AND ".join(clauses)

        base_query += " GROUP BY p.ProductID, p.CategoryID, p.ProductName, p.Description, p.Price, p.Availability"

        sort_choice = self.sort_var.get() if hasattr(self, "sort_var") else "Most Relevant"
        order_clause = " ORDER BY RatingCount DESC, AvgRating DESC"  # default like Tokopedia relevance
        if sort_choice == "Price: Low to High":
            order_clause = " ORDER BY p.Price ASC"
        elif sort_choice == "Price: High to Low":
            order_clause = " ORDER BY p.Price DESC"
        elif sort_choice == "Top Rated":
            order_clause = " ORDER BY AvgRating DESC, RatingCount DESC"
        elif sort_choice == "Stock: High to Low":
            order_clause = " ORDER BY Stock DESC"

        query = base_query + order_clause
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        for row in rows:
            product_id, category_id, name, desc, price, availability, stock_count, shelf_summary, avg_rating, rating_count, category_name = row
            stock = int(stock_count) if stock_count else 0

            # Create product card frame
            card_frame = ttk.Frame(self.scrollable_frame, relief="raised", borderwidth=2)
            card_frame.pack(fill="x", padx=10, pady=5)

            # Product info
            ttk.Label(card_frame, text=f"{name}", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(card_frame, text=f"{category_name} · {product_id}", foreground="#4b5563").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(card_frame, text=desc, wraplength=520, foreground="#374151").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(card_frame, text=f"Rp {price:,.0f}", font=("Arial", 11, "bold"), foreground="#0f9d58").grid(row=3, column=0, sticky="w", padx=5, pady=2)

            rating_text = f"{avg_rating:.1f} ★ ({rating_count})" if rating_count else "Belum ada rating"
            ttk.Label(card_frame, text=rating_text, foreground="#f59e0b").grid(row=4, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(card_frame, text=f"Stock: {stock}").grid(row=5, column=0, sticky="w", padx=5, pady=2)

            if self.current_role == "supplier":
                ttk.Label(card_frame, text=f"Shelves: {shelf_summary or 'N/A'}", foreground="#6b7280").grid(row=6, column=0, sticky="w", padx=5, pady=2)

            # Availability badge
            badge_bg = "#d1fae5" if availability == "Available" else "#fee2e2"
            badge_fg = "#065f46" if availability == "Available" else "#991b1b"
            tk.Label(card_frame, text=availability, bg=badge_bg, fg=badge_fg, padx=8, pady=2).grid(row=0, column=1, padx=8, pady=2, sticky="e")

            # Actions
            action_frame = ttk.Frame(card_frame)
            action_frame.grid(row=3, column=1, rowspan=3, padx=10, pady=5, sticky="ne")

            ttk.Button(action_frame, text="View Detail", command=lambda pid=product_id: self.show_product_detail(pid)).grid(row=0, column=0, padx=5, pady=2, sticky="ew")

            if self.current_role == "customer":
                qty_var = tk.IntVar(value=1)
                ttk.Label(action_frame, text="Qty").grid(row=1, column=0, padx=5, pady=2, sticky="w")
                qty_spin = ttk.Spinbox(action_frame, from_=1, to=max(stock, 1), width=5, textvariable=qty_var)
                qty_spin.grid(row=2, column=0, padx=5, pady=2, sticky="w")

                state = tk.NORMAL if stock > 0 else tk.DISABLED
                ttk.Button(action_frame, text="Add to Cart", state=state, command=lambda pid=product_id, qv=qty_var: self.add_to_cart(pid, qv.get())).grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    def add_product(self):
        try:
            prod_id = self.ent_prod_id.get().strip().upper()
            cat_id = self.ent_prod_cat.get().strip()
            name = self.ent_prod_name.get().strip()
            desc = self.ent_prod_desc.get().strip()
            price_raw = self.ent_prod_price.get().strip()
            stock_raw = self.ent_prod_stock.get().strip()

            # Validate required fields
            if not prod_id or not cat_id or not name or not price_raw:
                messagebox.showerror("Error", "Product ID, Category ID, Name, and Price are required")
                return

            # Enforce ProductID pattern: PROD + 3 digits (e.g., PROD001)
            if not re.fullmatch(r"PROD\d{3}", prod_id):
                messagebox.showerror("Error", "Product ID must follow format PROD### (e.g., PROD001)")
                return

            # Parse numeric fields
            try:
                price_val = float(price_raw)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number")
                return
            try:
                stock_val = int(stock_raw) if stock_raw else 0
            except ValueError:
                messagebox.showerror("Error", "Stock Quantity must be an integer")
                return
            if price_val < 0 or stock_val < 0:
                messagebox.showerror("Error", "Price and Stock Quantity must be non-negative")
                return

            # Ensure ProductID is unique
            self.cursor.execute("SELECT 1 FROM Product WHERE ProductID=?", (prod_id,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Product ID already exists")
                return

            # Ensure supplier adds only to their own categories
            if self.current_role == "supplier":
                self.cursor.execute("SELECT SupplierID FROM Category WHERE CategoryID=?", (cat_id,))
                owner = self.cursor.fetchone()
                if not owner or owner[0] != self.current_related_id:
                    messagebox.showerror("Error", "You can only add products to your own categories.")
                    return
            else:
                # If somehow a non-supplier hits this button, block it.
                messagebox.showerror("Error", "Only suppliers can add products.")
                return

            data = (
                prod_id,
                cat_id,
                name,
                desc,
                price_val,
                "Available",
                stock_val,
                ""
            )

            self.cursor.execute("INSERT INTO Product VALUES (?,?,?,?,?,?,?,?)", data)
            self.conn.commit()
            messagebox.showinfo("Success", "Product Added")
            self.load_products()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add product: {e}")

    def show_product_detail(self, product_id):
        detail_win = tk.Toplevel(self.root)
        detail_win.title("Product Detail")
        detail_win.geometry("500x420")
        detail_win.transient(self.root)
        detail_win.grab_set()

        self.cursor.execute(
            """
            SELECT p.ProductName, p.Description, p.Price, p.Availability,
                   IFNULL(c.CategoryName, 'Uncategorized'), IFNULL(s.SupplierName, 'Unknown Supplier')
            FROM Product p
            LEFT JOIN Category c ON p.CategoryID = c.CategoryID
            LEFT JOIN Supplier s ON c.SupplierID = s.SupplierID
            WHERE p.ProductID = ?
            """,
            (product_id,),
        )
        row = self.cursor.fetchone()
        if not row:
            detail_win.destroy()
            messagebox.showerror("Error", "Product not found")
            return

        name, desc, price, availability, category_name, supplier_name = row

        self.cursor.execute(
            "SELECT IFNULL(AVG(Rating), 0), COUNT(RatingID) FROM Rating WHERE ProductID=?",
            (product_id,),
        )
        avg_rating, rating_count = self.cursor.fetchone()

        ttk.Label(detail_win, text=name, font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=6)
        ttk.Label(detail_win, text=f"{category_name} · Supplier: {supplier_name}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(detail_win, text=f"Rp {price:,.0f}", font=("Arial", 12, "bold"), foreground="#0f9d58").pack(anchor="w", padx=10, pady=4)
        ttk.Label(detail_win, text=f"Rating: {avg_rating:.1f} ★ ({rating_count})").pack(anchor="w", padx=10, pady=2)
        ttk.Label(detail_win, text=f"Availability: {availability}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(detail_win, text="Description:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=4)

        txt_desc = tk.Text(detail_win, height=10, wrap="word")
        txt_desc.pack(fill="both", expand=True, padx=10, pady=4)
        txt_desc.insert("1.0", desc)
        txt_desc.configure(state="disabled")

    def load_supplier_log(self):
        for item in self.tree_supplier_log.get_children():
            self.tree_supplier_log.delete(item)

        # Populate product dropdown for supplier
        if hasattr(self, "cmb_log_product"):
            options = [f"{pid} - {pname}" for pid, pname in self.get_supplier_products_for_log()]
            self.cmb_log_product["values"] = options
            if options and not self.log_product_var.get():
                self.log_product_var.set(options[0])

        query = """
            SELECT p.ProductID, p.ProductName, c.CategoryName,
                   IFNULL(inv.stock_sum, 0) as Stock,
                   CASE WHEN IFNULL(inv.stock_sum,0) <= 3 THEN 'Low Stock' ELSE 'OK' END as Status,
                   IFNULL(inv.shelf_summary, '') as Shelves
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            LEFT JOIN (
                SELECT ProductID,
                       SUM(count_per_shelf) as stock_sum,
                       GROUP_CONCAT(Shelfloc || ' x' || count_per_shelf, ', ') as shelf_summary
                FROM (
                    SELECT ProductID, Shelfloc, COUNT(*) as count_per_shelf
                    FROM InventorySlot
                    GROUP BY ProductID, Shelfloc
                )
                GROUP BY ProductID
            ) inv ON p.ProductID = inv.ProductID
            WHERE c.SupplierID = ?
            ORDER BY Stock ASC
        """
        self.cursor.execute(query, (self.current_related_id,))
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_supplier_log.insert("", "end", values=row)

    def build_cart_ui(self):
        lbl = ttk.Label(self.frame_cart, text="Shopping Cart", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        tree_frame = ttk.Frame(self.frame_cart)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Product ID", "Name", "Quantity", "Price", "Total", "Action")
        self.tree_cart = ttk.Treeview(tree_frame, columns=cols, show="headings")

        for col in cols:
            self.tree_cart.heading(col, text=col)
            self.tree_cart.column(col, width=100)

        self.tree_cart.pack(fill="both", expand=True)
        self.tree_cart.bind("<ButtonRelease-1>", self.on_cart_click)
        self.bind_mousewheel(self.tree_cart, target="tree")

        # Summary and payment selection
        summary_frame = ttk.LabelFrame(self.frame_cart, text="Checkout")
        summary_frame.pack(fill="x", padx=10, pady=5)

        self.cart_total_var = tk.StringVar(value="Rp 0")
        ttk.Label(summary_frame, text="Total:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(summary_frame, textvariable=self.cart_total_var, font=("Arial", 11, "bold"), foreground="#0f9d58").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(summary_frame, text="Payment Method:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cart_payment_var = tk.StringVar(value="Select")
        self.cmb_cart_payment = ttk.Combobox(summary_frame, textvariable=self.cart_payment_var, state="readonly", width=25)
        self.cmb_cart_payment["values"] = [
            "Credit Card",
            "Debit Card",
            "Bank Transfer",
            "E-Wallet",
            "Cash on Delivery",
        ]
        self.cmb_cart_payment.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_checkout = ttk.Button(summary_frame, text="Checkout", command=self.checkout)
        btn_checkout.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="ew")

        self.load_cart()

    def load_cart(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)

        query = """
            SELECT c.ProductID, p.ProductName, c.Quantity, p.Price, (c.Quantity * p.Price) as Total
            FROM Cart c
            JOIN Product p ON c.ProductID = p.ProductID
            WHERE c.CustomerID = ?
        """
        self.cursor.execute(query, (self.current_related_id,))
        rows = self.cursor.fetchall()
        total_sum = 0
        for row in rows:
            self.tree_cart.insert("", "end", values=row + ("Remove",))
            total_sum += row[4]

        if hasattr(self, "cart_total_var"):
            self.cart_total_var.set(f"Rp {total_sum:,.0f}")

    def add_to_cart(self, product_id, qty=1):
        if self.current_role != "customer":
            return
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            qty = 1
        qty = max(1, qty)

        # Check stock first (sum of InventorySlot rows for the product)
        self.cursor.execute("SELECT COUNT(*) FROM InventorySlot WHERE ProductID = ?", (product_id,))
        stock_row = self.cursor.fetchone()
        available_stock = int(stock_row[0]) if stock_row else 0
        if available_stock < qty:
            messagebox.showerror("Out of Stock", "Requested quantity exceeds available stock.")
            return

        # Check if already in cart
        self.cursor.execute("SELECT Quantity FROM Cart WHERE CustomerID=? AND ProductID=?", (self.current_related_id, product_id))
        existing = self.cursor.fetchone()
        if existing:
            self.cursor.execute("UPDATE Cart SET Quantity=Quantity+? WHERE CustomerID=? AND ProductID=?", (qty, self.current_related_id, product_id))
        else:
            self.cursor.execute("INSERT INTO Cart (CustomerID, ProductID, Quantity, AddedDate) VALUES (?, ?, ?, datetime('now'))", (self.current_related_id, product_id, qty))
        self.conn.commit()
        messagebox.showinfo("Success", "Added to cart!")
        self.load_cart()  # Refresh cart to show updated items

    def add_stock_from_log(self):
        if self.current_role != "supplier":
            return

        raw_product = self.log_product_var.get().strip() if hasattr(self, "log_product_var") else ""
        if not raw_product:
            messagebox.showerror("Error", "Select a product")
            return
        product_id = raw_product.split(" - ")[0].strip()

        shelfloc = self.log_shelf_var.get().strip() if hasattr(self, "log_shelf_var") else ""
        if not shelfloc:
            messagebox.showerror("Error", "Enter a shelfloc")
            return

        try:
            qty = int(self.log_qty_var.get()) if hasattr(self, "log_qty_var") else 1
        except (TypeError, ValueError):
            qty = 1
        if qty <= 0:
            messagebox.showerror("Error", "Quantity must be at least 1")
            return

        # Verify product ownership
        self.cursor.execute(
            """
            SELECT 1
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            WHERE p.ProductID = ? AND c.SupplierID = ?
            """,
            (product_id, self.current_related_id),
        )
        if not self.cursor.fetchone():
            messagebox.showerror("Error", "You can only add stock for your own products")
            return

        # Ensure shelfloc belongs to this product (or create mapping)
        self.cursor.execute("SELECT ProductID FROM Shelfloc WHERE Shelfloc = ?", (shelfloc,))
        existing = self.cursor.fetchone()
        if existing and existing[0] != product_id:
            messagebox.showerror("Error", "Shelfloc already mapped to another product")
            return
        if not existing:
            self.cursor.execute("INSERT INTO Shelfloc (Shelfloc, ProductID) VALUES (?, ?)", (shelfloc, product_id))

        # Insert inventory slots (1 row per unit)
        rows = [(shelfloc, product_id) for _ in range(qty)]
        self.cursor.executemany("INSERT INTO InventorySlot (Shelfloc, ProductID) VALUES (?, ?)", rows)
        self.conn.commit()

        messagebox.showinfo("Success", f"Added {qty} unit(s) to {shelfloc}")
        self.load_supplier_log()
        self.load_products()
        self.refresh_dashboard()

    def on_cart_click(self, event):
        if self.current_role != "customer":
            return
        item = self.tree_cart.identify_row(event.y)
        column = self.tree_cart.identify_column(event.x)
        if column == "#6":  # Action column
            values = self.tree_cart.item(item, "values")
            if values and values[5] == "Remove":
                product_id = values[0]
                self.cursor.execute("DELETE FROM Cart WHERE CustomerID=? AND ProductID=?", (self.current_related_id, product_id))
                self.conn.commit()
                self.load_cart()
                messagebox.showinfo("Success", "Removed from cart!")

    def checkout(self):
        # Validate cart
        self.cursor.execute("SELECT ProductID, Quantity FROM Cart WHERE CustomerID=?", (self.current_related_id,))
        cart_items = self.cursor.fetchall()
        if not cart_items:
            messagebox.showerror("Error", "Your cart is empty.")
            return

        payment_method = self.cart_payment_var.get() if hasattr(self, "cart_payment_var") else ""
        if not payment_method or payment_method == "Select":
            messagebox.showerror("Error", "Please choose a payment method before checkout.")
            return

        # Move cart items to orders
        for product_id, quantity in cart_items:
            # Create unique-ish order id using epoch millis
            order_id = f"COI{int(time.time() * 1000) % 1000000000:09d}"
            self.cursor.execute(
                """
                INSERT INTO CustomerOrderItem (CustomerOrderItemID, CustomerID, ProductID, CustomerOrderDate, PaymentMethod, CustomerOrderItemStatus, EstimatedTime)
                VALUES (?, ?, ?, datetime('now'), ?, 'Pending', '3 Days')
                """,
                (order_id, self.current_related_id, product_id, payment_method),
            )
        # Clear cart
        self.cursor.execute("DELETE FROM Cart WHERE CustomerID=?", (self.current_related_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Checkout completed!")
        self.load_cart()

    def load_orders(self):
        for item in self.tree_orders.get_children():
            self.tree_orders.delete(item)

        if self.current_role == "customer":
            self.cursor.execute(
                """
                SELECT coi.CustomerOrderItemID, coi.CustomerID, coi.ProductID, coi.Shelfloc, coi.CustomerOrderDate,
                       coi.PaymentMethod, coi.CustomerOrderItemStatus, coi.EstimatedTime
                FROM CustomerOrderItem coi
                WHERE coi.CustomerID = ?
                ORDER BY coi.CustomerOrderDate DESC
                """,
                (self.current_related_id,),
            )
            rows = self.cursor.fetchall()
        else:  # supplier view their products' orders
            self.cursor.execute(
                """
                SELECT coi.CustomerOrderItemID, coi.CustomerID, coi.ProductID, coi.Shelfloc, coi.CustomerOrderDate,
                       coi.PaymentMethod, coi.CustomerOrderItemStatus, coi.EstimatedTime
                FROM CustomerOrderItem coi
                JOIN Product p ON coi.ProductID = p.ProductID
                JOIN Category c ON p.CategoryID = c.CategoryID
                WHERE c.SupplierID = ?
                ORDER BY coi.CustomerOrderDate DESC
                """,
                (self.current_related_id,),
            )
            rows = self.cursor.fetchall()
        for row in rows:
            self.tree_orders.insert("", "end", values=row)

    def logout(self):
        # Clear session variables
        self.current_user = None
        self.current_role = None
        self.current_related_id = None

        # Destroy the current UI
        if hasattr(self, 'notebook'):
            self.notebook.destroy()

        # Hide main window and show login again
        self.root.withdraw()
        self.show_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()