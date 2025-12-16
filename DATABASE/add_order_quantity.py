import mysql.connector
from db_config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("Connected to database successfully")
    
    # Add Quantity column to CustomerOrderItem
    try:
        cursor.execute("ALTER TABLE CustomerOrderItem ADD COLUMN Quantity INT NOT NULL DEFAULT 1")
        print("✓ Quantity column added to CustomerOrderItem table")
    except mysql.connector.Error as e:
        if "Duplicate column name" in str(e):
            print("✓ Quantity column already exists")
        else:
            print(f"Error: {e}")
    
    # Set existing orders to quantity 1
    cursor.execute("UPDATE CustomerOrderItem SET Quantity = 1 WHERE Quantity IS NULL OR Quantity = 0")
    print("✓ Updated existing orders")
    
    connection.commit()
    print("\n✓ Migration completed!")
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
