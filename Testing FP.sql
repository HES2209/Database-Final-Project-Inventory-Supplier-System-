-- Setting up the schema based on your 3NF structure.

-- 1. SUPPLIER Table
-- Stores information about the product suppliers.
CREATE TABLE Supplier (
    SupplierID      VARCHAR(100) PRIMARY KEY,
    SupplierName    VARCHAR(255) NOT NULL,
    ContactPerson   VARCHAR(255),
    Email           VARCHAR(255) UNIQUE,
    PhoneNumber     VARCHAR(100),
    Address         VARCHAR(255)
);

-- 2. CUSTOMER Table
-- Stores information about the customers.
CREATE TABLE Customer (
    CustomerID      VARCHAR(100) PRIMARY KEY,
    FirstName       VARCHAR(100) NOT NULL,
    LastName        VARCHAR(100),
    Email           VARCHAR(255) UNIQUE,
    PhoneNumber     VARCHAR(100),
    Address         VARCHAR(255)
);

-- 3. CATEGORY Table
-- Stores product categories, linking to the main supplier for that category.
CREATE TABLE Category (
    CategoryID      VARCHAR(100) PRIMARY KEY,
    CategoryName    VARCHAR(255) NOT NULL UNIQUE,
    SupplierID      VARCHAR(100),
    -- FK: Links a category to the main supplier that stocks it.
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- 4. PRODUCT Table
-- Stores the core product details, linking to a Category.
CREATE TABLE Product (
    ProductID       VARCHAR(100) PRIMARY KEY,
    CategoryID      VARCHAR(100) NOT NULL,
    ProductName     VARCHAR(255) NOT NULL,
    Description     TEXT,
    Price           DECIMAL(10, 2) NOT NULL, -- Assuming price needs two decimal places
    Availability    VARCHAR(50), -- e.g., 'Available', 'Out of Stock'
    -- FK: Links a product to its category.
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

-- 5. SHELFLOC Table (Inventory/Warehouse Location)
-- Stores physical inventory locations and the product type stored there.
CREATE TABLE Shelfloc (
    Shelfloc        VARCHAR(100) PRIMARY KEY, -- Unique ID for the shelf location (e.g., A1, B2)
    ProductID       VARCHAR(100) NOT NULL,
    -- FK: Specifies which product is stored in this location.
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- 6. CUSTOMER_ORDER_ITEM Table (Sales Transactions)
-- This is a line-item in a customer's order.
CREATE TABLE CustomerOrderItem (
    CustomerOrderItemID VARCHAR(100) PRIMARY KEY,
    CustomerID          VARCHAR(100) NOT NULL,
    ProductID           VARCHAR(100) NOT NULL,
    Shelfloc            VARCHAR(100) NOT NULL, -- The specific shelf location the item was taken from
    CustomerOrderDate   DATE NOT NULL,
    PaymentMethod       VARCHAR(50),
    CustomerOrderItemStatus VARCHAR(50), -- e.g., 'Arrived', 'On the way', 'Delayed'
    EstimatedTime       VARCHAR(100), -- Free text or calculated time
    -- FKs: Linking the item to the Customer, Product, and specific Shelf Location.
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (Shelfloc) REFERENCES Shelfloc(Shelfloc)
);

-- 7. SUPPLIER_ORDER_ITEM Table (Purchasing/Procurement)
-- This is a line-item in a purchase order sent to a supplier.
CREATE TABLE SupplierOrderItem (
    SupplierOrderItemID VARCHAR(100) PRIMARY KEY,
    SupplierID          VARCHAR(100) NOT NULL,
    ProductID           VARCHAR(100) NOT NULL,
    SupplierOrderDate   DATE NOT NULL,
    SupplierOrderItemStatus VARCHAR(50), -- e.g., 'Arrived', 'On the way', 'Delayed'
    EstimatedTime       VARCHAR(100),
    -- FKs: Linking the item to the Supplier and the Product being purchased.
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);