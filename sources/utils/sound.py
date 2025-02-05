import pygame

class SoundManager:
    def __init__(self, timermanager):
        self.timer = timermanager

        self.accrocher = pygame.mixer.Sound('data/sounds/accrocher_tableau.wav') #
        self.accrocher2 = pygame.mixer.Sound('data/sounds/accrocher.mp3') #
        self.achieve = pygame.mixer.Sound('data/sounds/achieve.mp3') #
        self.blank_sound = pygame.mixer.Sound('data/sounds/blank_sound.mp3')
        self.bott = pygame.mixer.Sound('data/sounds/bot or mites.mp3')
        self.down = pygame.mixer.Sound('data/sounds/Doordown.wav') #
        self.up = pygame.mixer.Sound('data/sounds/elevator.wav') #
        self.floorcracking = pygame.mixer.Sound('data/sounds/floorcracking.mp3')
        self.incorrect = pygame.mixer.Sound('data/sounds/incorrect.mp3') #
        self.items = pygame.mixer.Sound('data/sounds/items.mp3') #
        self.mite = pygame.mixer.Sound('data/sounds/mite.mp3')
        self.mites = pygame.mixer.Sound('data/sounds/mites.mp3')
        self.mites2 = pygame.mixer.Sound('data/sounds/mites2.mp3')
        self.mites3 = pygame.mixer.Sound('data/sounds/mites3.mp3')
        self.mites4 = pygame.mixer.Sound('data/sounds/mites4.mp3')
        self.mites5 = pygame.mixer.Sound('data/sounds/mites5.mp3')
        self.noise = pygame.mixer.Sound('data/sounds/noise.mp3')
        self.rain = pygame.mixer.Sound('data/sounds/rain.mp3')
        self.robot_moving = pygame.mixer.Sound('data/sounds/robot_moving.mp3')
        self.robot = pygame.mixer.Sound('data/sounds/robot.mp3')
        self.robot1 = pygame.mixer.Sound('data/sounds/robot1.wav')
        self.robot2 = pygame.mixer.Sound('data/sounds/robot2.wav')
        self.robot3 = pygame.mixer.Sound('data/sounds/robot3.wav')
        self.robot4 = pygame.mixer.Sound('data/sounds/robot4.wav')
        self.robot5 = pygame.mixer.Sound('data/sounds/robot5.wav')
        self.robot6 = pygame.mixer.Sound('data/sounds/robot6.wav')
        self.robot7 = pygame.mixer.Sound('data/sounds/robot7.mp3')
        self.robots = pygame.mixer.Sound('data/sounds/robots.mp3')
        self.shop = pygame.mixer.Sound('data/sounds/shop.wav') #
        self.walk = pygame.mixer.Sound('data/sounds/walk.wav')
        self.wind = pygame.mixer.Sound('data/sounds/wind.mp3')

        self.noise_blank=[self.wind,
                          self.rain,
                          self.floorcracking
        ]

        self.robot=[self.robot, 
                    self.robot1,
                    self.robot2,  
                    self.robot3, 
                    self.robot4, 
                    self.robot5, 
                    self.robot6, 
                    self.robot7, 
                    self.robots]