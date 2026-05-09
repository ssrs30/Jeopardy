import pygame
import pygame.freetype
from pathlib import Path
import Text_wrapper
import threading

pygame.init()
pygame.font.init()
pygame.mixer.init()

class GetReady:
    def __init__(self, screen, round_no):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        current_dir = Path(__file__).parent
        bg_path = current_dir / "Game Assets" / "bg.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        frame_player_path = current_dir / "Game Assets" / "frame_player.png"
        frame_continue_path = current_dir / "Game Assets" / "button.png"
        frame_continue_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        continue_text_path = current_dir / "Game Assets" / "CONTINUE.png"
        continue_pressed_path = current_dir / "Game Assets" / "CONTINUE_pressed.png"
        items_path = current_dir / "Game Assets" / "ITEMS.png"
        items_pressed_path = current_dir / "Game Assets" / "ITEMS_pressed.png"
        shop_path = current_dir / "Game Assets" / "SHOP.png"
        shop_pressed_path = current_dir / "Game Assets" / "SHOP_pressed.png"
        top_button_path = current_dir / "Game Assets" / "top_button.png"
        top_button_pressed_path = current_dir / "Game Assets" / "top_button_pressed.png"

        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.frame_player = pygame.image.load(str(frame_player_path)).convert_alpha()

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

        self.text = f"Get Ready for Round{round_no}!"
        self.text_rect = pygame.Rect(600, 300, 800, 250)
        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 100)

        self.ready = False
        self.thread_start = False

    def _countdown(self):
        threading.Timer(3.0, self._change_state()).start()
    
    def _change_state(self):
        self.ready = True
    
    def update(self, events):
        if not self.thread_start:

            self._countdown()
            self.thread_start = True
        
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
                if self.quit_button_rect.collidepoint(event.pos):
                    return 2
                if self.frame_continue_rect.collidepoint(event.pos):
                    return 4
                if self.top_button_items_rect.collidepoint(event.pos):
                    return 2
                if self.top_button_shop_rect.collidepoint(event.pos):
                    return 2
                
        return 1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        if self.ready:
            self.screen.blit(self.current_button, self.frame_continue_rect)
            self.screen.blit(self.current_continue, self.continue_rect)

        Text_wrapper.draw_wrapped_text(self.screen, self.text, self.font, (255, 255, 255), self.text_rect, True)

        """self.screen.blit(self.frame_player, (440, 320))
        self.screen.blit(self.frame_player, (200, 450))
        self.screen.blit(self.frame_player, (680, 450))"""




if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = GetReady(screen, 2)
    clock = pygame.time.Clock()
    num = 1
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 1:
            num = window.update(events)
            window.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()