# Inventory & Supplier System

A comprehensive Python Tkinter application for managing an inventory and supplier system with MySQL database integration. This is a final project for Database Technology course.

## Features

### For Customers
- **User Registration & Login** - Create account and login with email verification
- **Browse Products** - View all products organized by category and supplier
- **Place Orders** - Order products with payment method selection (Credit Card, Debit Card, Transfer)
- **Order History** - View all past orders with status tracking
- **Dashboard** - Personal dashboard showing account information and quick access to features

### For Suppliers
- **User Registration & Login** - Create supplier account and login
- **Product Management** - Add, edit, and delete products in their assigned category
- **Add Product Variants** - Suppliers can add multiple variants of products to their category
- **Product Inventory** - Manage product details: name, description, price, availability, shelf location
- **Order Tracking** - View incoming customer orders for their products
- **Dashboard** - Supplier dashboard with company information and category assignment

## System Architecture

### Database Schema

The system uses the following tables:

- **Supplier** - Stores supplier information
- **Customer** - Stores customer information
- **Category** - Product categories (each supplier supplies ONE category)
- **Product** - Products with details (quantity, description, price, availability)
- **Shelfloc** - Physical inventory locations for products
- **CustomerOrderItem** - Customer purchase orders
- **SupplierOrderItem** - Supplier purchase/restock orders

**Key Relationship:** 
- Each supplier supplies exactly ONE category
- Each category can contain MANY products
- Suppliers can add multiple product variants to their category

## Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server installed and running
- pip (Python package manager)

### Step 1: Set up the Database

1. Open MySQL and run the SQL scripts provided:
   - `Inventory-and-Supplier-System.sql` - Creates tables and initial structure
   - `Inventory & Supplier-Data.sql` - Populates sample data

```sql
mysql -u root -p < "Inventory-and-Supplier-System.sql"
mysql -u root -p < "Inventory & Supplier-Data.sql"
```

Or use MySQL Workbench to execute the scripts.

### Step 2: Configure Database Connection

Edit `db_config.py` with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change if you have a password
    'database': 'datatech',
    'raise_on_warnings': True,
    'autocommit': True
}
```

### Step 3: Install Required Packages

```bash
pip install mysql-connector-python
```

Tkinter comes built-in with Python, so no additional installation needed for GUI.

### Step 4: Run the Application

```bash
python main.py
```

The application window will open. You can now login or register as a customer or supplier.

## How to Use

### As a Customer

1. **Register**: Click "Register" and select "Customer"
   - Enter email, first name, last name, phone number, and address
   - Account will be created in the database

2. **Login**: Use your registered email to login

3. **Browse Products**: View all available products by category
   - Click "Browse & Order Products" on dashboard
   - Browse products by category

4. **Place Order**:
   - Click "Order Now" on any product
   - Select payment method
   - Click "Confirm Order"
   - Order is recorded with "Processing" status

5. **View Orders**:
   - Click "View My Orders" to see all your orders
   - Check order status: Processing, On the way, Arrived, or Delayed

### As a Supplier

1. **Register**: Click "Register" and select "Supplier"
   - Enter email, supplier name, contact person, phone number, and address
   - Account will be created

2. **Login**: Use your registered email to login

3. **Add Products**:
   - Click "Add New Product"
   - Fill in product details:
     - Product name
     - Description (specs/features)
     - Price in Rp
     - Availability (In Stock / Out of Stock)
     - Shelf location (e.g., A1, B2, etc.)
   - Click "Save Product"

4. **Manage Products**:
   - Click "Manage My Products"
   - View all your products in your assigned category
   - Click "Edit" to update product details
   - Click "Delete" to remove a product

5. **View Incoming Orders**:
   - Click "View Incoming Orders"
   - See all customer orders for your products
   - View customer information and order status

## Sample Test Data

### Pre-registered Suppliers
- Email: Aaron999@gmail.com (Laptops and Computers)
- Email: MM_000@yahoo.com (Printers & Scanners)
- Email: AChris22@gmail.com (Stationery)
- Email: Simon_Alex@gmail.com (Computer Components)

### Pre-registered Customers
- Email: alice_johnson@gmail.com (Alice Johnson)
- Email: rodaly@yahoo.com (Robert Judaly)
- Email: mark.reven@gmail.com (Mark Revener)
- Email: Lizzyamalka@gmail.com (Lizzy Amalka)

## File Structure

```
Final Projects/
├── main.py                              # Main application file
├── db_config.py                         # Database configuration
├── README.md                            # This file
├── Inventory-and-Supplier-System.sql    # Database schema
├── Inventory & Supplier-Data.sql        # Sample data
└── customers.json / suppliers.json      # Auto-generated (if using file storage)
```

## Database Connection Notes

- The application connects to MySQL database named `datatech`
- Ensure MySQL server is running before starting the application
- If database connection fails, check `db_config.py` credentials
- Default MySQL user is usually `root` with no password on local machines

## Features Implementation Details

### Login System
- Email-based login (no password check in current implementation)
- Separate login pages for customers and suppliers
- Auto-detection of user type and loading correct dashboard

### Product Management
- Products are linked to categories via CategoryID
- Suppliers can only manage products in their assigned category
- Each product has a shelf location for inventory tracking

### Order System
- Customers can place orders with different payment methods
- Orders are automatically linked to shelf locations
- Order status tracking: Processing → On the way → Arrived/Delayed

### Data Validation
- Email format validation during registration
- Required field validation
- Price validation (numeric)
- Duplicate email checking

## Future Enhancements

- Password hashing for security
- Order status update functionality
- Inventory quantity management
- Advanced product search and filtering
- Admin dashboard for system management
- Email notifications for orders
- Payment processing integration
- User profile editing
- Order cancellation functionality

## Troubleshooting

### "Failed to connect to database" error
- Check MySQL server is running
- Verify credentials in `db_config.py`
- Ensure database `datatech` exists and tables are created

### "No products available" message
- Run the data population SQL script
- Check products exist in the database

### Application window not opening
- Verify Python version is 3.7+
- Check Tkinter is installed (usually comes with Python)

## Support

For issues or questions, check:
1. Database configuration in `db_config.py`
2. MySQL server status
3. Database schema is properly created
4. Sample data is loaded
