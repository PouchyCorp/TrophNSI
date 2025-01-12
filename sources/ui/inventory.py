from objects.placeable import Placeable
from utils.coord import Coord
from pygame import Surface, transform, BLEND_RGB_MIN, font, Rect, draw
from ui.sprite import ICON_1, WINDOW, nine_slice_scaling, FLECHE_GAUCHE, FLECHE_DROITE
from ui.confirmationpopup import ConfirmationPopup
from ui.popup import InfoPopup


BORDER_AROUND_WINDOW = 24
OBJECT_SIZE = 180
ITEMS_PER_PAGE = 8


class Inventory:
    def __init__(self, title: str = "Inventory", content : list[Placeable] = []) -> None:
        """Initializes the inventory with an optional title."""
        self.inv: list[Placeable] = content  # List of owned items
        self.displayed_objects: list[tuple[Placeable, Surface]] = []  # Rendered items on the current page
        self._page: int = 0  # Current page index
        self.font = font.SysFont(None, 30)  # Font for labels
        self.title = title  # Title of the inventory
        self.window_sprite: Surface = WINDOW  # Window background
        self.button_prev_rect = FLECHE_GAUCHE.get_rect(topleft = (64,975))
        self.button_next_rect = FLECHE_GAUCHE.get_rect(topleft = (224,975))
    def init(self):
        """Initializes the objects for rendering on the current page."""
        # Paginate items
        start = self._page * ITEMS_PER_PAGE
        end = (self._page + 1) * ITEMS_PER_PAGE
        self.displayed_objects = self.inv[start:end]

        self._process_objects()
        self._resize_window_sprite()

    def _process_objects(self):
        """Processes each object for rendering on the current page."""
        processed_objects = []

        for ind, obj in enumerate(self.displayed_objects):
            # Scale the object to fit within a thumbnail
            biggest_side = max(obj.rect.width, obj.rect.height)
            scale_ratio = OBJECT_SIZE / biggest_side
            thumbnail_surf = transform.scale_by(obj.surf, scale_ratio)
            thumbnail_rect = thumbnail_surf.get_rect()

            # Apply greyscale if the object is placed
            if obj.placed:
                thumbnail_surf.fill((50, 50, 50), special_flags=BLEND_RGB_MIN)

            # Position the thumbnail
            thumbnail_rect.x = BORDER_AROUND_WINDOW + 12 if ind % 2 == 0 else BORDER_AROUND_WINDOW + OBJECT_SIZE + 20 + 12
            thumbnail_rect.y = 72 + (220 * (ind // 2))

            # Create a new Placeable for the thumbnail
            thumbnail_placeable = Placeable(obj.name, Coord(obj.coord.room_num, thumbnail_rect.topleft), thumbnail_surf)
            thumbnail_placeable.id = obj.id
            thumbnail_placeable.pixelise()

            # Create a label for the object
            label_surf = self.font.render(obj.name, True, "green")

            # Add to processed list
            processed_objects.append((thumbnail_placeable, label_surf))

        self.displayed_objects = processed_objects

    def _resize_window_sprite(self):
        """Resizes the window sprite based on the displayed objects."""
        width = BORDER_AROUND_WINDOW * 2 + OBJECT_SIZE + 144
        height = OBJECT_SIZE*5
        self.window_sprite = nine_slice_scaling(WINDOW, (width, height), 12)

    def draw(self, win: Surface, mouse_pos: Coord):
        """Draws the inventory or shop interface on the screen."""
        win.blit(self.window_sprite, (12, 60))
        self._draw_title(win)
        self._mouse_highlight(win, mouse_pos)

        # Draw objects and their labels
        win.blits([(plcb.surf, plcb.rect.topleft) for plcb, _ in self.displayed_objects])
        win.blits([(txt_surf, (plcb.rect.x, plcb.rect.y + 190)) for plcb, txt_surf in self.displayed_objects])

        # Draw navigation buttons
        self._draw_navigation_buttons(win)

    def _draw_title(self, win: Surface):
        """Draws the title of the inventory or shop."""
        title_surf = self.font.render(self.title, True, "white")
        win.blit(title_surf, (BORDER_AROUND_WINDOW, 42))

    def _mouse_highlight(self, win: Surface, mouse_pos: Coord):
        """Highlights the item under the mouse pointer."""
        for placeable, _ in self.displayed_objects:
            if placeable.rect.collidepoint(mouse_pos.xy):
                placeable.draw_outline(win, (150, 150, 255))

    def _draw_navigation_buttons(self, win: Surface):
        """Draws the previous and next page buttons."""
        #.rect(win, (100, 100, 100), self.button_prev_rect) #temp
        draw.rect(win, (100, 100, 100), self.button_next_rect) #temp
        win.blit(FLECHE_GAUCHE, self.button_prev_rect)
        win.blit(FLECHE_DROITE, self.button_next_rect)

    def handle_navigation(self, mouse_pos: Coord):
        """Handles navigation button clicks to change pages."""
        if self.button_prev_rect.collidepoint(mouse_pos.xy) and self._page > 0:
            self._page -= 1
            self.init()
        elif self.button_next_rect.collidepoint(mouse_pos.xy) and (self._page + 1) * ITEMS_PER_PAGE < len(self.inv):
            self._page += 1
            self.init()
    
    def handle_click(self, mouse_pos):
        """returns the placeable contained in inventory if all conditions are valid : placeable not already placed, mouse clicked on it"""
        clicked_showed_obj_id = self._select_item(mouse_pos)  # Check if an inventory item was clicked, and if the object is already placed
        if clicked_showed_obj_id:
            clicked_obj = self._search_by_id(clicked_showed_obj_id)  # Retrieve the object by its ID
            if not clicked_obj.placed:
                return clicked_obj
        return None

    def _select_item(self, mouse_pos: Coord) -> str | None:
        """Returns the ID of the selected item, or None if no item is selected or the item is already placed."""
        for placeable, _ in self.displayed_objects:
            if placeable.rect.collidepoint(mouse_pos.xy) and not placeable.placed:
                return placeable.id
        return None

    def _search_by_id(self, item_id: int) -> Placeable | None:
        """Finds and returns the first placeable matching the given ID."""
        for obj in self.inv:
            if obj.id == item_id:
                return obj
        return None

    def __repr__(self):
        """Returns a string representation of the inventory."""
        return str(self.__dict__)


class Shop(Inventory):
    def buy_object(self, obj : Placeable, game):
        if game.gold - obj.price >= 0:
            game.gold -= obj.price
            game.inventory.inv.append(obj)
            self.inv.remove(obj)
            self.init()
            game.popups.append(InfoPopup(f"{obj.name} a été ajouté à ton inventaire !"))
        else:
            game.popups.append(InfoPopup("Tu n'as as assez d'argent pour acheter l'objet :("))

    def handle_click(self, mouse_pos : Coord, game):
        """checks if click event happenend on an object, and launches confirmation for buying"""
        clicked_showed_obj_id = self._select_item(mouse_pos)  # Check if an inventory item was clicked, and if the object is already placed
        if clicked_showed_obj_id:
            clicked_obj = self._search_by_id(clicked_showed_obj_id)  # Retrieve the object by its ID
            game.confirmation_popups.append(ConfirmationPopup(game.win, f"acheter cet objet pour {clicked_obj.price}$?", self.buy_object, yes_func_args=[clicked_obj, game]))
            from core.logic import State
            game.gui_state = State.CONFIRMATION