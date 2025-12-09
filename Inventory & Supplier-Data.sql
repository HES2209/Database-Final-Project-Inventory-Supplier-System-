CREATE DATABASE Datatech;
USE Datatech;

SET AUTOCOMMIT=0;
INSERT INTO Supplier VALUES (1,'Supplier1','Aaron','Aaron999@gmail.com','087771182399', 'Jakarta Barat'),
(13,'Supplier2','Mugen','MM_000@yahoo.com','087278982399', 'Jakarta Selatan'),
(22,'Supplier3','Chris','AChris22@gmail.com','087770972399', 'Jakarta Utara'),
(7,'Supplier4','Simon','Simon_Alex@gmail.com','0877711276290', 'BSD'),
(12,'Supplier5','Audrey','AudreyM@gmail.com','0774981182309', 'Alam Sutera'),
(9,'Supplier6','Janice','JJanice777@gmail.com','050771184478', 'Jakarta Utara');
COMMIT;

SET AUTOCOMMIT=0;
INSERT INTO Customer VALUES ('CUST501', 'Alice', 'Johnson', 'alice_johnson@gmail.com', '089922010223', 'Jl. Meruya Ilir Raya No. 25, Srengseng, Kecamatan Kembangan, Jakarta Barat'),
('CUST502', 'Robert', 'Judaly', 'rodaly@yahoo.com', '087581928033', 'Komplek Taman Ratu Indah Blok B3 No. 7, Duri Kepa, Kecamatan Kebon Jeruk, Jakarta Barat'),
('CUST503', 'Mark', 'Revener', 'mark.reven@gmail.com', '085182730486', 'Jl. Bintaro Utama Sektor 3A, Pondok Ranji, Kecamatan Ciputat Timur, Tangerang Selatan'),
('CUST504', 'Lizzy', 'Amalka', 'Lizzyamalka@gmail.com', '082193489383', '	Jl. Permata Hijau Blok AA No. 12, Grogol Utara, Kecamatan Kebayoran Lama, Jakarta Selatan');
COMMIT;

SET AUTOCOMMIT=0;
INSERT INTO Category VALUES ('CAT01', 'Laptops and Computers', '1'),
('CAT02', 'Printers & Scanners', '13'),
('CAT03', 'Stationery', '22'),
('CAT04', 'Computer Components	', '7');
COMMIT;

SET AUTOCOMMIT=0;
INSERT INTO Product VALUES ('PROD101', 'CAT01', 'NovaBook Pro 15"', '16GB RAM, 512GB SSD, Silver', 'Rp20,799,000.00', 'In Stock'),
('PROD102', 'CAT01', 'Zenith Laptop 13"', '8GB RAM, 256GB SSD, Black', 'Rp14,999,000.00', 'In Stock'),
('PROD103', 'CAT01', 'UltraWide Monitor 34"', 'Curved QHD display for multitasking', 'Rp7,999,000.00', 'In Stock'),
('PROD201', 'CAT02', 'All-in-One Printer X5', 'Wireless color printer and scanner', 'Rp3,999,000.00', 'In Stock'),
('PROD301', 'CAT03', 'Premium Gel Pens (12-pack)', 'Assorted colors, smooth writing', 'Rp20,000.00', 'In Stock'),
('PROD401', 'CAT04', 'Gaming Mouse RGB', 'Programmable buttons, 16000 DPI', 'Rp150,000.00', 'In Stock');
COMMIT;

SET AUTOCOMMIT=0;
INSERT INTO Shelfloc VALUES ('A1', 'PROD101'),
('A2', 'PROD102'),
('A3', 'PROD103'),
('B1', 'PROD201'),
('C1', 'PROD301'),
('D1', 'PROD401');
COMMIT;

SET AUTOCOMMIT=0;
INSERT INTO CustomerOrderItem VALUES
('COI001', 'CUST501', 'PROD101', 'A1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
('COI002', 'CUST501', 'PROD301', 'C1', '2025-12-03', 'Credit Card', 'Arrived', '4 Days'),
('COI003', 'CUST502', 'PROD201', 'B1', '2025-12-02', 'Debit Card', 'On the way', '2 Days'),
('COI004', 'CUST503', 'PROD401', 'D1', '2025-12-01', 'Transfer', 'Delayed', '7 Days');
COMMIT;


SET AUTOCOMMIT=0;
INSERT INTO SupplierOrderItem VALUES
('SOI001', '1', 'PROD101', '2025-11-20', 'Arrived', '3 Days'),
('SOI002', '13', 'PROD201', '2025-11-25', 'On the way', '5 Days');
COMMIT;
