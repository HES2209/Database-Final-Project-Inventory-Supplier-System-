import mysql.connector
from db_config import DB_CONFIG

try:
    # Connect to database
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("Connected to database successfully")
    
    # Add Status column
    try:
        cursor.execute("ALTER TABLE Shelfloc ADD COLUMN Status VARCHAR(50) DEFAULT 'Available'")
        print("✓ Status column added to Shelfloc table")
    except mysql.connector.Error as e:
        if "Duplicate column name" in str(e):
            print("✓ Status column already exists")
        else:
            print(f"Error adding column: {e}")
    
    # Update existing records to have Available status
    cursor.execute("UPDATE Shelfloc SET Status = 'Available' WHERE Status IS NULL")
    print(f"✓ Updated {cursor.rowcount} shelf locations to 'Available' status")
    
    # Show results
    cursor.execute("SELECT Shelfloc, ProductID, Status FROM Shelfloc LIMIT 5")
    print("\nSample shelf locations:")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    connection.commit()
    print("\n✓ Migration completed successfully!")
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed")
