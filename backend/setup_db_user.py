import mysql.connector
import os

try:
    # Connect as root first to create new user
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="" 
    )
    cursor = conn.cursor()

    # Configuration
    new_user = "firevision_user"
    new_pass = "FireVisionSecurePass2025!"
    database = "firevision"

    # Create User if not exists
    try:
        cursor.execute(f"CREATE USER IF NOT EXISTS '{new_user}'@'localhost' IDENTIFIED BY '{new_pass}';")
        print(f"✅ User '{new_user}' ensured.")
    except Exception as e:
        print(f"⚠️ User creation warning: {e}")

    # Grant Privileges ONLY on firevision database
    cursor.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{new_user}'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    print(f"✅ Privileges granted to '{new_user}' for database '{database}'.")

    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Pastikan XAMPP MySQL sudah jalan dan password root kosong (default).")
