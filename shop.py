import pygame
import pygame.freetype
from pathlib import Path

pygame.init()
pygame.font.init()

class Shop:
    def __init__(self, screen):
        self.screen = screen

        current_dir = Path(__file__).parent
        frame_path = current_dir / "Game Assets" / "frame_player.png"
        frame_pressed_path = current_dir / "Game Assets" / "frame_player_pressed.png"
        shop_title_path = current_dir / "Game Assets" / "SHOP_title.png"
        frame_return_path = current_dir / "Game Assets" / "button.png"
        frame_return_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        return_text_path = current_dir / "Game Assets" / "RETURN.png"
        return_pressed_path = current_dir / "Game Assets" / "RETURN_pressed.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        items_path = current_dir / "Game Assets" / "ITEMS.png"
        items_pressed_path = current_dir / "Game Assets" / "ITEMS_pressed.png"
        shop_path = current_dir / "Game Assets" / "SHOP.png"
        shop_pressed_path = current_dir / "Game Assets" / "SHOP_pressed.png"
        top_button_path = current_dir / "Game Assets" / "top_button.png"
        top_button_pressed_path = current_dir / "Game Assets" / "top_button_pressed.png"
        icon1_path = current_dir / "Game Assets" / "shop_icon1.png"
        icon2_path = current_dir / "Game Assets" / "shop_icon2.png"
        icon3_path = current_dir / "Game Assets" / "shop_icon3.png"
        icon4_path = current_dir / "Game Assets" / "shop_icon4.png"

        self.frame = pygame.image.load(str(frame_path)).convert_alpha()
        self.frame_pressed = pygame.image.load(str(frame_pressed_path)).convert_alpha()
        self.frame_rect1 = self.frame.get_rect(topleft = (200, 300))
        self.frame_rect2 = self.frame.get_rect(topleft = (650, 300))
        self.frame_rect3 = self.frame.get_rect(topleft = (200, 500))
        self.frame_rect4 = self.frame.get_rect(topleft = (650, 500))
        self.shop_title = pygame.image.load(str(shop_title_path)).convert_alpha()

        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.frame_return = pygame.image.load(str(frame_return_path)).convert_alpha()
        self.frame_return_pressed = pygame.image.load(str(frame_return_pressed_path)).convert_alpha()
        self.frame_return_rect = self.frame_return.get_rect(center = (600, 700))

        self.return_text = pygame.image.load(str(return_text_path)).convert_alpha()
        self.return_pressed = pygame.image.load(str(return_pressed_path)).convert_alpha()
        self.return_rect = self.return_text.get_rect(center = (600, 700))

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

        self.icon1 = pygame.image.load(str(icon1_path)).convert_alpha()        
        self.icon2 = pygame.image.load(str(icon2_path)).convert_alpha()        
        self.icon3 = pygame.image.load(str(icon3_path)).convert_alpha()        
        self.icon4 = pygame.image.load(str(icon4_path)).convert_alpha()

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()

        if self.frame_return_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_return_pressed
            self.current_return = self.return_pressed
        else:
            self.current_button = self.frame_return
            self.current_return = self.return_text

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

        self.current_frame1 = self.frame_pressed if self.frame_rect1.collidepoint(mouse_pos) else self.frame
        self.current_frame2 = self.frame_pressed if self.frame_rect2.collidepoint(mouse_pos) else self.frame
        self.current_frame3 = self.frame_pressed if self.frame_rect3.collidepoint(mouse_pos) else self.frame
        self.current_frame4 = self.frame_pressed if self.frame_rect4.collidepoint(mouse_pos) else self.frame

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame_return_rect.collidepoint(event.pos):
                    return 2
                if self.top_button_items_rect.collidepoint(event.pos):
                    return 2
                if self.top_button_shop_rect.collidepoint(event.pos):
                    return 2
                if self.quit_button_rect.collidepoint(event.pos):
                    return 2
        
        return 1

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.quit_button, self.quit_button_rect)
        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)
        self.screen.blit(self.current_button, self.frame_return_rect)
        self.screen.blit(self.current_return, self.return_rect)

        self.screen.blit(self.shop_title, (400, 100))

        self.screen.blit(self.current_frame1, self.frame_rect1)
        self.screen.blit(self.current_frame2, self.frame_rect2)
        self.screen.blit(self.current_frame3, self.frame_rect3)
        self.screen.blit(self.current_frame4, self.frame_rect4)

        self.screen.blit(self.icon1, (240, 340))
        self.screen.blit(self.icon2, (690, 340))
        self.screen.blit(self.icon3, (240, 540))
        self.screen.blit(self.icon4, (690, 543))


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Shop(screen)
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