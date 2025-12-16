import mysql.connector
from db_config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("Connected to database successfully")
    
    # Add Quantity column
    try:
        cursor.execute("ALTER TABLE Shelfloc ADD COLUMN Quantity INT NOT NULL DEFAULT 1")
        print("✓ Quantity column added to Shelfloc table")
    except mysql.connector.Error as e:
        if "Duplicate column name" in str(e):
            print("✓ Quantity column already exists")
        else:
            print(f"Error: {e}")
    
    # Set existing records to quantity 1
    cursor.execute("UPDATE Shelfloc SET Quantity = 1 WHERE Quantity IS NULL OR Quantity = 0")
    print(f"✓ Updated shelf locations to have quantity")
    
    # Remove Status column (not needed anymore)
    try:
        cursor.execute("ALTER TABLE Shelfloc DROP COLUMN Status")
        print("✓ Removed Status column (not needed)")
    except mysql.connector.Error as e:
        if "check that it exists" in str(e):
            print("✓ Status column already removed")
        else:
            print(f"Note: {e}")
    
    connection.commit()
    print("\n✓ Migration completed - shelves now use quantity-based tracking!")
    
    cursor.execute("SELECT Shelfloc, ProductID, Quantity FROM Shelfloc LIMIT 5")
    print("\nSample shelf locations:")
    for row in cursor.fetchall():
        print(f"  {row}")
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
