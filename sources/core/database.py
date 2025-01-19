import sqlite3
from hashlib import sha256
import pygame as pg
import pickle
from enum import Enum, auto
from ui.inputbox import InputBox
from  ui.infopopup import InfoPopup
from ui.button import Button

class LoginStates(Enum):
    HOME = auto()
    REGISTER = auto()
    LOGIN = auto()

class PgDataBase:
    def __init__(self):
        self.db_link = "userData.db"
        self.gui_state = LoginStates.HOME

        self.ready_to_launch = (False, None)

        self.username_input = InputBox(10,10,600,50)
        self.password_input = InputBox(10,70,600,50)

        self.info_popups : list[InfoPopup]= []

#-------------------------------------------------
#               DATABASE PART
#-------------------------------------------------

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
        cursor.execute('SELECT pickled_data FROM users WHERE username = ?', (username))
        result = cursor.fetchone()
        connection.close()

        if result and result[0]:
            pickled_data = result[0]
            user_data = pickle.loads(pickled_data)  # Deserialize the data
            print("got user data")
            if type(user_data) is dict:
                return user_data
        
        print("No pickled data found for user, loading default save.")
        from  utils.room_config import DEFAULT_SAVE
        return DEFAULT_SAVE

    def register_user(self):
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.info_popups.append(InfoPopup("Both fields are required!"))
            return
        
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                        (username, self.hash_password(password)))
            connection.commit()
            self.info_popups.append(InfoPopup("User registered successfully!"))
        except sqlite3.IntegrityError:
            self.info_popups.append(InfoPopup("Username already exists."))
        finally:
            connection.close()

    def login_user(self):
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.info_popups.append(InfoPopup("Both fields are required!"))
            return
        
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        connection.close()
        
        if result and result[0] == self.hash_password(password):
            self.info_popups.append(InfoPopup("Login successful!"))
            self.ready_to_launch = (True, username)
        else:
            self.info_popups.append(InfoPopup("Invalid username or password."))

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


#-------------------------------------------------
#               GUI PART
#-------------------------------------------------
    def quit(self):
        if self.gui_state is LoginStates.HOME:
            from sys import exit
            exit()
        else:
            self.gui_state = LoginStates.HOME
    
    def change_gui_to_login(self):
        self.gui_state = LoginStates.LOGIN
    
    def change_gui_to_register(self):
        self.gui_state = LoginStates.REGISTER
    
    def render_popups(self, win):  
        # Iterate over existing popups to render and manage their lifetime
        for popup in self.info_popups:
            if popup.lifetime <= 0:
                self.info_popups.remove(popup)  # Remove expired popups
            else:
                popup.draw(win)  # Render the popup on the window
                popup.lifetime -= 1  # Decrement popup's lifetime

    def tk_ui(self) -> tuple[str, dict]:
        self.initialize_database()
        fps = 60  # Frame rate
        CLOCK = pg.time.Clock()
        WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
        WIN.fill('black')
        pg.display.set_icon(pg.image.load('data/big_icon.png'))

        import ui.sprite as sprite

        quit_button = Button((10,200), self.quit, sprite.whiten(sprite.QUIT_BUTTON) , sprite.QUIT_BUTTON)
        register_button = Button((10,300), self.change_gui_to_register, sprite.whiten(sprite.REGISTER_BUTTON), sprite.REGISTER_BUTTON)
        login_button = Button((10,400), self.change_gui_to_login, sprite.whiten(sprite.LOGIN_BUTTON), sprite.LOGIN_BUTTON)
        accept_login_button = Button((10,300), self.login_user, sprite.whiten(sprite.CONFIRM_BUTTON), sprite.CONFIRM_BUTTON)
        accept_register_button = Button((10,300), self.register_user, sprite.whiten(sprite.CONFIRM_BUTTON), sprite.CONFIRM_BUTTON)


        while not self.ready_to_launch[0]:
            CLOCK.tick(fps)  # Maintain frame rate
            mouse_pos = pg.mouse.get_pos()  # Create a coordinate object for the mouse position
            events = pg.event.get()  # Get all events from the event queue
            WIN.fill('blue')

            for event in events:
                if event.type == pg.QUIT:  # Check for quit event
                    pg.quit()  # Quit Pygame
                    from sys import exit
                    exit()

                if event.type in [pg.MOUSEBUTTONUP, pg.KEYDOWN]:
                    match self.gui_state:
                        case LoginStates.LOGIN:
                            self.password_input.handle_event(event)
                            self.username_input.handle_event(event)
                            quit_button.handle_event(event)
                            accept_login_button.handle_event(event)

                        case LoginStates.REGISTER:
                            self.password_input.handle_event(event)
                            self.username_input.handle_event(event)
                            quit_button.handle_event(event)
                            accept_register_button.handle_event(event)

                        case LoginStates.HOME:
                            quit_button.handle_event(event)
                            register_button.handle_event(event)
                            login_button.handle_event(event)
            
            #draw
            match self.gui_state:
                case LoginStates.LOGIN:
                    self.password_input.draw(WIN)
                    self.username_input.draw(WIN)
                    quit_button.draw(WIN, quit_button.rect.collidepoint(mouse_pos))
                    accept_login_button.draw(WIN, accept_login_button.rect.collidepoint(mouse_pos))

                case LoginStates.REGISTER:
                    self.password_input.draw(WIN)
                    self.username_input.draw(WIN)
                    quit_button.draw(WIN, quit_button.rect.collidepoint(mouse_pos))
                    accept_register_button.draw(WIN, accept_register_button.rect.collidepoint(mouse_pos))

                case LoginStates.HOME:
                    quit_button.draw(WIN, quit_button.rect.collidepoint(mouse_pos))
                    register_button.draw(WIN, register_button.rect.collidepoint(mouse_pos))
                    login_button.draw(WIN, login_button.rect.collidepoint(mouse_pos))

            
            self.render_popups(WIN)
            
            pg.display.flip()  # Update the display


        #if root terminated and ready to launch, returns game data
        if self.ready_to_launch[0]:
            return self.ready_to_launch[1], self.fetch_user_data(self.ready_to_launch[1])