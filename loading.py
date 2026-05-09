import pygame
from pathlib import Path
import time
import threading
import LLM

pygame.init()

class loading:
    def __init__(self, screen):
        self.screen = screen
        
        current_dir = Path(__file__).parent
        loading1_path = current_dir / "Game Assets" / "LOADING1.png"
        loading2_path = current_dir / "Game Assets" / "LOADING2.png"
        loading3_path = current_dir / "Game Assets" / "LOADING3.png"
        continue_img = current_dir / "Game Assets" / "CONTINUE.png"
        button = current_dir / "Game Assets" / "button.png"
        button_pressed = current_dir / "Game Assets" / "button_pressed.png"

        loading1 = pygame.image.load(str(loading1_path)).convert_alpha()
        loading2 = pygame.image.load(str(loading2_path)).convert_alpha()
        loading3 = pygame.image.load(str(loading3_path)).convert_alpha()
        self.continue_img = pygame.image.load(str(continue_img)).convert_alpha()
        self.loading = [loading1, loading2, loading3]
        self.loading_rect = loading1.get_rect(center = (600, 400))
        self.button = pygame.image.load(str(button)).convert_alpha()
        self.button_pressed = pygame.image.load(str(button_pressed)).convert_alpha()
        self.button_rect = self.button.get_rect(center = (600, 400))

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 500  # Milliseconds between image swaps

    def update(self, events, data_ready) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if not data_ready:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.loading)

            self.current_img = self.loading[self.current_frame]
            self.current_button = pygame.Surface((200, 54))
        else:
            self.current_img = self.continue_img
            self.loading_rect = self.continue_img.get_rect(center = (600, 400))

            if self.button_rect.collidepoint(mouse_pos):
                self.current_button = self.button_pressed
            else:
                self.current_button = self.button

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        return 1

        return 5

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.current_button, self.button_rect)
        self.screen.blit(self.current_img, self.loading_rect)
        

if __name__ == "__main__":
    data_ready = False
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    window = loading(screen)

    def load():
        questions = LLM.q_generate(LLM.prompt)
        global data_ready
        data_ready = True

    threading.Thread(target=load, daemon=True).start()
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        num = 5
        if num == 5:
            num = window.update(events, data_ready)
            window.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()