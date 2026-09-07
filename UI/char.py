import pygame
import pygame.freetype
import sys
from UI.pause import pause_window
from .assets import load_font, load_image, load_sound, media_path

pygame.init()
pygame.font.init()
pygame.mixer.init()


class Character:
    """Username entry and avatar selection before starting a run."""

    def __init__(self, screen):
        """Load avatars, frames, continue/quit controls, fonts, and input box state."""
        self.clock = pygame.time.Clock()
        self.screen = screen
        c1_path = media_path("Game Assets", "Characters", "c1.png")
        c2_path = media_path("Game Assets", "Characters", "c2.png")
        c3_path = media_path("Game Assets", "Characters", "c3.png")
        c4_path = media_path("Game Assets", "Characters", "c4.png")
        self.avatar_paths = [str(p) if p else "" for p in (c1_path, c2_path, c3_path, c4_path)]
        self.button_sound = load_sound("Sound Effect", "button.mp3")
        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)
        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.c1 = load_image("Game Assets", "Characters", "c1.png", size=(80, 80), label="C1")
        self.c2 = load_image("Game Assets", "Characters", "c2.png", size=(80, 80), label="C2")
        self.c3 = load_image("Game Assets", "Characters", "c3.png", size=(80, 80), label="C3")
        self.c4 = load_image("Game Assets", "Characters", "c4.png", size=(80, 80), label="C4")
        self.frame_select = load_image("Game Assets", "frame_select.png", size=(120, 140), label="")
        self.frame_continue = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_continue_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_continue_rect = self.frame_continue.get_rect(topleft=(900, 700))
        self.continue_text = load_image("Game Assets", "CONTINUE.png", size=(180, 50), label="CONTINUE")
        self.continue_pressed = load_image("Game Assets", "CONTINUE_pressed.png", size=(180, 50), label="CONTINUE")
        self.continue_rect = self.continue_text.get_rect(topleft=(920, 710))
        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright=(1190, 10))
        self.frame = load_image("Game Assets", "frame_char.png", size=(120, 140), label="")
        self.frame_pressed = load_image("Game Assets", "frame_char_pressed.png", size=(120, 140), label="")
        self.frame1_rect = self.frame.get_rect(topleft=(300, 450))
        self.frame2_rect = self.frame.get_rect(topleft=(460, 450))
        self.frame3_rect = self.frame.get_rect(topleft=(640, 450))
        self.frame4_rect = self.frame.get_rect(topleft=(800, 450))
        self.font = load_font(50)
        self.input_box = pygame.Rect(300, 200, 600, 70)
        self.color_active = pygame.Color("lightskyblue3")
        self.color_inactive = pygame.Color("gray15")
        self.color = self.color_inactive
        self.text = ""
        self.warning_text = ""
        self.active = False
        self.selected_idx = 0
        self.rect = self.frame.get_rect(topleft=(300, 450))
        self.current_frame_continue = self.frame_continue
        self.current_continue = self.continue_text

    def update(self, events) -> str:
        """Return ``START`` with valid name on continue, ``QUIT`` for pause, or ``CHAR`` while editing."""
        mouse_pos = pygame.mouse.get_pos()
        current_frames = [
            self.frame_pressed if self.frame1_rect.collidepoint(mouse_pos) else self.frame,
            self.frame_pressed if self.frame2_rect.collidepoint(mouse_pos) else self.frame,
            self.frame_pressed if self.frame3_rect.collidepoint(mouse_pos) else self.frame,
            self.frame_pressed if self.frame4_rect.collidepoint(mouse_pos) else self.frame,
        ]
        self.current_frame1, self.current_frame2, self.current_frame3, self.current_frame4 = current_frames
        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_frame_continue = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_frame_continue = self.frame_continue
            self.current_continue = self.continue_text
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.input_box.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive
                if self.frame1_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.selected_idx = 0
                elif self.frame2_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.selected_idx = 1
                elif self.frame3_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.selected_idx = 2
                elif self.frame4_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.selected_idx = 3
                self.rect = self.frame.get_rect(topleft=[(300, 450), (460, 450), (640, 450), (800, 450)][self.selected_idx])
                if self.frame_continue_rect.collidepoint(event.pos):
                    if self.text.strip():
                        self.button_sound.play()
                        self.warning_text = ""
                        return "START"
                    self.warning_text = "Error: please enter your username."
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return "QUIT"
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) <= 10 and event.unicode.isprintable():
                    self.text += event.unicode
                if self.text.strip():
                    self.warning_text = ""
        return "CHAR"

    def draw(self):
        """Draw background, username field, avatar grid, selection cursor, and continue/quit."""
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)
        self.font.render_to(self.screen, (300, 150), "Username:", (255, 255, 255))
        self.font.render_to(self.screen, (self.input_box.x + 5, self.input_box.y + 5), self.text, (255, 255, 255))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        if not self.text.strip() and self.warning_text:
            self.font.render_to(self.screen, (300, self.input_box.bottom + 10), self.warning_text, (255, 80, 80), size=24)
        self.font.render_to(self.screen, (340, 380), "Choose your Character!", (255, 255, 255))
        self.screen.blit(self.current_frame1, self.frame1_rect)
        self.screen.blit(self.current_frame2, self.frame2_rect)
        self.screen.blit(self.current_frame3, self.frame3_rect)
        self.screen.blit(self.current_frame4, self.frame4_rect)
        self.screen.blit(self.frame_select, self.rect)
        self.screen.blit(self.c1, (325, 490))
        self.screen.blit(self.c2, (485, 490))
        self.screen.blit(self.c3, (665, 490))
        self.screen.blit(self.c4, (825, 490))
        self.screen.blit(self.current_frame_continue, self.frame_continue_rect)
        self.screen.blit(self.current_continue, self.continue_rect)

    def run(self):
        """Standalone loop with optional quit confirmation modal; returns ``(name, avatar_path)`` on start."""
        confirm_quit = False
        modal = pause_window(self.screen)
        while True:
            events = pygame.event.get()
            if confirm_quit:
                for event in events:
                    choice = modal.update([event], 3)
                    if choice == 0:
                        pygame.quit(); sys.exit()
                    if choice == 3:
                        confirm_quit = False
                self.draw(); modal.draw(); pygame.display.flip(); self.clock.tick(60); continue
            for event in events:
                if event.type == pygame.QUIT:
                    confirm_quit = True
                    break
            if confirm_quit:
                self.draw(); modal.draw(); pygame.display.flip(); self.clock.tick(60); continue
            action = self.update(events)
            if action == "QUIT":
                confirm_quit = True
            elif action == "START":
                return self.text.strip(), self.avatar_paths[self.selected_idx]
            self.draw(); pygame.display.flip(); self.clock.tick(60)
