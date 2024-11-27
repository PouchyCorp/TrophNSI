from placeable import Placeable
from coord import Coord
from pygame import Surface, transform, BLEND_RGB_MIN, font
from sprite import ICON_1, WINDOW, nine_slice_scaling

class Inventory:
    def __init__(self) -> None:
        '''list of owned items'''
        self.inv : list[Placeable] = []

        #showed placeables when opened
        self.showed_objects : list[tuple[Placeable, Surface]] = []
        #false if closed, true if opened
        self._page = 0
        self.font = font.SysFont(None,30)

        self.window_sprite : Surface = WINDOW

    def open(self):
        """initialise all objects for rendering"""
        self.showed_objects = self.inv[self._page*8:(self._page+1)*8]

        for ind , obj in enumerate(self.showed_objects):
            #8 element at a time ( or else too big)
          
            biggest_side = max([obj.rect.width, obj.rect.height])
            scale_ratio = 180/biggest_side

            thumbnail_surf = transform.scale_by(obj.surf, scale_ratio)
            thumbnail_rect = thumbnail_surf.get_rect()

            #greyscale placed objects
            if obj.placed == True:
                thumbnail_surf.fill((50,50,50), special_flags=BLEND_RGB_MIN)

            #placement
            if ind % 2 == 0:
                thumbnail_rect.x = 12
            else:
                thumbnail_rect.x = 12+180+20
            thumbnail_rect.y = 72+(220*(ind//2))

            
            #create placeable
            thumbnail_placeable = Placeable(obj.name, Coord(obj.coord.room_num, thumbnail_rect.topleft), thumbnail_surf)
            #important
            thumbnail_placeable.id = obj.id

            thumbnail_placeable.pixelise()

            #blit label on thumbnail
            #label
            label_text = obj.name
            label_surf = self.font.render(label_text,True,"green")

            #update list
            #self.showed change de type
            self.showed_objects[ind] = (thumbnail_placeable, label_surf)
        
        if self.showed_objects:
            first_obj_topleft = self.showed_objects[0][0].rect.topleft
            last_obj_bottomright = self.showed_objects[-1][0].rect.bottomright
            if len(self.showed_objects) > 1:
                difference = (12+180+144+12, last_obj_bottomright[1]-first_obj_topleft[1]+24)
            else:
                difference = (12+138, 24+180)
            self.window_sprite = nine_slice_scaling(WINDOW, difference, 6)
        else:
            self.window_sprite = nine_slice_scaling(WINDOW, (180,180), 6)

    def draw(self, win : Surface, mouse_pos : Coord, is_open : bool):
        if is_open:

            #keep this order
            win.blit(self.window_sprite, (0,60))
            self.mouse_highlight(win, mouse_pos)
            win.blits([(plcb.surf, plcb.rect.topleft) for plcb, _ in self.showed_objects])
            win.blits([(txt_surf, (plcb.rect.x, plcb.rect.y+190)) for plcb, txt_surf in self.showed_objects])

        else:
            win.blit(ICON_1, (0,60))
    
    def mouse_highlight(self, win : Surface, mouse_pos : Coord):
        for placeable, _ in self.showed_objects:
            if placeable.rect.collidepoint(mouse_pos.xy):
                placeable.draw_outline(win,(150,150,255))


    def select_item(self, mouse_pos : Coord) -> str | None:
        """return the id of the item selected
        returns None if no items"""
        for placeable, _ in self.showed_objects:
            if placeable.rect.collidepoint(mouse_pos.xy):
                return placeable.id
        return None
    
    def search_by_id(self, id : int) -> Placeable:
        '''returns the first placeable matching the id'''
        for obj in self.inv:
            if obj.id == id:
                return obj

    def __repr__(self):
        return str(self.__dict__)