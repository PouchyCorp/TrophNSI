import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
INVENTORY_ROWS, INVENTORY_COLS = 2, 4
CELL_SIZE = 64
INVENTORY_WIDTH = INVENTORY_COLS * CELL_SIZE
INVENTORY_HEIGHT = INVENTORY_ROWS * CELL_SIZE
SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT = 40, INVENTORY_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

class InventorySystem:
    def __init__(self, screen):
        self.screen = screen
        self.items = [
            "Sword", "Shield", "Potion", "Bow", "Arrow", "Helmet", "Armor", "Boots",
            "Ring", "Amulet", "Key", "Scroll", "Map", "Torch", "Food", "Water"
        ]  # Test items
        self.current_scroll_index = 0
        self.inventory_open = False
        self.font = pygame.font.Font(None, 36)

    def draw_inventory(self):
        # Draw inventory background
        inventory_x = (SCREEN_WIDTH - INVENTORY_WIDTH) // 2
        inventory_y = (SCREEN_HEIGHT - INVENTORY_HEIGHT) // 2
        pygame.draw.rect(self.screen, GRAY, (inventory_x, inventory_y, INVENTORY_WIDTH, INVENTORY_HEIGHT))

        # Draw items in grid
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                index = self.current_scroll_index + row * INVENTORY_COLS + col
                if index < len(self.items):
                    x = inventory_x + col * CELL_SIZE
                    y = inventory_y + row * CELL_SIZE
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)

                    # Render item name
                    item_text = self.font.render(self.items[index], True, BLACK)
                    self.screen.blit(item_text, (x + 5, y + 5))

        # Draw scroll buttons
        left_button = pygame.Rect(inventory_x - SCROLL_BUTTON_WIDTH, inventory_y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
        right_button = pygame.Rect(inventory_x + INVENTORY_WIDTH, inventory_y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)

        pygame.draw.rect(self.screen, BLUE, left_button)
        pygame.draw.rect(self.screen, BLUE, right_button)

        left_text = self.font.render("<", True, WHITE)
        right_text = self.font.render(">", True, WHITE)

        self.screen.blit(left_text, (left_button.centerx - left_text.get_width() // 2, left_button.centery - left_text.get_height() // 2))
        self.screen.blit(right_text, (right_button.centerx - right_text.get_width() // 2, right_button.centery - right_text.get_height() // 2))

        return left_button, right_button

    def handle_click(self, pos):
        inventory_x = (SCREEN_WIDTH - INVENTORY_WIDTH) // 2
        inventory_y = (SCREEN_HEIGHT - INVENTORY_HEIGHT) // 2

        # Check grid click
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                x = inventory_x + col * CELL_SIZE
                y = inventory_y + row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if rect.collidepoint(pos):
                    index = self.current_scroll_index + row * INVENTORY_COLS + col
                    if index < len(self.items):
                        print(f"Clicked on {self.items[index]}")

        # Check scroll buttons
        left_button = pygame.Rect(inventory_x - SCROLL_BUTTON_WIDTH, inventory_y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
        right_button = pygame.Rect(inventory_x + INVENTORY_WIDTH, inventory_y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)

        if left_button.collidepoint(pos) and self.current_scroll_index > 0:
            self.current_scroll_index -= INVENTORY_COLS
        elif right_button.collidepoint(pos) and self.current_scroll_index + INVENTORY_ROWS * INVENTORY_COLS < len(self.items):
            self.current_scroll_index += INVENTORY_COLS

    def toggle_inventory(self):
        self.inventory_open = not self.inventory_open

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.toggle_inventory()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.inventory_open:
                    self.handle_click(event.pos)

    def render(self):
        if self.inventory_open:
            self.draw_inventory()

# Main loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inventory System")
clock = pygame.time.Clock()

inventory = InventorySystem(screen)
running = True
while running:
    screen.fill(WHITE)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    inventory.update(events)
    inventory.render()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
