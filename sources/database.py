import sqlite3
from hashlib import sha256

def init_db():
    connection = sqlite3.connect("testDb.db")
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)""")
    connection.commit()
    connection.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_user(username, password):
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    try:
        # Insert user into the database
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hash_password(password)))
        connection.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        connection.close()

def login_user(username, password):
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    
    if result and result[0] == hash_password(password):
        print("Login successful!")
    else:
        print("Error: Invalid username or password.")
    
    connection.close()


def main():
    init_db()
    while True:
        print("\n--- Login System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_user(username, password)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
