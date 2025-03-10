# migrate_db.py
import psycopg2

conn_string = "host='localhost' dbname='ci_metrics' user='mitalijuvekar' password='MiTuLi26@02'"

def migrate_database():
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if columns exist before adding them
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='builds' AND column_name='branch'")
        if cursor.fetchone() is None:
            print("Adding 'branch' column to builds table...")
            cursor.execute("ALTER TABLE builds ADD COLUMN branch VARCHAR")
        else:
            print("Column 'branch' already exists.")
            
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='builds' AND column_name='commit_hash'")
        if cursor.fetchone() is None:
            print("Adding 'commit_hash' column to builds table...")
            cursor.execute("ALTER TABLE builds ADD COLUMN commit_hash VARCHAR")
        else:
            print("Column 'commit_hash' already exists.")
            
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()