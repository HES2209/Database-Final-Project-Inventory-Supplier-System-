USE datatech;

CREATE TABLE Supplier (
    SupplierID      VARCHAR(100) PRIMARY KEY,
    SupplierName    VARCHAR(255) NOT NULL,
    ContactPerson   VARCHAR(255),
    Email           VARCHAR(255) UNIQUE,
    PhoneNumber     VARCHAR(100),
    Address         VARCHAR(255)
);

INSERT INTO Supplier VALUES (1,'Supplier1','Aaron','Aaron999@gmail.com','087771182399', 'Jakarta Barat'),
(13,'Supplier2','Mugen','MM_000@yahoo.com','087278982399', 'Jakarta Selatan'),
(22,'Supplier3','Chris','AChris22@gmail.com','087770972399', 'Jakarta Utara'),
(7,'Supplier4','Simon','Simon_Alex@gmail.com','0877711276290', 'BSD'),
(12,'Supplier5','Audrey','AudreyM@gmail.com','0774981182309', 'Alam Sutera'),
(9,'Supplier6','Janice','JJanice777@gmail.com','050771184478', 'Jakarta Utara');

SELECT *
FROM Supplier;

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

INSERT INTO Customer VALUES ('CUST501', 'Alice', 'Johnson', 'alice_johnson@gmail.com', '089922010223', 'Jl. Meruya Ilir Raya No. 25, Srengseng, Kecamatan Kembangan, Jakarta Barat'),
('CUST502', 'Robert', 'Judaly', 'rodaly@yahoo.com', '087581928033', 'Komplek Taman Ratu Indah Blok B3 No. 7, Duri Kepa, Kecamatan Kebon Jeruk, Jakarta Barat'),
('CUST503', 'Mark', 'Revener', 'mark.reven@gmail.com', '085182730486', 'Jl. Bintaro Utama Sektor 3A, Pondok Ranji, Kecamatan Ciputat Timur, Tangerang Selatan'),
('CUST504', 'Lizzy', 'Amalka', 'Lizzyamalka@gmail.com', '082193489383', '	Jl. Permata Hijau Blok AA No. 12, Grogol Utara, Kecamatan Kebayoran Lama, Jakarta Selatan');

SELECT *
FROM Customer;


-- 3. CATEGORY Table
-- Stores product categories, linking to the main supplier for that category.
CREATE TABLE Category (
    CategoryID      VARCHAR(100) PRIMARY KEY,
    CategoryName    VARCHAR(255) NOT NULL UNIQUE,
    SupplierID      VARCHAR(100),
    -- FK: Links a category to the main supplier that stocks it.
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

INSERT INTO Category VALUES ('CAT01', 'Laptops and Computers', '1'),
('CAT02', 'Printers & Scanners', '13'),
('CAT03', 'Stationery', '22'),
('CAT04', 'Computer Components	', '7');

SELECT *
FROM Category;

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

INSERT INTO Product VALUES ('PROD101', 'CAT01', 'NovaBook Pro 15"', '16GB RAM, 512GB SSD, Silver', 20799000.00, 'In Stock'),
('PROD102', 'CAT01', 'Zenith Laptop 13"', '8GB RAM, 256GB SSD, Black', 14999000.00, 'In Stock'),
('PROD103', 'CAT01', 'UltraWide Monitor 34"', 'Curved QHD display for multitasking', 7999000.00, 'In Stock'),
('PROD201', 'CAT02', 'All-in-One Printer X5', 'Wireless color printer and scanner', 3999000.00, 'In Stock'),
('PROD301', 'CAT03', 'Premium Gel Pens (12-pack)', 'Assorted colors, smooth writing', 20000.00, 'In Stock'),
('PROD401', 'CAT04', 'Gaming Mouse RGB', 'Programmable buttons, 16000 DPI', 150000.00, 'In Stock');

SELECT *
FROM Product;

-- 5. SHELFLOC Table (Inventory/Warehouse Location)
-- Stores physical inventory locations and the product type stored there.
CREATE TABLE Shelfloc (
    Shelfloc        VARCHAR(100) PRIMARY KEY, -- Unique ID for the shelf location (e.g., A1, B2)
    ProductID       VARCHAR(100) NOT NULL,
    -- FK: Specifies which product is stored in this location.
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

INSERT INTO Shelfloc VALUES ('A1', 'PROD101'),
('A2', 'PROD102'),
('A3', 'PROD103'),
('B1', 'PROD201'),
('C1', 'PROD301'),
('D1', 'PROD401');

SELECT *
FROM Shelfloc;

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

INSERT INTO CustomerOrderItem VALUES
('COI001', 'CUST501', 'PROD101', 'A1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
('COI002', 'CUST501', 'PROD301', 'C1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
('COI003', 'CUST502', 'PROD201', 'B1', '2025-12-02', 'Debit Card', 'On the way', '2 Days'),
('COI004', 'CUST503', 'PROD401', 'D1', '2025-12-01', 'Transfer', 'Delayed', '7 Days');

SELECT *
FROM CustomerOrderItem;

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

INSERT INTO SupplierOrderItem VALUES
('SOI001', '1', 'PROD101', '2025-11-20', 'Arrived', '3 Days'),
('SOI002', '13', 'PROD201', '2025-11-25', 'On the way', '5 Days');

SELECT*
FROM SupplierOrderItem;