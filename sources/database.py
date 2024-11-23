import sqlite3
from hashlib import sha256
import tkinter as tk
from tkinter import messagebox
import pickle
import pygame

def initialize_database():
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            pickled_data BLOB)
    ''')
    connection.commit()
    connection.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def fetch_user_data(username):
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    cursor.execute('SELECT pickled_data FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    connection.close()

    if result and result[0]:
        pickled_data = result[0]
        user_data = pickle.loads(pickled_data)  # Deserialize the data
        print("got user data")
        return user_data
    else:
        print("No pickled data found for user.")
        return None

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Input Error", "Both fields are required!")
        return
    
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                       (username, hash_password(password)))
        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        connection.close()

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Input Error", "Both fields are required!")
        return
    
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    connection.close()
    
    if result and result[0] == hash_password(password):
        messagebox.showinfo("Success", "Login successful!")
        pygame_window(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def save_user_data(username, data):
    """
    Save pickled user data to the database.
    Args:
        username (str): The username of the user.
        data (dict): The data to be pickled and saved.
    """
    pickled_data = pickle.dumps(data)  # Serialize the data
    connection = sqlite3.connect('testDb.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET pickled_data = ? WHERE username = ?', (pickled_data, username))
    connection.commit()
    connection.close()
    print('successfuly saved')


def pygame_window(username : str):
    pygame.init()
    WIN = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Welcome to Pygame!")
    running = True
    
    user_data = fetch_user_data(username)
    
    if type(user_data) == list:
        rects = user_data
    else:
        rects = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save_user_data(username, rects)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                rects.append(pygame.Rect(mouse_pos[0], mouse_pos[1], 10, 10))
        
        WIN.fill((30, 30, 30))
        for rect in rects:
            pygame.draw.rect(WIN, "white", rect)
        pygame.display.flip()

    pygame.quit()

initialize_database()

root = tk.Tk()
root.title("SQLite Login Test")

tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)


btn_register = tk.Button(root, text="Register", command=register_user)
btn_register.grid(row=2, column=0, padx=10, pady=10)

btn_login = tk.Button(root, text="Login", command=login_user)
btn_login.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()