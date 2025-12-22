import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'firevision')
    )

def init_db():
    try:
        # Connect to MySQL Server first to create DB if not exists
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        c = conn.cursor()
        db_name = os.getenv('DB_NAME', 'firevision')
        c.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.close()

        # Connect to the specific database
        conn = get_db_connection()
        c = conn.cursor()
        
        # Table Alarms
        c.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uuid VARCHAR(255),
                timestamp VARCHAR(255),
                camera_id VARCHAR(255),
                zone VARCHAR(255),
                confidence REAL,
                status VARCHAR(50), 
                image_path TEXT
            )
        ''')

        # Simple Migration: Check if status column exists in alarms, if not add it
        try:
            c.execute("SHOW COLUMNS FROM alarms LIKE 'status'")
            result = c.fetchone()
            if not result:
                print("Migrating: Adding 'status' column to alarms table")
                c.execute("ALTER TABLE alarms ADD COLUMN status VARCHAR(50) DEFAULT 'Unverified'")
                conn.commit()
        except Exception as e:
            print(f"Migration warning: {e}")
        
        # Table Users
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                plan VARCHAR(50) DEFAULT 'free'
            )
        ''')

        # Table Transactions
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(255) UNIQUE,
                username VARCHAR(255),
                amount INT,
                status VARCHAR(50),
                snap_token VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table Notification Settings
        c.execute("""
            CREATE TABLE IF NOT EXISTS notification_settings (
                username VARCHAR(255) PRIMARY KEY,
                telegram_enabled BOOLEAN DEFAULT FALSE,
                telegram_bot_token TEXT,
                telegram_chat_id TEXT,
                email_enabled BOOLEAN DEFAULT FALSE,
                email_smtp_host VARCHAR(255),
                email_smtp_port INT DEFAULT 587,
                email_sender VARCHAR(255),
                email_password TEXT,
                email_recipient TEXT,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        """)

        # Migration: Add plan column if not exists
        try:
            c.execute("SELECT plan FROM users LIMIT 1")
            c.fetchall() 
        except Exception:
            print("⚠️ 'plan' column missing in users. Adding it...")
            try:
                c.execute("ALTER TABLE users ADD COLUMN plan VARCHAR(50) DEFAULT 'free'")
            except Exception as e_alter:
                print(f"❌ Failed to alter table: {e_alter}")

        # Migration: Add email column if not exists (Verified for Forgot Password feature)
        try:
            c.execute("SELECT email FROM users LIMIT 1")
            c.fetchall()
        except Exception:
             print("⚠️ 'email' column missing in users. Adding it...")
             try:
                 c.execute("ALTER TABLE users ADD COLUMN email VARCHAR(255) UNIQUE")
             except Exception as e_alter:
                 print(f"❌ Failed to add email column: {e_alter}")
        
        # Table Password Resets (Temporary tokens)
        c.execute('''
            CREATE TABLE IF NOT EXISTS password_resets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255),
                token VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized ({db_name}: alarms, users, notification_settings, password_resets)")
    except Exception as e:
        print(f"❌ Error initializing DB: {e}")
