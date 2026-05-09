import pygame
import pygame.freetype
from pathlib import Path
import Text_wrapper

pygame.init()
pygame.font.init()

class Guidelines:
    def __init__(self, screen, filename):
        with open(filename, "r") as f:
            self.text = f.readlines()

        self.text_rect0 = pygame.Rect(50, 50, 1100, 30)
        self.text_rect1 = pygame.Rect(50, 80, 1100, 30)
        self.text_rect2 = pygame.Rect(50, 110, 1100, 30)
        self.text_rect3 = pygame.Rect(50, 140, 1100, 30)
        self.text_rect4 = pygame.Rect(50, 170, 1100, 50)
        self.text_rect5 = pygame.Rect(50, 220, 1100, 30)
        self.text_rect6 = pygame.Rect(50, 250, 1100, 50)
        self.text_rect7 = pygame.Rect(50, 300, 1100, 30)
        self.text_rect8 = pygame.Rect(50, 330, 1100, 70)
        self.text_rect9 = pygame.Rect(50, 400, 1100, 50)
        self.text_rect10 = pygame.Rect(50, 450, 1100, 50)
        
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(150)
        
        current_dir = Path(__file__).parent
        bg_path = current_dir / "Game Assets" / "bg.png"
        frame_return_path = current_dir / "Game Assets" / "button.png"
        frame_return_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        return_path = current_dir / "Game Assets" / "RETURN.png"
        return_pressed_path = current_dir / "Game Assets" / "RETURN_pressed.png"
        prev_path = current_dir / "Game Assets" / "prev_grey.png"
        next_path = current_dir / "Game Assets" / "next.png"

        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.button = pygame.image.load(str(frame_return_path)).convert_alpha()
        self.button_pressed = pygame.image.load(str(frame_return_pressed_path)).convert_alpha()
        self.button_rect = self.button.get_rect(center = (1030, 730))
        self.return_text = pygame.image.load(str(return_path)).convert_alpha()
        self.return_pressed = pygame.image.load(str(return_pressed_path)).convert_alpha()
        self.return_rect = self.return_text.get_rect(center = (1030, 730))

        self.prev = pygame.image.load(str(prev_path)).convert_alpha()
        self.next = pygame.image.load(str(next_path)).convert_alpha()
        self.next_rect = self.next.get_rect(topleft = (650, 600))

        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 20)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.current_button = self.button_pressed
            self.current_return = self.return_pressed
        else:
            self.current_button = self.button
            self.current_return = self.return_text

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    return 3
                if self.next_rect.collidepoint(event.pos):
                    return 2
                
        return 1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        
        Text_wrapper.draw_wrapped_text(self.screen, self.text[0], self.font, (255, 255, 255), self.text_rect0)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[1], self.font, (255, 255, 255), self.text_rect1)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[2], self.font, (255, 255, 255), self.text_rect2)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[3], self.font, (255, 255, 255), self.text_rect3)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[4], self.font, (255, 255, 255), self.text_rect4)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[5], self.font, (255, 255, 255), self.text_rect5)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[6], self.font, (255, 255, 255), self.text_rect6)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[7], self.font, (255, 255, 255), self.text_rect7)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[8], self.font, (255, 255, 255), self.text_rect8)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[9], self.font, (255, 255, 255), self.text_rect9)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[10], self.font, (255, 255, 255), self.text_rect10)

        self.screen.blit(self.current_button, self.button_rect)
        self.screen.blit(self.current_return, self.return_rect)

        self.screen.blit(self.next, self.next_rect)
        self.screen.blit(self.prev, (550, 600))

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Guidelines(screen, Path(__file__).parent / "Guideline.txt")
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