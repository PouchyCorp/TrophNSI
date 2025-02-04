import sqlite3
from hashlib import sha256
import pygame as pg
import pickle
from enum import Enum, auto
from ui.inputbox import InputBox
from  ui.infopopup import InfoPopup
from ui.button import Button
from ui.userlist import UserList
from  utils.room_config import DEFAULT_SAVE

class LoginStates(Enum):
    HOME = auto()
    REGISTER = auto()
    LOGIN = auto()

class PgDataBase:
    def __init__(self):
        self.db_link = "data/userData.db"
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
    
    def fetch_all_user_data(self):
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        cursor.execute('SELECT username, pickled_data FROM users')
        result = cursor.fetchall()
        connection.close()

        result = [(row[0], pickle.loads(row[1])) for row in result]

        return result


    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def fetch_user_data(self, username):
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        cursor.execute('SELECT pickled_data FROM users WHERE username == (?)', username)
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
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.info_popups.append(InfoPopup("Both fields are required!"))
            return
        
        connection = sqlite3.connect(self.db_link)
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, pickled_data) VALUES (?, ?, ?)', 
                        (username, self.hash_password(password), pickle.dumps(DEFAULT_SAVE)))
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
    
    def close(self):
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

    def home_screen(self) -> tuple[str, dict]:
        self.initialize_database()

        pg.init()
        fps = 60  # Frame rate
        CLOCK = pg.time.Clock()
        WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
        WIN.fill('black')
        win_rect = WIN.get_rect()
        pg.display.set_icon(pg.image.load('data/big_icon.png'))

        import ui.sprite as sprite

        quit_button = Button((0,0), self.quit, sprite.whiten(sprite.QUIT_BUTTON) , sprite.QUIT_BUTTON)
        close_button = Button((0,0), self.close, sprite.whiten(sprite.CLOSE_BUTTON) , sprite.CLOSE_BUTTON)
        register_button = Button((0,0), self.change_gui_to_register, sprite.whiten(sprite.REGISTER_BUTTON), sprite.REGISTER_BUTTON)
        login_button = Button((0,0), self.change_gui_to_login, sprite.whiten(sprite.LOGIN_BUTTON), sprite.LOGIN_BUTTON)
        accept_login_button = Button((0,0), self.login_user, sprite.whiten(sprite.CONFIRM_BUTTON), sprite.CONFIRM_BUTTON)
        accept_register_button = Button((0,0), self.register_user, sprite.whiten(sprite.CONFIRM_BUTTON), sprite.CONFIRM_BUTTON)
 
        userlist = UserList((0,0), self.fetch_all_user_data())

        login_button.rect.center = win_rect.center
        register_button.rect.center = (login_button.rect.centerx, login_button.rect.centery+login_button.rect.height+30)
        quit_button.rect.center = (register_button.rect.centerx, register_button.rect.centery+register_button.rect.height+30)
        close_button.rect.center = (register_button.rect.centerx, register_button.rect.centery+register_button.rect.height+30)
        accept_login_button.rect.center = register_button.rect.center
        accept_register_button.rect.center = register_button.rect.center
        self.password_input.rect.center = login_button.rect.center
        self.username_input.rect.center = (self.password_input.rect.centerx, self.password_input.rect.centery-self.password_input.rect.height-30)

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
                            close_button.handle_event(event)
                            accept_login_button.handle_event(event)

                        case LoginStates.REGISTER:
                            self.password_input.handle_event(event)
                            self.username_input.handle_event(event)
                            close_button.handle_event(event)
                            accept_register_button.handle_event(event)

                        case LoginStates.HOME:
                            quit_button.handle_event(event)
                            register_button.handle_event(event)
                            login_button.handle_event(event)
                    
                    userlist.init(self.fetch_all_user_data())
                    userlist.handle_event(event)
            
            #draw
            match self.gui_state:
                case LoginStates.LOGIN:
                    self.password_input.draw(WIN)
                    self.username_input.draw(WIN)
                    close_button.draw(WIN, close_button.rect.collidepoint(mouse_pos))
                    accept_login_button.draw(WIN, accept_login_button.rect.collidepoint(mouse_pos))

                case LoginStates.REGISTER:
                    self.password_input.draw(WIN)
                    self.username_input.draw(WIN)
                    close_button.draw(WIN, close_button.rect.collidepoint(mouse_pos))
                    accept_register_button.draw(WIN, accept_register_button.rect.collidepoint(mouse_pos))

                case LoginStates.HOME:
                    quit_button.draw(WIN, quit_button.rect.collidepoint(mouse_pos))
                    register_button.draw(WIN, register_button.rect.collidepoint(mouse_pos))
                    login_button.draw(WIN, login_button.rect.collidepoint(mouse_pos))
            
            userlist.draw(WIN)

            
            self.render_popups(WIN)
            
            pg.display.flip()  # Update the display


        #if root terminated and ready to launch, returns game data
        if self.ready_to_launch[0]:
            return self.ready_to_launch[1], self.fetch_user_data(self.ready_to_launch[1])