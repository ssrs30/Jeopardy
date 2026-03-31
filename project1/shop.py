import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
DARK_BLUE = (30, 30, 60)

class Shop:
    def __init__(self, screen, player):
        """
        Initialize the Shop with the game screen and player instance.
        The player instance is used to manage coins and inventory.
        """
        self.screen = screen
        self.player = player
        self.font_m = pygame.font.Font(None, 36)
        self.font_s = pygame.font.Font(None, 24)
        
        self.items = [
            {"id": "skip", "name": "Skip Card", "price": 500, "desc": "Skip one question safely", "rect": pygame.Rect(100, 150, 280, 100)},
            {"id": "fifty_fifty", "name": "50/50", "price": 300, "desc": "Remove 2 wrong options", "rect": pygame.Rect(420, 150, 280, 100)},
            {"id": "shield", "name": "Point Shield", "price": 400, "desc": "No penalty for wrong answer", "rect": pygame.Rect(100, 280, 280, 100)},
            {"id": "double", "name": "Double Chance", "price": 600, "desc": "Two attempts for one question", "rect": pygame.Rect(420, 280, 280, 100)}
        ]
        
        self.exit_button = pygame.Rect(325, 480, 150, 50)
        self.message = ""
        self.msg_timer = 0

    def draw(self):
        """Draw the Shop UI components"""
        self.screen.fill(DARK_BLUE)
        
        # 1. Draw Header
        title = self.font_m.render("GAME SHOP", True, GOLD)
        self.screen.blit(title, (400 - title.get_width()//2, 40))
        
        # 2. Display Player Stats (Coins & Inventory)
        coin_txt = self.font_m.render(f"Your Coins: {self.player.coins}", True, WHITE)
        self.screen.blit(coin_txt, (50, 90))
        
        inv_txt = self.font_s.render(
            f"Inventory -> Skip: {self.player.inventory.get('skips', 0)} | "
            f"50/50: {self.player.inventory.get('fifty_fifty', 0)} | "
            f"Shield: {self.player.inventory.get('shields', 0)}", 
            True, GRAY
        )
        self.screen.blit(inv_txt, (50, 120))

        # 3. Draw Item Cards
        for item in self.items:
            # Draw card background
            pygame.draw.rect(self.screen, BLUE, item["rect"], border_radius=10)
            pygame.draw.rect(self.screen, WHITE, item["rect"], 2, border_radius=10)
            
            # Item Name & Price
            name_surf = self.font_m.render(item["name"], True, WHITE)
            price_surf = self.font_m.render(f"${item['price']}", True, GOLD)
            desc_surf = self.font_s.render(item["desc"], True, GRAY)
            
            self.screen.blit(name_surf, (item["rect"].x + 15, item["rect"].y + 15))
            self.screen.blit(price_surf, (item["rect"].x + 200, item["rect"].y + 15))
            self.screen.blit(desc_surf, (item["rect"].x + 15, item["rect"].y + 60))

        # 4. Draw Exit Button
        pygame.draw.rect(self.screen, PURPLE, self.exit_button, border_radius=5)
        exit_txt = self.font_m.render("EXIT", True, WHITE)
        self.screen.blit(exit_txt, (self.exit_button.centerx - exit_txt.get_width()//2, self.exit_button.centery - exit_txt.get_height()//2))

        # 5. Display Feedback Message (e.g., "Not enough coins")
        if self.msg_timer > 0:
            msg_surf = self.font_s.render(self.message, True, GOLD)
            self.screen.blit(msg_surf, (400 - msg_surf.get_width()//2, 440))
            self.msg_timer -= 1

    def handle_click(self, pos):
        """Process click events for purchasing items or exiting"""
        # Check Exit button
        if self.exit_button.collidepoint(pos):
            return "EXIT"

        # Check Item buttons
        for item in self.items:
            if item["rect"].collidepoint(pos):
                if self.player.coins >= item["price"]:
                    self.player.coins -= item["price"]
                    self.update_inventory(item["id"])
                    self.message = f"Purchased {item['name']}!"
                    self.msg_timer = 90 # Show message for 1.5 seconds
                else:
                    self.message = "Not enough coins!"
                    self.msg_timer = 90
        return None

    def update_inventory(self, item_id):
        """Map item IDs to player inventory keys"""
        if item_id == "skip":
            self.player.inventory["skips"] = self.player.inventory.get("skips", 0) + 1
        elif item_id == "fifty_fifty":
            self.player.inventory["fifty_fifty"] = self.player.inventory.get("fifty_fifty", 0) + 1
        elif item_id == "shield":
            self.player.inventory["shields"] = self.player.inventory.get("shields", 0) + 1
        elif item_id == "double":
            self.player.inventory["double_chance"] = self.player.inventory.get("double_chance", 0) + 1

