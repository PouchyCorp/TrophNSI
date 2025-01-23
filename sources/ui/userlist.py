from pygame import Surface, Rect, MOUSEBUTTONUP
from ui.sprite import WINDOW, nine_slice_scaling
from utils.fonts import TERMINAL_FONT
from core.spectator import Spectator

class UserList:
    def __init__(self, coord : tuple, content : list[tuple]):
        self.coord = coord
        self.content = content
        self.lengh = len(content)
        self.page = 1
        self.processed_tabs = []
        self.init()

    def init(self):
        self.displayed_content = self.content[(self.page-1)*4:self.page*4]
        self.process_tabs()

    def process_tabs(self) -> list[tuple[Surface, Rect]]:
        self.processed_tabs = []
        for i, data in enumerate(self.displayed_content):
            username, dic = data
            username_surf = TERMINAL_FONT.render(username, True, "white")
            rect = Rect(self.coord[0]+24, self.coord[1]+(100*i)+24, 1000, 100)
            
            bg_surf = nine_slice_scaling(WINDOW, rect.size, (12,12,12,12))
            bg_surf.blit(username_surf, (12,12))

            self.processed_tabs.append((bg_surf, rect))

    def draw(self, win : Surface):
        win.blits(self.processed_tabs)


    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            mouse_pos = event.pos
            for i, tab in enumerate(self.processed_tabs):
                if tab[1].collidepoint(mouse_pos):
                    Spectator(self.displayed_content[i][1]).start_spectating()
