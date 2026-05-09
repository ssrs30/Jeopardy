import pygame
import pygame.freetype
from pathlib import Path
import Text_wrapper

pygame.init()
pygame.font.init()

class dailydouble:
    def __init__(self, screen):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        current_dir = Path(__file__).parent
        frame_continue_path = current_dir / "Game Assets" / "button.png"
        frame_continue_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        continue_text_path = current_dir / "Game Assets" / "CONTINUE.png"
        continue_pressed_path = current_dir / "Game Assets" / "CONTINUE_pressed.png"
        frame_player_path = current_dir / "Game Assets" / "frame_player.png"
        frame_AI_path = current_dir / "Game Assets" / "frame_AI.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        items_path = current_dir / "Game Assets" / "ITEMS.png"
        items_pressed_path = current_dir / "Game Assets" / "ITEMS_pressed.png"
        shop_path = current_dir / "Game Assets" / "SHOP.png"
        shop_pressed_path = current_dir / "Game Assets" / "SHOP_pressed.png"
        top_button_path = current_dir / "Game Assets" / "top_button.png"
        top_button_pressed_path = current_dir / "Game Assets" / "top_button_pressed.png"

        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 50)
        self.font_warning = pygame.freetype.Font(current_dir / "Pix32.ttf", 32)
        self.title = "YOU FOUND A DAILY DOUBLE!"
        self.wager_text = "YOUR WAGER:"

        self.frame_player = pygame.image.load(str(frame_player_path)).convert_alpha()
        self.frame_AI = pygame.image.load(str(frame_AI_path)).convert_alpha()

        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.frame_continue = pygame.image.load(str(frame_continue_path)).convert_alpha()
        self.frame_continue_pressed = pygame.image.load(str(frame_continue_pressed_path)).convert_alpha()
        self.frame_continue_rect = self.frame_continue.get_rect(center = (600, 700))

        self.continue_text = pygame.image.load(str(continue_text_path)).convert_alpha()
        self.continue_pressed = pygame.image.load(str(continue_pressed_path)).convert_alpha()
        self.continue_rect = self.continue_text.get_rect(center = (600, 700))

        self.items = pygame.image.load(str(items_path)).convert_alpha()
        self.items_pressed = pygame.image.load(str(items_pressed_path)).convert_alpha()
        self.items_rect = self.items.get_rect(center = (1050, 50))

        self.shop = pygame.image.load(str(shop_path)).convert_alpha()
        self.shop_pressed = pygame.image.load(str(shop_pressed_path)).convert_alpha()
        self.shop_rect = self.shop.get_rect(center = (875, 50))

        self.top_button = pygame.image.load(str(top_button_path)).convert_alpha()
        self.top_button_pressed = pygame.image.load(str(top_button_pressed_path)).convert_alpha()
        self.top_button_items_rect = self.top_button.get_rect(center = (1050, 50))
        self.top_button_shop_rect = self.top_button.get_rect(center = (875, 50))

        self.current_warning = ""
        self.warning_text1 = "Error: invalid value. Please input integers only."
        self.warning_text2 = "Error: value is out of range. Your wager should be between 0 and your current score"
        self.warning_rect = pygame.Rect(300, 450, 600, 100)

        self.input_box = pygame.Rect(300, 400, 600, 50)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_inactive = pygame.Color('gray15')
        self.color = self.color_inactive

        self.text = ''
        self.active = False

    def update(self, events, score):
        mouse_pos = pygame.mouse.get_pos()
        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_button = self.frame_continue
            self.current_continue = self.continue_text

        if self.top_button_items_rect.collidepoint(mouse_pos):
            self.current_top_button_items = self.top_button_pressed
            self.current_items = self.items_pressed
        else:
            self.current_top_button_items = self.top_button
            self.current_items = self.items
        
        if self.top_button_shop_rect.collidepoint(mouse_pos):
            self.current_top_button_shop = self.top_button_pressed
            self.current_shop = self.shop_pressed
        else:
            self.current_top_button_shop = self.top_button
            self.current_shop = self.shop
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user clicked on the input_box rect
                self.active = self.input_box.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive

                if self.frame_continue_rect.collidepoint(event.pos):
                    try:
                        num = int(self.text)
                        if num >= 0 and num <= score:
                            return 2, int(self.text)
                        else:
                            self.current_warning = self.warning_text2
                    except ValueError:
                        self.current_warning = self.warning_text1
                if self.top_button_items_rect.collidepoint(event.pos):
                    return 2, 0
                if self.top_button_shop_rect.collidepoint(event.pos):
                    return 2, 0
                if self.quit_button_rect.collidepoint(event.pos):
                    return 2, 0
                    
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 20:
                        self.text += event.unicode
        
        return 1, 0
    
    def update_character(self, char_path):
        self.char = pygame.image.load(str(char_path)).convert_alpha()

    def draw(self):
        self.screen.blit(self.dark_surface, (0, 0))

        self.screen.blit(self.frame_player, (15, 10))
        self.screen.blit(self.frame_AI, (350, 20))
        self.screen.blit(self.frame_AI, (350, 80))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        self.title_surf, self.title_rect = self.font.render(self.title, (255, 255, 255))
        self.title_rect.center = (600, 250)
        self.screen.blit(self.title_surf, self.title_rect)
        
        self.font.render_to(self.screen, (300, 350), self.wager_text, (255, 255, 255))
        self.font.render_to(self.screen,(self.input_box.x+5, self.input_box.y+5) ,self.text, (255, 255, 255))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

        self.screen.blit(self.current_button, self.frame_continue_rect)
        self.screen.blit(self.current_continue, self.continue_rect)
        
        Text_wrapper.draw_wrapped_text(self.screen, self.current_warning, self.font_warning, (250, 150, 150), self.warning_rect)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = dailydouble(screen)
    clock = pygame.time.Clock()
    num = 1
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 1:
            num, wager = window.update(events, 1000)
            window.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()