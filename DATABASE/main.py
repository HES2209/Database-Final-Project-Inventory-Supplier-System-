import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG
from datetime import datetime
import re
import json
import os

class InventorySupplierSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory & Supplier System")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color scheme
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.bg_color = "#ecf0f1"
        self.success_color = "#27ae60"
        
        self.root.configure(bg=self.bg_color)
        
        # Database connection
        self.db_connection = None
        self.connect_database()
        
        # Current user data
        self.current_user = None
        self.current_user_type = None  # "customer" or "supplier"
        self.current_supplier_id = None
        self.current_customer_id = None
        
        # Show login screen
        self.show_login_screen()
    
    def connect_database(self):
        """Connect to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(**DB_CONFIG)
            if self.db_connection.is_connected():
                print("Connected to database successfully")
        except Error as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database:\n{str(e)}\n\nPlease check your database configuration in db_config.py")
            self.root.destroy()
    
    def execute_query(self, query, params=None):
        """Execute a database query"""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.db_connection.commit()
            return cursor
        except Error as e:
            messagebox.showerror("Database Error", f"Query error: {str(e)}")
            return None
    
    def fetch_query(self, query, params=None):
        """Fetch data from database"""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", f"Query error: {str(e)}")
            return None
    
    def fetch_one(self, query, params=None):
        """Fetch single row from database"""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Error as e:
            messagebox.showerror("Database Error", f"Query error: {str(e)}")
            return None
    
    def store_password(self, email, password, user_type):
        """Store password securely (for demo purposes, using JSON file)"""
        try:
            password_file = "passwords.json"
            
            # Load existing passwords
            if os.path.exists(password_file):
                with open(password_file, 'r') as f:
                    passwords = json.load(f)
            else:
                passwords = {}
            
            # Store new password
            if user_type not in passwords:
                passwords[user_type] = {}
            
            passwords[user_type][email] = password
            
            # Save to file
            with open(password_file, 'w') as f:
                json.dump(passwords, f, indent=4)
        except Exception as e:
            print(f"Error storing password: {str(e)}")
    
    def verify_password(self, email, password, user_type):
        """Verify password from storage"""
        try:
            password_file = "passwords.json"
            
            if not os.path.exists(password_file):
                return False
            
            with open(password_file, 'r') as f:
                passwords = json.load(f)
            
            if user_type in passwords and email in passwords[user_type]:
                return passwords[user_type][email] == password
            
            return False
        except Exception as e:
            print(f"Error verifying password: {str(e)}")
            return False
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, title):
        """Create a header for screens"""
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        label = tk.Label(header, text=title, font=("Arial", 24, "bold"), 
                        fg="white", bg=self.primary_color)
        label.pack(pady=10)
        
        return header
    
    def show_login_screen(self):
        """Display login screen"""
        self.clear_window()
        
        # Header
        self.create_header("Inventory & Supplier System")
        
        # Main container
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(container, text="Login", font=("Arial", 20, "bold"),
                        bg=self.bg_color, fg=self.primary_color)
        title.pack(pady=20)
        
        # User type selection
        user_type_frame = tk.Frame(container, bg=self.bg_color)
        user_type_frame.pack(pady=10)
        
        tk.Label(user_type_frame, text="Login as:", font=("Arial", 12),
                bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        
        self.login_user_type = tk.StringVar(value="customer")
        
        tk.Radiobutton(user_type_frame, text="Customer", variable=self.login_user_type,
                      value="customer", font=("Arial", 11), bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(user_type_frame, text="Supplier", variable=self.login_user_type,
                      value="supplier", font=("Arial", 11), bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        # Email field
        tk.Label(container, text="Email:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
        self.login_email = tk.Entry(container, font=("Arial", 11), width=40)
        self.login_email.pack(padx=50, pady=5)
        
        # Password field
        tk.Label(container, text="Password:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
        self.login_password = tk.Entry(container, font=("Arial", 11), width=40, show="*")
        self.login_password.pack(padx=50, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(container, bg=self.bg_color)
        button_frame.pack(pady=30)
        
        # Login button
        login_btn = tk.Button(button_frame, text="Login", font=("Arial", 12, "bold"),
                             bg=self.secondary_color, fg="white", width=15,
                             command=self.handle_login)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        # Register button
        register_btn = tk.Button(button_frame, text="Register", font=("Arial", 12, "bold"),
                                bg=self.accent_color, fg="white", width=15,
                                command=self.show_register_screen)
        register_btn.pack(side=tk.LEFT, padx=10)
    
    def handle_login(self):
        """Handle login logic"""
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()
        user_type = self.login_user_type.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return
        
        if user_type == "customer":
            customer = self.fetch_one(
                "SELECT * FROM Customer WHERE Email = %s",
                (email,)
            )
            if customer and self.verify_password(email, password, "customer"):
                self.current_user = email
                self.current_user_type = "customer"
                self.current_customer_id = customer['CustomerID']
                self.show_customer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or password")
        else:
            supplier = self.fetch_one(
                "SELECT * FROM Supplier WHERE Email = %s",
                (email,)
            )
            if supplier and self.verify_password(email, password, "supplier"):
                self.current_user = email
                self.current_user_type = "supplier"
                self.current_supplier_id = supplier['SupplierID']
                self.show_supplier_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or password")
    
    def show_register_screen(self):
        """Display registration screen"""
        self.clear_window()
        
        # Header
        self.create_header("Create Account")
        
        # Main container
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(container, text="Register", font=("Arial", 20, "bold"),
                        bg=self.bg_color, fg=self.primary_color)
        title.pack(pady=20)
        
        # User type selection
        user_type_frame = tk.Frame(container, bg=self.bg_color)
        user_type_frame.pack(pady=10)
        
        tk.Label(user_type_frame, text="Register as:", font=("Arial", 12),
                bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        
        self.register_user_type = tk.StringVar(value="customer")
        
        tk.Radiobutton(user_type_frame, text="Customer", variable=self.register_user_type,
                      value="customer", font=("Arial", 11), bg=self.bg_color,
                      command=self.update_register_fields).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(user_type_frame, text="Supplier", variable=self.register_user_type,
                      value="supplier", font=("Arial", 11), bg=self.bg_color,
                      command=self.update_register_fields).pack(side=tk.LEFT, padx=5)
        
        # Scrollable frame for form
        canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Store reference for field updating
        self.register_form_frame = scrollable_frame
        self.create_register_fields()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        # Register button
        register_btn = tk.Button(button_frame, text="Create Account", font=("Arial", 12, "bold"),
                                bg=self.secondary_color, fg="white", width=20,
                                command=self.handle_register)
        register_btn.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_btn = tk.Button(button_frame, text="Back to Login", font=("Arial", 12, "bold"),
                            bg=self.primary_color, fg="white", width=20,
                            command=self.show_login_screen)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def create_register_fields(self):
        """Create registration form fields based on user type"""
        # Clear previous fields
        for widget in self.register_form_frame.winfo_children():
            widget.destroy()
        
        user_type = self.register_user_type.get()
        
        # Common fields
        tk.Label(self.register_form_frame, text="Email:", font=("Arial", 11),
                bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
        self.reg_email = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
        self.reg_email.pack(padx=50, pady=5)
        
        tk.Label(self.register_form_frame, text="Password:", font=("Arial", 11),
                bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
        self.reg_password = tk.Entry(self.register_form_frame, font=("Arial", 11), 
                                    width=40, show="*")
        self.reg_password.pack(padx=50, pady=5)
        
        tk.Label(self.register_form_frame, text="Confirm Password:", font=("Arial", 11),
                bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
        self.reg_confirm_password = tk.Entry(self.register_form_frame, font=("Arial", 11),
                                            width=40, show="*")
        self.reg_confirm_password.pack(padx=50, pady=5)
        
        if user_type == "customer":
            tk.Label(self.register_form_frame, text="First Name:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_first_name = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_first_name.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Last Name:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_last_name = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_last_name.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Phone Number:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_phone = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_phone.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Address:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_address = tk.Text(self.register_form_frame, font=("Arial", 11), 
                                      width=40, height=3)
            self.reg_address.pack(padx=50, pady=5)
        
        else:  # Supplier
            tk.Label(self.register_form_frame, text="Supplier Name:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_supplier_name = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_supplier_name.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Contact Person:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_contact_person = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_contact_person.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Category to Supply:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            
            # Get all categories
            categories = self.fetch_query("SELECT * FROM Category")
            self.category_options = {cat['CategoryName']: cat['CategoryID'] for cat in categories} if categories else {}
            
            self.reg_category = ttk.Combobox(self.register_form_frame, 
                                            values=list(self.category_options.keys()),
                                            font=("Arial", 11), width=37, state="readonly")
            self.reg_category.pack(padx=50, pady=5)
            
            if self.category_options:
                self.reg_category.current(0)  # Select first category by default
            
            tk.Label(self.register_form_frame, text="Phone Number:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_phone = tk.Entry(self.register_form_frame, font=("Arial", 11), width=40)
            self.reg_phone.pack(padx=50, pady=5)
            
            tk.Label(self.register_form_frame, text="Address:", font=("Arial", 11),
                    bg=self.bg_color).pack(anchor="w", padx=50, pady=(20, 5))
            self.reg_address = tk.Text(self.register_form_frame, font=("Arial", 11),
                                      width=40, height=3)
            self.reg_address.pack(padx=50, pady=5)
    
    def update_register_fields(self):
        """Update form fields when user type changes"""
        self.create_register_fields()
    
    def handle_register(self):
        """Handle registration logic"""
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        confirm_password = self.reg_confirm_password.get().strip()
        user_type = self.register_user_type.get()
        
        # Validation
        if not email or not password:
            messagebox.showerror("Error", "Email and password are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if user_type == "customer":
            first_name = self.reg_first_name.get().strip()
            last_name = self.reg_last_name.get().strip()
            phone = self.reg_phone.get().strip()
            address = self.reg_address.get("1.0", tk.END).strip()
            
            if not first_name or not last_name or not phone or not address:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Check if email exists
            existing = self.fetch_one("SELECT * FROM Customer WHERE Email = %s", (email,))
            if existing:
                messagebox.showerror("Error", "Email already registered")
                return
            
            # Generate CustomerID
            customer_id = f"CUST{datetime.now().strftime('%d%m%H%M')}"
            
            try:
                query = """INSERT INTO Customer (CustomerID, FirstName, LastName, Email, PhoneNumber, Address)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                self.execute_query(query, (customer_id, first_name, last_name, email, phone, address))
                
                # Store password in a separate secure storage (for this demo, we'll create a simple password file)
                self.store_password(email, password, "customer")
                
                messagebox.showinfo("Success", "Customer account created successfully!")
                self.show_login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        else:  # Supplier
            supplier_name = self.reg_supplier_name.get().strip()
            contact_person = self.reg_contact_person.get().strip()
            phone = self.reg_phone.get().strip()
            address = self.reg_address.get("1.0", tk.END).strip()
            category_name = self.reg_category.get()
            
            if not supplier_name or not contact_person or not phone or not address or not category_name:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Check if email exists
            existing = self.fetch_one("SELECT * FROM Supplier WHERE Email = %s", (email,))
            if existing:
                messagebox.showerror("Error", "Email already registered")
                return
            
            # Generate SupplierID
            supplier_id = int(datetime.now().strftime('%d%H%M%S'))
            
            try:
                # Insert supplier
                query = """INSERT INTO Supplier (SupplierID, SupplierName, ContactPerson, Email, PhoneNumber, Address)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                self.execute_query(query, (supplier_id, supplier_name, contact_person, email, phone, address))
                
                # Store password
                self.store_password(email, password, "supplier")
                
                # Update category with supplier ID
                category_id = self.category_options.get(category_name)
                if category_id:
                    update_query = "UPDATE Category SET SupplierID = %s WHERE CategoryID = %s"
                    self.execute_query(update_query, (supplier_id, category_id))
                
                messagebox.showinfo("Success", "Supplier account created successfully!")
                self.show_login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_customer_dashboard(self):
        """Display customer dashboard"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="Customer Dashboard", font=("Arial", 20, "bold"),
                              fg="white", bg=self.primary_color)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        user_label = tk.Label(header, text=f"Welcome, {self.current_user}",
                             font=("Arial", 12), fg="white", bg=self.primary_color)
        user_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        logout_btn = tk.Button(header, text="Logout", font=("Arial", 11, "bold"),
                              bg=self.accent_color, fg="white",
                              command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main content
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get customer info
        customer_info = self.fetch_one(
            "SELECT * FROM Customer WHERE CustomerID = %s",
            (self.current_customer_id,)
        )
        
        # Info panel
        info_frame = tk.LabelFrame(container, text="Your Information", font=("Arial", 12, "bold"),
                                   bg=self.bg_color, padx=20, pady=20)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"""
Name: {customer_info.get('FirstName', '')} {customer_info.get('LastName', '')}
Email: {customer_info.get('Email', '')}
Phone: {customer_info.get('PhoneNumber', '')}
Address: {customer_info.get('Address', '')}
        """
        
        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 11),
                             bg=self.bg_color, justify=tk.LEFT)
        info_label.pack(anchor="w")
        
        # Features panel
        features_frame = tk.LabelFrame(container, text="Available Features", font=("Arial", 12, "bold"),
                                      bg=self.bg_color, padx=20, pady=20)
        features_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        features = [
            ("Browse & Order Products", self.browse_products),
            ("View My Orders", self.view_customer_orders),
            ("Logout", self.logout)
        ]
        
        for feature_name, command in features:
            btn = tk.Button(features_frame, text=feature_name, font=("Arial", 12),
                           bg=self.secondary_color, fg="white", width=30,
                           command=command)
            btn.pack(pady=10)
    
    def show_supplier_dashboard(self):
        """Display supplier dashboard"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="Supplier Dashboard", font=("Arial", 20, "bold"),
                              fg="white", bg=self.primary_color)
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        user_label = tk.Label(header, text=f"Welcome, {self.current_user}",
                             font=("Arial", 12), fg="white", bg=self.primary_color)
        user_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        logout_btn = tk.Button(header, text="Logout", font=("Arial", 11, "bold"),
                              bg=self.accent_color, fg="white",
                              command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main content
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get supplier info
        supplier_info = self.fetch_one(
            "SELECT * FROM Supplier WHERE SupplierID = %s",
            (self.current_supplier_id,)
        )
        
        # Get supplier's category
        category_info = self.fetch_one(
            "SELECT * FROM Category WHERE SupplierID = %s",
            (self.current_supplier_id,)
        )
        
        # Info panel
        info_frame = tk.LabelFrame(container, text="Your Information", font=("Arial", 12, "bold"),
                                   bg=self.bg_color, padx=20, pady=20)
        info_frame.pack(fill=tk.X, pady=10)
        
        category_text = f"Category: {category_info.get('CategoryName', 'Not assigned')}" if category_info else "Category: Not assigned"
        info_text = f"""
Supplier Name: {supplier_info.get('SupplierName', '')}
Contact Person: {supplier_info.get('ContactPerson', '')}
Email: {supplier_info.get('Email', '')}
Phone: {supplier_info.get('PhoneNumber', '')}
Address: {supplier_info.get('Address', '')}
{category_text}
        """
        
        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 11),
                             bg=self.bg_color, justify=tk.LEFT)
        info_label.pack(anchor="w")
        
        # Features panel
        features_frame = tk.LabelFrame(container, text="Available Features", font=("Arial", 12, "bold"),
                                      bg=self.bg_color, padx=20, pady=20)
        features_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        features = [
            ("Manage My Products", self.manage_supplier_products),
            ("Add New Product", self.add_new_product),
            ("View Incoming Orders", self.view_supplier_orders),
            ("Logout", self.logout)
        ]
        
        for feature_name, command in features:
            btn = tk.Button(features_frame, text=feature_name, font=("Arial", 12),
                           bg=self.secondary_color, fg="white", width=30,
                           command=command)
            btn.pack(pady=10)
    
    def browse_products(self):
        """Browse products screen"""
        self.clear_window()
        self.create_header("Browse & Order Products")
        
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get all categories
        categories = self.fetch_query("SELECT * FROM Category")
        
        if not categories:
            message = tk.Label(container, text="No products available",
                              font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
            message.pack(pady=50)
        else:
            # Create scrollable frame for products
            canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Display products by category
            for category in categories:
                products = self.fetch_query(
                    "SELECT * FROM Product WHERE CategoryID = %s",
                    (category['CategoryID'],)
                )
                
                if products:
                    cat_frame = tk.LabelFrame(scrollable_frame, text=category['CategoryName'],
                                             font=("Arial", 11, "bold"), bg=self.bg_color,
                                             padx=10, pady=10)
                    cat_frame.pack(fill=tk.X, pady=10, padx=5)
                    
                    for product in products:
                        self.create_product_card(cat_frame, product)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        back_btn = tk.Button(self.root, text="Back to Dashboard", font=("Arial", 11, "bold"),
                            bg=self.secondary_color, fg="white", width=20,
                            command=self.show_customer_dashboard)
        back_btn.pack(pady=10)
    
    def create_product_card(self, parent, product):
        """Create a product card with order option"""
        # Calculate stock from shelf quantities (SUM of all quantities)
        stock_count = self.fetch_one(
            "SELECT COALESCE(SUM(Quantity), 0) as count FROM Shelfloc WHERE ProductID = %s",
            (product['ProductID'],)
        )
        stock = stock_count['count'] if stock_count else 0
        availability = "In Stock" if stock > 0 else "Out of Stock"
        
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, pady=5)
        
        # Product info
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        name_label = tk.Label(info_frame, text=product['ProductName'], font=("Arial", 11, "bold"),
                             bg="white", justify=tk.LEFT)
        name_label.pack(anchor="w")
        
        desc_label = tk.Label(info_frame, text=product['Description'], font=("Arial", 9),
                             bg="white", fg="gray", justify=tk.LEFT)
        desc_label.pack(anchor="w")
        
        price_label = tk.Label(info_frame, text=f"Price: Rp {product['Price']:,.2f}", 
                              font=("Arial", 10, "bold"), bg="white", fg=self.success_color)
        price_label.pack(anchor="w", pady=5)
        
        stock_label = tk.Label(info_frame, text=f"Stock Available: {stock} unit(s)", 
                              font=("Arial", 10, "bold"), bg="white", fg=self.secondary_color)
        stock_label.pack(anchor="w")
        
        status_label = tk.Label(info_frame, text=f"Status: {availability}", 
                               font=("Arial", 9), bg="white",
                               fg=self.success_color if availability == 'In Stock' else self.accent_color)
        status_label.pack(anchor="w")
        
        # Order button
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        if availability == 'In Stock':
            order_btn = tk.Button(btn_frame, text="Order Now", font=("Arial", 10, "bold"),
                                 bg=self.secondary_color, fg="white", width=12,
                                 command=lambda p=product, s=stock: self.place_order(p, s))
            order_btn.pack()
        else:
            unavail_label = tk.Label(btn_frame, text="Out of Stock", font=("Arial", 10),
                                    bg=self.accent_color, fg="white")
            unavail_label.pack(padx=5, pady=5)
    
    def place_order(self, product, stock):
        """Place an order for a product"""
        order_window = tk.Toplevel(self.root)
        order_window.title("Place Order")
        order_window.geometry("400x350")
        order_window.configure(bg=self.bg_color)
        
        tk.Label(order_window, text=f"Order: {product['ProductName']}", font=("Arial", 12, "bold"),
                bg=self.bg_color).pack(pady=10)
        
        tk.Label(order_window, text=f"Available Stock: {stock} unit(s)", font=("Arial", 11),
                bg=self.bg_color, fg=self.secondary_color).pack(pady=5)
        
        # Quantity input
        tk.Label(order_window, text="Quantity:", font=("Arial", 11),
                bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        
        quantity_var = tk.StringVar(value="1")
        quantity_spinbox = tk.Spinbox(order_window, from_=1, to=stock, textvariable=quantity_var,
                                     font=("Arial", 11), width=10)
        quantity_spinbox.pack(padx=20, pady=5)
        
        tk.Label(order_window, text="Payment Method:", font=("Arial", 11),
                bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        
        payment_var = tk.StringVar(value="Credit Card")
        for method in ["Credit Card", "Debit Card", "Transfer"]:
            tk.Radiobutton(order_window, text=method, variable=payment_var, value=method,
                          font=("Arial", 10), bg=self.bg_color).pack(anchor="w", padx=40, pady=2)
        
        # Create order record
        def confirm_order():
            try:
                qty = int(quantity_var.get())
                if qty <= 0 or qty > stock:
                    messagebox.showerror("Error", f"Invalid quantity. Max: {stock}")
                    return
                
                payment = payment_var.get()
                order_id = f"COI{datetime.now().strftime('%d%m%H%M%S')}"
                
                # Get shelf locations for this product (ordered by quantity descending)
                shelves = self.fetch_query(
                    "SELECT Shelfloc, Quantity FROM Shelfloc WHERE ProductID = %s ORDER BY Quantity DESC",
                    (product['ProductID'],)
                )
                
                if not shelves:
                    messagebox.showerror("Error", "Not enough stock available")
                    return
                
                # Calculate if we have enough total stock
                total_available = sum(s['Quantity'] for s in shelves)
                if total_available < qty:
                    messagebox.showerror("Error", f"Not enough stock. Available: {total_available}")
                    return
                
                # Take from shelves until we have enough
                remaining_qty = qty
                shelves_used = []
                
                for shelf in shelves:
                    if remaining_qty <= 0:
                        break
                    
                    take_qty = min(shelf['Quantity'], remaining_qty)
                    shelves_used.append({
                        'Shelfloc': shelf['Shelfloc'],
                        'take': take_qty,
                        'original': shelf['Quantity']
                    })
                    remaining_qty -= take_qty
                
                # Use the first shelf for the order record
                first_shelf = shelves_used[0]['Shelfloc']
                
                # Create order
                query = """INSERT INTO CustomerOrderItem 
                          (CustomerOrderItemID, CustomerID, ProductID, Shelfloc, CustomerOrderDate, 
                           PaymentMethod, CustomerOrderItemStatus, EstimatedTime, Quantity)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                self.execute_query(query, (
                    order_id, self.current_customer_id, product['ProductID'],
                    first_shelf, datetime.now().date(), payment,
                    "Processing", "3-5 Days", qty
                ))
                
                # Update quantities in all used shelves
                for shelf_info in shelves_used:
                    new_quantity = shelf_info['original'] - shelf_info['take']
                    if new_quantity <= 0:
                        # Delete shelf if empty
                        delete_query = "DELETE FROM Shelfloc WHERE Shelfloc = %s"
                        self.execute_query(delete_query, (shelf_info['Shelfloc'],))
                    else:
                        # Update quantity
                        update_query = "UPDATE Shelfloc SET Quantity = %s WHERE Shelfloc = %s"
                        self.execute_query(update_query, (new_quantity, shelf_info['Shelfloc']))
                
                messagebox.showinfo("Success", f"Order placed successfully!\nOrder ID: {order_id}\nQuantity: {qty}")
                order_window.destroy()
                self.browse_products()
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to place order: {str(e)}")
        
        confirm_btn = tk.Button(order_window, text="Confirm Order", font=("Arial", 11, "bold"),
                               bg=self.success_color, fg="white", width=20, command=confirm_order)
        confirm_btn.pack(pady=20)
        
        cancel_btn = tk.Button(order_window, text="Cancel", font=("Arial", 11),
                              bg=self.primary_color, fg="white", width=20,
                              command=order_window.destroy)
        cancel_btn.pack(pady=5)
    
    def view_customer_orders(self):
        """View customer orders"""
        self.clear_window()
        self.create_header("My Orders")
        
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        orders = self.fetch_query(
            """SELECT c.*, p.ProductName
               FROM CustomerOrderItem c
               JOIN Product p ON c.ProductID = p.ProductID
               WHERE c.CustomerID = %s ORDER BY c.CustomerOrderDate DESC""",
            (self.current_customer_id,)
        )
        
        if not orders:
            message = tk.Label(container, text="You have no orders yet",
                              font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
            message.pack(pady=50)
        else:
            # Create scrollable table
            canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for order in orders:
                status_color = self.success_color if order['CustomerOrderItemStatus'] == 'Arrived' else \
                              self.accent_color if order['CustomerOrderItemStatus'] == 'Delayed' else \
                              self.secondary_color
                
                order_frame = tk.LabelFrame(scrollable_frame, text=f"Order {order['CustomerOrderItemID']}",
                                           font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
                order_frame.pack(fill=tk.X, pady=5)
                
                order_info = f"""
Product: {order['ProductName']}
Quantity: {order.get('Quantity', 1)} unit(s)
Date: {order['CustomerOrderDate']}
Payment: {order['PaymentMethod']}
Status: {order['CustomerOrderItemStatus']}
Estimated Time: {order['EstimatedTime']}
                """
                
                tk.Label(order_frame, text=order_info, font=("Arial", 10), bg="white", 
                        justify=tk.LEFT).pack(anchor="w")
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        back_btn = tk.Button(self.root, text="Back to Dashboard", font=("Arial", 11, "bold"),
                            bg=self.secondary_color, fg="white", width=20,
                            command=self.show_customer_dashboard)
        back_btn.pack(pady=10)
    
    def logout(self):
        """Handle logout"""
        self.current_user = None
        self.current_user_type = None
        self.current_supplier_id = None
        self.current_customer_id = None
        self.show_login_screen()
    
    def manage_supplier_products(self):
        """View and manage supplier's products"""
        self.clear_window()
        self.create_header("My Products")
        
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get supplier's category
        category = self.fetch_one(
            "SELECT * FROM Category WHERE SupplierID = %s",
            (self.current_supplier_id,)
        )
        
        if not category:
            message = tk.Label(container, text="You have not been assigned a category yet",
                              font=("Arial", 14), bg=self.bg_color, fg=self.accent_color)
            message.pack(pady=50)
        else:
            # Get products in this category
            products = self.fetch_query(
                "SELECT * FROM Product WHERE CategoryID = %s",
                (category['CategoryID'],)
            )
            
            if not products:
                message = tk.Label(container, text=f"No products in {category['CategoryName']} yet",
                                  font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
                message.pack(pady=50)
            else:
                # Create scrollable table
                canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                for product in products:
                    # Calculate total stock (SUM of quantities)
                    stock_count = self.fetch_one(
                        "SELECT COALESCE(SUM(Quantity), 0) as count FROM Shelfloc WHERE ProductID = %s",
                        (product['ProductID'],)
                    )
                    stock = stock_count['count'] if stock_count else 0
                    
                    # Get shelf locations
                    shelves = self.fetch_query(
                        "SELECT Shelfloc FROM Shelfloc WHERE ProductID = %s",
                        (product['ProductID'],)
                    )
                    shelf_list = ", ".join([s['Shelfloc'] for s in shelves]) if shelves else "No locations"
                    
                    prod_frame = tk.LabelFrame(scrollable_frame, text=product['ProductName'],
                                              font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
                    prod_frame.pack(fill=tk.X, pady=5)
                    
                    info = f"""
Description: {product['Description']}
Price: Rp {product['Price']:,.2f}
Total Stock: {stock} unit(s)
Shelf Locations: {shelf_list}
                    """
                    
                    tk.Label(prod_frame, text=info, font=("Arial", 9), bg="white",
                            justify=tk.LEFT).pack(anchor="w")
                    
                    action_frame = tk.Frame(prod_frame, bg="white")
                    action_frame.pack(fill=tk.X, pady=10)
                    
                    manage_stock_btn = tk.Button(action_frame, text="Manage Stock", font=("Arial", 9),
                                                bg=self.secondary_color, fg="white", width=15,
                                                command=lambda p=product: self.manage_product_stock(p))
                    manage_stock_btn.pack(side=tk.LEFT, padx=5)
                    
                    edit_btn = tk.Button(action_frame, text="Edit", font=("Arial", 9),
                                        bg=self.secondary_color, fg="white", width=10,
                                        command=lambda p=product: self.edit_product(p))
                    edit_btn.pack(side=tk.LEFT, padx=5)
                    
                    delete_btn = tk.Button(action_frame, text="Delete", font=("Arial", 9),
                                          bg=self.accent_color, fg="white", width=10,
                                          command=lambda p=product: self.delete_product(p))
                    delete_btn.pack(side=tk.LEFT, padx=5)
                
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        back_btn = tk.Button(self.root, text="Back to Dashboard", font=("Arial", 11, "bold"),
                            bg=self.secondary_color, fg="white", width=20,
                            command=self.show_supplier_dashboard)
        back_btn.pack(pady=10)
    
    def add_new_product(self):
        """Add new product variant"""
        # Get supplier's category
        category = self.fetch_one(
            "SELECT * FROM Category WHERE SupplierID = %s",
            (self.current_supplier_id,)
        )
        
        if not category:
            messagebox.showerror("Error", "You must be assigned a category first")
            return
        
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Product")
        add_window.geometry("500x550")
        add_window.configure(bg=self.bg_color)
        
        tk.Label(add_window, text=f"Add Product to {category['CategoryName']}", 
                font=("Arial", 12, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Product Name
        tk.Label(add_window, text="Product Name:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        product_name = tk.Entry(add_window, font=("Arial", 11), width=40)
        product_name.pack(padx=20, pady=5)
        
        # Description
        tk.Label(add_window, text="Description:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        description = tk.Text(add_window, font=("Arial", 11), width=40, height=3)
        description.pack(padx=20, pady=5)
        
        # Price
        tk.Label(add_window, text="Price (Rp):", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        price = tk.Entry(add_window, font=("Arial", 11), width=40)
        price.pack(padx=20, pady=5)
        
        # Initial Stock Quantity
        tk.Label(add_window, text="Initial Stock Quantity (units):", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        quantity = tk.Entry(add_window, font=("Arial", 11), width=40)
        quantity.pack(padx=20, pady=5)
        
        # Starting Shelf Location
        tk.Label(add_window, text="Shelf Location (e.g., A1, B5):", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        shelf_loc = tk.Entry(add_window, font=("Arial", 11), width=40)
        shelf_loc.pack(padx=20, pady=5)
        
        tk.Label(add_window, text="(All units will be stored at this location)", 
                font=("Arial", 9), bg=self.bg_color, fg="gray").pack(anchor="w", padx=20)
        
        def save_product():
            name = product_name.get().strip()
            desc = description.get("1.0", tk.END).strip()
            pr = price.get().strip()
            qty = quantity.get().strip()
            shelf_location = shelf_loc.get().strip().upper()
            
            if not all([name, desc, pr, qty, shelf_location]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                pr = float(pr)
                qty_int = int(qty)
                if qty_int <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
                    return
            except:
                messagebox.showerror("Error", "Please enter valid price and quantity")
                return
            
            # Check if shelf location is occupied
            existing = self.fetch_one(
                "SELECT Shelfloc, ProductID FROM Shelfloc WHERE Shelfloc = %s",
                (shelf_location,)
            )
            
            if existing:
                messagebox.showerror("Error", f"Shelf {shelf_location} is already occupied by another product!")
                return
            
            try:
                # Generate ProductID
                product_id = f"PROD{datetime.now().strftime('%d%m%H%M%S')}"
                
                # Insert product
                query = """INSERT INTO Product (ProductID, CategoryID, ProductName, Description, Price, Availability)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                self.execute_query(query, (product_id, category['CategoryID'], name, desc, pr, "In Stock"))
                
                # Create single shelf location with quantity
                shelf_query = "INSERT INTO Shelfloc (Shelfloc, ProductID, Quantity) VALUES (%s, %s, %s)"
                self.execute_query(shelf_query, (shelf_location, product_id, qty_int))
                
                messagebox.showinfo("Success", f"Product added successfully with {qty_int} unit(s) in stock!")
                add_window.destroy()
                self.manage_supplier_products()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
        save_btn = tk.Button(add_window, text="Save Product", font=("Arial", 11, "bold"),
                            bg=self.success_color, fg="white", width=20, command=save_product)
        save_btn.pack(pady=10)
        
        cancel_btn = tk.Button(add_window, text="Cancel", font=("Arial", 11),
                              bg=self.primary_color, fg="white", width=20,
                              command=add_window.destroy)
        cancel_btn.pack(pady=5)
    
    def manage_product_stock(self, product):
        """Manage stock for a product"""
        stock_window = tk.Toplevel(self.root)
        stock_window.title(f"Manage Stock: {product['ProductName']}")
        stock_window.geometry("500x400")
        stock_window.configure(bg=self.bg_color)
        
        # Get total stock (SUM of quantities)
        stock_count = self.fetch_one(
            "SELECT COALESCE(SUM(Quantity), 0) as count FROM Shelfloc WHERE ProductID = %s",
            (product['ProductID'],)
        )
        current_stock = stock_count['count'] if stock_count else 0
        
        tk.Label(stock_window, text=f"Manage Stock: {product['ProductName']}", 
                font=("Arial", 12, "bold"), bg=self.bg_color).pack(pady=10)
        
        tk.Label(stock_window, text=f"Total Stock: {current_stock} unit(s)", 
                font=("Arial", 11, "bold"), bg=self.bg_color, fg=self.secondary_color).pack(pady=10)
        
        # Get all shelf locations with quantities
        shelves = self.fetch_query(
            "SELECT Shelfloc, Quantity FROM Shelfloc WHERE ProductID = %s",
            (product['ProductID'],)
        )
        
        tk.Label(stock_window, text="Shelf Locations:", font=("Arial", 11, "bold"),
                bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Scrollable list of shelf locations
        canvas = tk.Canvas(stock_window, bg="white", height=150, highlightthickness=1)
        scrollbar = ttk.Scrollbar(stock_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if shelves:
            for shelf in shelves:
                shelf_label = tk.Label(scrollable_frame, text=f"  • {shelf['Shelfloc']} - {shelf['Quantity']} unit(s)", 
                                      font=("Arial", 10), bg="white", justify=tk.LEFT)
                shelf_label.pack(anchor="w")
        else:
            no_shelf_label = tk.Label(scrollable_frame, text="  No shelf locations assigned", 
                                     font=("Arial", 10), bg="white", fg="gray")
            no_shelf_label.pack(anchor="w")
        
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add stock
        tk.Label(stock_window, text="Add Stock Units:", font=("Arial", 11, "bold"),
                bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        
        add_qty_frame = tk.Frame(stock_window, bg=self.bg_color)
        add_qty_frame.pack(anchor="w", padx=20, pady=5)
        
        tk.Label(add_qty_frame, text="Quantity:", font=("Arial", 10),
                bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        add_qty = tk.Entry(add_qty_frame, font=("Arial", 10), width=10)
        add_qty.pack(side=tk.LEFT, padx=5)
        
        tk.Label(add_qty_frame, text="Shelf Location:", font=("Arial", 10),
                bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        add_shelf = tk.Entry(add_qty_frame, font=("Arial", 10), width=10)
        add_shelf.pack(side=tk.LEFT, padx=5)
        
        def add_stock():
            try:
                qty = int(add_qty.get())
                shelf_loc = add_shelf.get().strip().upper()
                
                if qty <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
                    return
                
                if not shelf_loc:
                    messagebox.showerror("Error", "Shelf location required")
                    return
                
                # Check if this shelf location exists
                existing = self.fetch_one(
                    "SELECT Shelfloc, ProductID, Quantity FROM Shelfloc WHERE Shelfloc = %s",
                    (shelf_loc,)
                )
                
                if existing:
                    # Check if it's for the same product
                    if existing['ProductID'] == product['ProductID']:
                        # Add to existing quantity
                        new_qty = existing['Quantity'] + qty
                        update_query = "UPDATE Shelfloc SET Quantity = %s WHERE Shelfloc = %s"
                        self.execute_query(update_query, (new_qty, shelf_loc))
                        messagebox.showinfo("Success", f"Added {qty} unit(s) to {shelf_loc}! Total: {new_qty}")
                    else:
                        # Different product occupies this shelf
                        messagebox.showerror("Error", f"Shelf {shelf_loc} is occupied by another product!")
                        return
                else:
                    # Create new shelf location
                    insert_query = "INSERT INTO Shelfloc (Shelfloc, ProductID, Quantity) VALUES (%s, %s, %s)"
                    self.execute_query(insert_query, (shelf_loc, product['ProductID'], qty))
                    messagebox.showinfo("Success", f"Created {shelf_loc} with {qty} unit(s)!")
                
                stock_window.destroy()
                self.manage_supplier_products()
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add stock: {str(e)}")
        
        add_btn = tk.Button(add_qty_frame, text="Add Stock", font=("Arial", 10, "bold"),
                           bg=self.success_color, fg="white", command=add_stock)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(stock_window, text="Close", font=("Arial", 11),
                             bg=self.primary_color, fg="white", width=20,
                             command=stock_window.destroy)
        close_btn.pack(pady=20)
    
    def edit_product(self, product):
        """Edit a product"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Product")
        edit_window.geometry("500x500")
        edit_window.configure(bg=self.bg_color)
        
        tk.Label(edit_window, text=f"Edit Product: {product['ProductName']}", 
                font=("Arial", 12, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Product Name
        tk.Label(edit_window, text="Product Name:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        product_name = tk.Entry(edit_window, font=("Arial", 11), width=40)
        product_name.insert(0, product['ProductName'])
        product_name.pack(padx=20, pady=5)
        
        # Description
        tk.Label(edit_window, text="Description:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        description = tk.Text(edit_window, font=("Arial", 11), width=40, height=3)
        description.insert("1.0", product['Description'])
        description.pack(padx=20, pady=5)
        
        # Price
        tk.Label(edit_window, text="Price (Rp):", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        price = tk.Entry(edit_window, font=("Arial", 11), width=40)
        price.insert(0, str(product['Price']))
        price.pack(padx=20, pady=5)
        
        # Availability
        tk.Label(edit_window, text="Availability:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        availability_var = tk.StringVar(value=product['Availability'])
        tk.Radiobutton(edit_window, text="In Stock", variable=availability_var, value="In Stock",
                      font=("Arial", 10), bg=self.bg_color).pack(anchor="w", padx=40)
        tk.Radiobutton(edit_window, text="Out of Stock", variable=availability_var, value="Out of Stock",
                      font=("Arial", 10), bg=self.bg_color).pack(anchor="w", padx=40)
        
        def update_product():
            name = product_name.get().strip()
            desc = description.get("1.0", tk.END).strip()
            pr = price.get().strip()
            avail = availability_var.get()
            
            if not all([name, desc, pr]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                pr = float(pr)
            except:
                messagebox.showerror("Error", "Please enter a valid price")
                return
            
            try:
                query = """UPDATE Product SET ProductName = %s, Description = %s, Price = %s, Availability = %s
                          WHERE ProductID = %s"""
                self.execute_query(query, (name, desc, pr, avail, product['ProductID']))
                messagebox.showinfo("Success", "Product updated successfully!")
                edit_window.destroy()
                self.manage_supplier_products()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product: {str(e)}")
        
        save_btn = tk.Button(edit_window, text="Update Product", font=("Arial", 11, "bold"),
                            bg=self.success_color, fg="white", width=20, command=update_product)
        save_btn.pack(pady=10)
        
        cancel_btn = tk.Button(edit_window, text="Cancel", font=("Arial", 11),
                              bg=self.primary_color, fg="white", width=20,
                              command=edit_window.destroy)
        cancel_btn.pack(pady=5)
    
    def edit_product(self, product):
        """Edit a product"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Product")
        edit_window.geometry("500x500")
        edit_window.configure(bg=self.bg_color)
        
        tk.Label(edit_window, text=f"Edit Product: {product['ProductName']}", 
                font=("Arial", 12, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Product Name
        tk.Label(edit_window, text="Product Name:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        product_name = tk.Entry(edit_window, font=("Arial", 11), width=40)
        product_name.insert(0, product['ProductName'])
        product_name.pack(padx=20, pady=5)
        
        # Description
        tk.Label(edit_window, text="Description:", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        description = tk.Text(edit_window, font=("Arial", 11), width=40, height=3)
        description.insert("1.0", product['Description'])
        description.pack(padx=20, pady=5)
        
        # Price
        tk.Label(edit_window, text="Price (Rp):", font=("Arial", 11), bg=self.bg_color).pack(anchor="w", padx=20, pady=(20, 5))
        price = tk.Entry(edit_window, font=("Arial", 11), width=40)
        price.insert(0, str(product['Price']))
        price.pack(padx=20, pady=5)
    
    def delete_product(self, product):
        """Delete a product"""
        if messagebox.askyesno("Confirm Delete", f"Delete {product['ProductName']}?"):
            try:
                # Delete from Shelfloc first
                self.execute_query(
                    "DELETE FROM Shelfloc WHERE ProductID = %s",
                    (product['ProductID'],)
                )
                
                # Delete from CustomerOrderItem
                self.execute_query(
                    "DELETE FROM CustomerOrderItem WHERE ProductID = %s",
                    (product['ProductID'],)
                )
                
                # Delete from SupplierOrderItem
                self.execute_query(
                    "DELETE FROM SupplierOrderItem WHERE ProductID = %s",
                    (product['ProductID'],)
                )
                
                # Delete product
                self.execute_query(
                    "DELETE FROM Product WHERE ProductID = %s",
                    (product['ProductID'],)
                )
                
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.manage_supplier_products()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
    
    def view_supplier_orders(self):
        """View orders for supplier"""
        self.clear_window()
        self.create_header("Incoming Orders")
        
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get supplier's products
        products = self.fetch_query(
            """SELECT p.ProductID FROM Product p
               JOIN Category c ON p.CategoryID = c.CategoryID
               WHERE c.SupplierID = %s""",
            (self.current_supplier_id,)
        )
        
        if not products:
            message = tk.Label(container, text="No orders for your products yet",
                              font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
            message.pack(pady=50)
        else:
            product_ids = tuple([p['ProductID'] for p in products])
            
            # Get orders for supplier's products
            orders = self.fetch_query(
                f"""SELECT c.*, p.ProductName, cust.FirstName, cust.LastName, cust.Email
                   FROM CustomerOrderItem c
                   JOIN Product p ON c.ProductID = p.ProductID
                   JOIN Customer cust ON c.CustomerID = cust.CustomerID
                   WHERE c.ProductID IN ({','.join(['%s']*len(product_ids))})
                   ORDER BY c.CustomerOrderDate DESC""",
                product_ids
            )
            
            if not orders:
                message = tk.Label(container, text="No orders yet",
                                  font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
                message.pack(pady=50)
            else:
                # Create scrollable table
                canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                for order in orders:
                    status_color = self.success_color if order['CustomerOrderItemStatus'] == 'Arrived' else \
                                  self.accent_color if order['CustomerOrderItemStatus'] == 'Delayed' else \
                                  self.secondary_color
                    
                    order_frame = tk.LabelFrame(scrollable_frame, text=f"Order {order['CustomerOrderItemID']}",
                                               font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
                    order_frame.pack(fill=tk.X, pady=5)
                    
                    order_info = f"""
Product: {order['ProductName']}
Customer: {order['FirstName']} {order['LastName']} ({order['Email']})
Date: {order['CustomerOrderDate']}
Payment: {order['PaymentMethod']}
Status: {order['CustomerOrderItemStatus']}
Estimated Time: {order['EstimatedTime']}
                    """
                    
                    tk.Label(order_frame, text=order_info, font=("Arial", 9), bg="white",
                            justify=tk.LEFT).pack(anchor="w")
                
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        back_btn = tk.Button(self.root, text="Back to Dashboard", font=("Arial", 11, "bold"),
                            bg=self.secondary_color, fg="white", width=20,
                            command=self.show_supplier_dashboard)
        back_btn.pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySupplierSystem(root)
    root.mainloop()
