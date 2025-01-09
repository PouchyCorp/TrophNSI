import sqlite3
from hashlib import sha256
import tkinter as tk
from tkinter import messagebox
import pickle
import pygame




class TkDataBase:
    def __init__(self):
        self.db_link = "testDb.db"
        self.root = tk.Tk()
        self.root.title("Login window")

        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)


        self.btn_register = tk.Button(self.root, text="Register", command=self.register_user)
        self.btn_register.grid(row=2, column=0, padx=10, pady=10)

        self.btn_login = tk.Button(self.root, text="Login", command=self.login_user)
        self.btn_login.grid(row=2, column=1, padx=10, pady=10)

    def initialize_database(self):
        connection = sqlite3.connect(self.db_link)
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

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def fetch_user_data(self, username):
        connection = sqlite3.connect(self.db_link)
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

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Both fields are required!")
            return
        
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                        (username, self.hash_password(password)))
            connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            connection.close()

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Both fields are required!")
            return
        
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        connection.close()
        
        if result and result[0] == self.hash_password(password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy() #-----------------------------Starts game
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def save_user_data(self, username, data):
        """
        Save pickled user data to the database.
        Args:
            username (str): The username of the user.
            data (dict): The data to be pickled and saved.
        """
        pickled_data = pickle.dumps(data)  # Serialize the data
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET pickled_data = ? WHERE username = ?', (pickled_data, username))
        connection.commit()
        connection.close()
        print('successfuly saved')


    def launch_game(username : str):
        
        user_data = self.fetch_user_data(username)
        

    def tk_ui(self):
        self.initialize_database()

        self.root.mainloop()