import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "secureportal.db"

def initialise_database():
    """Create the SecurePortal database and users table."""

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
             ) """
         )

    cursor.execute(
    """
    INSERT OR IGNORE INTO users (username, password_hash, role)
    VALUES (?, ?, ?)
    """,
    (
        "amina",
        generate_password_hash("Cyber123"),
        "Student"
    )
)

    cursor.execute(
    """
    INSERT OR IGNORE INTO users (username, password_hash, role)
    VALUES (?, ?, ?)
    """,
    (
        "admin",
        generate_password_hash("Admin123"),
        "Administrator"
    )
)

    connection.commit()
    connection.close()
    
    print("Database initialised successfully.")

if __name__ == "__main__":
    initialise_database()