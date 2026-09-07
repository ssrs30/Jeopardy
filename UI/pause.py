import pygame

from .assets import load_image, load_sound

pygame.init()


class pause_window:

    def __init__(self, screen):
        self.screen = screen
        self.button_sound = load_sound("Sound Effect", "button.mp3")

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)
        self.quit_frame = load_image("Game Assets", "quit_frame.png", size=(600, 280), label="")
        self.quitting = load_image("Game Assets", "QUITTING.png", size=(360, 80), label="QUIT?")
        self.yes = load_image("Game Assets", "YES.png", size=(140, 50), label="YES")
        self.no = load_image("Game Assets", "NO.png", size=(140, 50), label="NO")
        self.button = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.button_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.buttonL_rect = self.button.get_rect(topleft=(360, 400))
        self.buttonR_rect = self.button.get_rect(topleft=(640, 400))
        self.current_buttonL = self.button
        self.current_buttonR = self.button
        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright=(1190, 10))

    def update(self, events, num) -> int:
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()
        self.current_buttonL = self.button_pressed if self.buttonL_rect.collidepoint(mouse_pos) else self.button
        self.current_buttonR = self.button_pressed if self.buttonR_rect.collidepoint(mouse_pos) else self.button
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonL_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 0
                if self.buttonR_rect.collidepoint(event.pos) or self.quit_button_rect.collidepoint(event.pos):
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
