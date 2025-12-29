import mysql.connector
import os
import getpass
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load env variables from .env file (if any)
load_dotenv()

def get_manual_db_connection():
    print("\n--- CONNECTION SETUP ---")
    print("Option 1: Paste the full 'MYSQL_URL' or 'Public Networking URL' from Railway.")
    print("          (Format: mysql://user:pass@host:port/db)")
    print("Option 2: Press ENTER to input fields manually.\n")
    
    conn_url = input("Paste Connection URL (or ENTER): ").strip()
    
    host, user, password, database, port = None, None, None, None, 3306
    
    if conn_url and conn_url.startswith("mysql://"):
        try:
            # Parse mysql://user:pass@host:port/db
            # Remove prefix
            clean = conn_url.replace("mysql://", "")
            
            # Split user:pass @ host:port/db
            creds, rest = clean.split("@")
            user, password = creds.split(":")
            
            # Split host:port / db
            if "/" in rest:
                net, database = rest.split("/")
            else:
                net = rest
                database = os.getenv('DB_NAME', 'railway')
                
            if ":" in net:
                host, port = net.split(":")
                port = int(port)
            else:
                host = net
                
            print(f"✅ Parsed: {user}@{host}:{port}/{database}")
        except Exception as e:
            print(f"⚠️ Failed to parse URL: {e}. Switching to manual input...")
            conn_url = None

    if not conn_url:
        # 1. HOST
        default_host = os.getenv('DB_HOST', 'localhost')
        host = input(f"DB Host [{default_host}]: ").strip() or default_host

        # 2. USER
        default_user = os.getenv('DB_USER', 'root')
        user = input(f"DB User [{default_user}]: ").strip() or default_user

        # 3. PASSWORD
        default_pass = os.getenv('DB_PASSWORD', '')
        password = input(f"DB Password [******]: ").strip()
        if not password: 
            password = default_pass

        # 4. DATABASE
        default_db = os.getenv('DB_NAME', 'railway')
        database = input(f"DB Name [{default_db}]: ").strip() or default_db

        # 5. PORT
        default_port = os.getenv('DB_PORT', '3306')
        p_input = input(f"DB Port [{default_port}]: ").strip()
        port = int(p_input) if p_input else int(default_port)

    print(f"\n🔄 Connecting to {user}@{host}:{port}/{database} ...")

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connection_timeout=10
        )
        return conn
    except Exception as e:
        print(f"❌ DB Connection failed: {e}")
        return None

def add_user():
    conn = get_manual_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(dictionary=True)
        username = "userpro"
        raw_password = "userpro123"
        hashed = generate_password_hash(raw_password)
        
        print(f"Checking if '{username}' exists...")
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            print(f"User '{username}' found. Updating to PRO plan and resetting password...")
            cursor.execute("UPDATE users SET plan = 'pro', password = %s WHERE username = %s", (hashed, username))
        else:
            print(f"User '{username}' not found. Creating new PRO user...")
            cursor.execute("INSERT INTO users (username, password, plan) VALUES (%s, %s, 'pro')", (username, hashed))
            
        conn.commit()
        print("\n✅ SUCCESS!")
        print(f"User '{username}' is ready on the connected database.")
        print("👉 Login details: userpro / userpro123")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    add_user()
