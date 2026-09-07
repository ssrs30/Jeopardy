import pygame

from .assets import load_image

pygame.init()

class loading:

    def __init__(self, screen):
        self.screen = screen
        loading1 = load_image("Game Assets", "LOADING1.png", size=(360, 120), label="LOADING")
        loading2 = load_image("Game Assets", "LOADING2.png", size=(360, 120), label="LOADING")
        loading3 = load_image("Game Assets", "LOADING3.png", size=(360, 120), label="LOADING")
        self.continue_img = load_image("Game Assets", "CONTINUE.png", size=(220, 70), label="CONTINUE")
        self.loading = [loading1, loading2, loading3]
        self.loading_rect = loading1.get_rect(center = (600, 400))
        self.default_center = (600, 400)
        self.button = load_image("Game Assets", "button.png", size=(280, 92), label="")
        self.button_pressed = load_image("Game Assets", "button_pressed.png", size=(280, 92), label="")
        self.button_rect = self.button.get_rect(center = (600, 400))

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 500  # Milliseconds between image swaps
        self._hint_font = pygame.font.Font(None, 30)

    def update(self, events, data_ready, generation_failed: bool = False) -> int:
        """handle clicks and hover"""
        mouse_pos = pygame.mouse.get_pos()
        if generation_failed:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.loading)
            self.current_img = self.loading[self.current_frame]
            self.loading_rect = self.current_img.get_rect(center=self.default_center)
            self.current_button = pygame.Surface((200, 54))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return 6
            return 5

        if not data_ready:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.loading)

            self.current_img = self.loading[self.current_frame]
            self.loading_rect = self.current_img.get_rect(center=self.default_center)
            self.current_button = pygame.Surface((200, 54))
        else:
            self.current_img = self.continue_img
            self.loading_rect = self.continue_img.get_rect(center=self.default_center)

            if self.button_rect.collidepoint(mouse_pos):
                self.current_button = self.button_pressed
            else:
                self.current_button = self.button

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        return 1

        return 5

    def draw(self, generation_failed: bool = False):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.current_button, self.button_rect)
        self.screen.blit(self.current_img, self.loading_rect)
        if generation_failed:
            title = self._hint_font.render("Could not load questions", True, (255, 90, 90))
            hint = self._hint_font.render("Press R to retry, or add a key in API.env", True, (230, 230, 230))
            tr = title.get_rect(center=(600, 720))
            hr = hint.get_rect(center=(600, 755))
            self.screen.blit(title, tr)
            self.screen.blit(hint, hr)
        
