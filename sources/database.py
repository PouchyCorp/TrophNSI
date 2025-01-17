import sqlite3
from hashlib import sha256
from tkinter import messagebox
import pygame as pg
import pickle
from room_config import DEFAULT_SAVE
from enum import Enum, auto
from ui.inputbox import InputBox
from ui.popup import InfoPopup

class LoginStates(Enum):
    HOME = auto()
    REGISTER_USERNAME = auto()
    REGISTER_PASSWORD = auto()
    LOGIN_USERNAME = auto()
    LOGIN_PASSWORD = auto()

class PgDataBase:
    def __init__(self):
        self.db_link = "userData.db"
        self.gui_state = LoginStates.HOME

        self.ready_to_launch = (False, None)



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
            if type(user_data) is dict:
                return user_data
        
        print("No pickled data found for user, loading default save.")
        return DEFAULT_SAVE

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
            self.ready_to_launch = (True, username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def save_user_data(self, username, data : dict):
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

    def tk_ui(self) -> tuple[str, dict]:
        self.initialize_database()
        fps = 60  # Frame rate
        CLOCK = pg.time.Clock
        WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
        WIN.fill('black')
        pg.display.set_icon(pg.image.load('data/big_icon.png'))

        quit_button = ()
        register_button = ()
        login_button = ()

        Username_input = InputBox(10,10,600,50,'username')
        Password_input = InputBox(10,10,600,50,'password')

        while True:
            CLOCK.tick(fps)  # Maintain frame rate
            mouse_pos = pg.mouse.get_pos()  # Create a coordinate object for the mouse position
            events = pg.event.get()  # Get all events from the event queue

            for event in events:
                if event.type == pg.QUIT:  # Check for quit event
                    pg.quit()  # Quit Pygame
                #handle events 


            pg.display.flip()  # Update the display


        #if root terminated and ready to launch, returns game data
        if self.ready_to_launch[0]:
            return self.ready_to_launch[1], self.fetch_user_data(self.ready_to_launch[1])