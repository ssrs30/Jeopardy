import pygame
from pathlib import Path

pygame.init()

class pause_window:
    def __init__(self, screen):
        self.screen = screen
        
        current_dir = Path(__file__).parent
        quit_frame_path = current_dir / "Game Assets" / "quit_frame.png"
        quitting_path = current_dir / "Game Assets" / "QUITTING.png"
        button_path = current_dir / "Game Assets" / "button.png"
        button_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        yes_path = current_dir / "Game Assets" / "YES.png"
        no_path = current_dir / "Game Assets" / "NO.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"

        button_sound_path = current_dir / "Sound Effect" / "button.mp3"
        self.button_sound = pygame.mixer.Sound(button_sound_path)

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        self.quit_frame = pygame.image.load(str(quit_frame_path)).convert_alpha()
        self.quitting = pygame.image.load(str(quitting_path)).convert_alpha()
        self.yes = pygame.image.load(str(yes_path)).convert_alpha()
        self.no = pygame.image.load(str(no_path)).convert_alpha()

        self.button = pygame.image.load(str(button_path)).convert_alpha()
        self.button_pressed = pygame.image.load(str(button_pressed_path)).convert_alpha()
        self.buttonL_rect = self.button.get_rect(topleft = (360, 400))
        self.buttonR_rect = self.button.get_rect(topleft = (640, 400))

        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        
    def update(self, events, num) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.buttonL_rect.collidepoint(mouse_pos):
            self.current_buttonL = self.button_pressed
        else:
            self.current_buttonL = self.button
    
        if self.buttonR_rect.collidepoint(mouse_pos):
            self.current_buttonR = self.button_pressed
        else:
            self.current_buttonR = self.button

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return 0
                elif event.key == pygame.K_ESCAPE:
                    self.button_sound.play()
                    return num
                elif event.key == pygame.K_n:
                    self.button_sound.play()
                    return num
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonL_rect.collidepoint(event.pos):
                    return 0
                elif self.buttonR_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return num
                elif self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return num
        return 2

    def draw(self):    
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)
        self.screen.blit(self.quit_frame, (300, 250))
        self.screen.blit(self.quitting, (400, 310))
        self.screen.blit(self.current_buttonL, self.buttonL_rect)
        self.screen.blit(self.yes, (420, 405))
        self.screen.blit(self.current_buttonR, self.buttonR_rect)
        self.screen.blit(self.no, (710, 405))

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = pause_window(screen)
    clock = pygame.time.Clock()
    num = 2
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 2:
            num = window.update(events, 1)
            window.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()