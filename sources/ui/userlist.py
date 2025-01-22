from pygame import Surface, Rect
from utils.fonts import TERMINAL_FONT

class UserList:
    def __init__(self, coord : tuple, content : list[tuple]):
        self.coord = coord
        self.content = content
        self.lengh = len(content)
        self.page = 1
        self.init()

    def init(self):
        self.displayed_content = self.content[(self.page-1)*4:self.page*4]
        self.processed_tabs : tuple[Surface, Rect] = self.process_tabs()

    def process_tabs(self) -> tuple[Surface, Rect]:
        for username, dic in self.displayed_content:
            pass

    def draw(self, win):
        pass


    def handle_event(self, event):
        pass
