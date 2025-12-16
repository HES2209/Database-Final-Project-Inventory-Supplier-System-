import mysql.connector
from db_config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("Connected to database successfully")
    
    # Drop the foreign key constraint from CustomerOrderItem
    try:
        # First, find the constraint name
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'CustomerOrderItem' 
            AND COLUMN_NAME = 'Shelfloc' 
            AND TABLE_SCHEMA = 'datatech'
        """)
        result = cursor.fetchone()
        
        if result:
            constraint_name = result[0]
            cursor.execute(f"ALTER TABLE CustomerOrderItem DROP FOREIGN KEY {constraint_name}")
            print(f"✓ Removed foreign key constraint: {constraint_name}")
        else:
            print("✓ No foreign key constraint found (already removed)")
    except mysql.connector.Error as e:
        print(f"Note: {e}")
    
    connection.commit()
    print("✓ Migration completed - shelf locations can now be deleted after sale")
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
