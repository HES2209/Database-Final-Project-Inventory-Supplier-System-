-- This script creates the database schema for your Inventory & Supplier System.
-- It is designed to be in 3NF (Third Normal Form) to reduce redundancy
-- and improve data integrity.

-- We drop tables in reverse order of creation to avoid foreign key errors.
DROP TABLE IF EXISTS SupplierOrderDetail;
DROP TABLE IF EXISTS SupplierOrder;
DROP TABLE IF EXISTS CustomerOrderDetail;
DROP TABLE IF EXISTS CustomerOrder;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Supplier;


-- 1. Supplier Table
-- Stores information about your suppliers.
CREATE TABLE Supplier (
    SupplierID VARCHAR(10) PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    ContactPerson VARCHAR(100),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Address VARCHAR(255)
);

-- 2. Customer Table
-- Stores information about your customers.
CREATE TABLE Customer (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Address VARCHAR(255)
);

-- 3. Category Table
-- Stores product categories (e.g., "Laptops", "Stationery").
-- We removed SupplierID from here to make the design more flexible.
CREATE TABLE Category (
    CategoryID VARCHAR(10) PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL,
    Description TEXT
);

-- 4. Product Table
-- Stores all your products.
-- We added SupplierID here to link each product to its main supplier.
-- We removed 'Availability' because it should be calculated from Inventory.Stock.
CREATE TABLE Product (
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(150) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL, -- The current selling price
    CategoryID VARCHAR(10),
    SupplierID VARCHAR(10),
    
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- 5. Inventory Table
-- Tracks the stock level and location for each product.
-- This is a 1-to-1 relationship with Product.
CREATE TABLE Inventory (
    InventoryID VARCHAR(10) PRIMARY KEY,
    ProductID VARCHAR(10) NOT NULL UNIQUE, -- 'UNIQUE' ensures one inventory record per product
    Stock INT NOT NULL DEFAULT 0,
    ReorderLevel INT,
    Location VARCHAR(100), -- e.g., "Warehouse A, Section 1"
    
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- 6. CustomerOrder Table (The "Order Header")
-- Stores one record for each *entire order* placed by a customer.
CREATE TABLE CustomerOrder (
    CustomerOrderID VARCHAR(10) PRIMARY KEY,
    CustomerID VARCHAR(10),
    OrderDate DATETIME NOT NULL,
    PaymentMethod VARCHAR(50),
    OrderStatus VARCHAR(50), -- e.g., "Pending", "Shipped", "Delivered"
    EstimatedDeliveryDate DATE,
    
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- 7. CustomerOrderDetail Table (The "Order Lines")
-- Stores the *specific items* that are part of a CustomerOrder.
CREATE TABLE CustomerOrderDetail (
    CustomerOrderDetailID VARCHAR(10) PRIMARY KEY,
    CustomerOrderID VARCHAR(10) NOT NULL,
    ProductID VARCHAR(10),
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL, -- The price of the product at the time of sale
    
    FOREIGN KEY (CustomerOrderID) REFERENCES CustomerOrder(CustomerOrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- 8. SupplierOrder Table (The "Purchase Order Header")
-- Stores one record for each *entire order* you place with a supplier.
CREATE TABLE SupplierOrder (
    SupplierOrderID VARCHAR(10) PRIMARY KEY,
    SupplierID VARCHAR(10),
    OrderDate DATETIME NOT NULL,
    OrderStatus VARCHAR(50), -- e.g., "Ordered", "Shipped", "Received"
    EstimatedArrivalDate DATE,
    
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- 9. SupplierOrderDetail Table (The "Purchase Order Lines")
-- Stores the *specific items* you are ordering from a supplier.
CREATE TABLE SupplierOrderDetail (
    SupplierOrderDetailID VARCHAR(10) PRIMARY KEY,
    SupplierOrderID VARCHAR(10) NOT NULL,
    ProductID VARCHAR(10),
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL, -- The *cost* of the product from the supplier
    
    FOREIGN KEY (SupplierOrderID) REFERENCES SupplierOrder(SupplierOrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- --- End of Schema ---