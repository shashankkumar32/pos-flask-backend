import os
import pymysql
from dotenv import load_dotenv

def check_db():
    print("--- Database Diagnostic Tool ---")
    
    # Load environment variables
    load_dotenv()
    
    host = os.environ.get("DB_HOST", "localhost")
    port = int(os.environ.get("DB_PORT", "3306"))
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "testdb")
    
    print(f"Targeting: {host}:{port} ({db_name})")
    print(f"User: {user}")
    
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port,
            connect_timeout=10
        )
        print("\n✅ SUCCESS: Connection established successfully!")
        connection.close()
    except pymysql.err.OperationalError as e:
        error_code, error_msg = e.args
        print(f"\n❌ ERROR (OperationalError): {error_msg}")
        
        if "Too many connections" in error_msg:
            print("👉 Analysis: You have reached the maximum allowed concurrent connections for your database.")
        elif "Access denied" in error_msg:
            print("👉 Analysis: Invalid credentials. Check your DB_USER and DB_PASSWORD.")
        elif "Can't connect to MySQL server" in error_msg:
            print("👉 Analysis: The server is unreachable. If you are on Railway, check if your project is active or hit the usage limit.")
        else:
            print("👉 Analysis: General connection failure. Check if the database host is up.")
            
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    check_db()
