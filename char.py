import pygame
import pygame.freetype
from pathlib import Path

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Character:
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.screen = screen

        current_dir = Path(__file__).parent
        bg_path = current_dir / "Game Assets" / "bg.png"
        c1_path = current_dir / "Game Assets" / "Characters" / "c1.png"
        c2_path = current_dir / "Game Assets" / "Characters" / "c2.png"
        c3_path = current_dir / "Game Assets" / "Characters" / "c3.png"
        c4_path = current_dir / "Game Assets" / "Characters" / "c4.png"
        frame_path = current_dir / "Game Assets" / "frame_char.png"
        frame_pressed_path = current_dir / "Game Assets" / "frame_char_pressed.png"
        frame_select_path = current_dir / "Game Assets" / "frame_select.png"
        frame_continue_path = current_dir / "Game Assets" / "button.png"
        frame_continue_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        continue_text_path = current_dir / "Game Assets" / "CONTINUE.png"
        continue_pressed_path = current_dir / "Game Assets" / "CONTINUE_pressed.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"

        self.menu_BGM_path = current_dir / "Sound Effect" / "menu_BGM.mp3"
        button_sound_path = current_dir / "Sound Effect" / "button.mp3"
        self.button_sound = pygame.mixer.Sound(button_sound_path)

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.c1 = pygame.image.load(str(c1_path)).convert_alpha()
        self.c2 = pygame.image.load(str(c2_path)).convert_alpha()
        self.c3 = pygame.image.load(str(c3_path)).convert_alpha()
        self.c4 = pygame.image.load(str(c4_path)).convert_alpha()
        self.frame_select = pygame.image.load(str(frame_select_path)).convert_alpha()

        self.frame_continue = pygame.image.load(str(frame_continue_path)).convert_alpha()
        self.frame_continue_pressed = pygame.image.load(str(frame_continue_pressed_path)).convert_alpha()
        self.frame_continue_rect = self.frame_continue.get_rect(topleft = (900, 700))

        self.continue_text = pygame.image.load(str(continue_text_path)).convert_alpha()
        self.continue_pressed = pygame.image.load(str(continue_pressed_path)).convert_alpha()
        self.continue_rect = self.continue_text.get_rect(topleft = (920, 710))

        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topleft = (10, 10))
        
        self.frame = pygame.image.load(str(frame_path)).convert_alpha()
        self.frame_pressed = pygame.image.load(str(frame_pressed_path)).convert_alpha()
        self.frame1_rect = self.frame.get_rect(topleft = (300, 450))
        self.frame2_rect = self.frame.get_rect(topleft = (460, 450))
        self.frame3_rect = self.frame.get_rect(topleft = (640, 450))
        self.frame4_rect = self.frame.get_rect(topleft = (800, 450))

        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 50)
        self.title = "Choose your Character!"
        self.name = "Username:"

        self.input_box = pygame.Rect(300, 200, 600, 70)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_inactive = pygame.Color('gray15')
        self.color = self.color_inactive

        self.text = ''
        self.active = False

        self.pos = (300, 450)
        self.rect = self.frame.get_rect(topleft = self.pos)

        self.music_started = False

    def update(self, events) -> int:
        if not self.music_started:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load(self.menu_BGM_path)
            pygame.mixer.music.play(-1)
            self.music_started = True
        
        mouse_pos = pygame.mouse.get_pos()

        if self.frame1_rect.collidepoint(mouse_pos):
            self.current_frame1 = self.frame_pressed
        else:
            self.current_frame1 = self.frame

        if self.frame2_rect.collidepoint(mouse_pos):
            self.current_frame2 = self.frame_pressed
        else:
            self.current_frame2 = self.frame

        if self.frame3_rect.collidepoint(mouse_pos):
            self.current_frame3 = self.frame_pressed
        else:
            self.current_frame3 = self.frame

        if self.frame4_rect.collidepoint(mouse_pos):
            self.current_frame4 = self.frame_pressed
        else:
            self.current_frame4 = self.frame

        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_frame_continue = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_frame_continue = self.frame_continue
            self.current_continue = self.continue_text

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user clicked on the input_box rect
                self.active = self.input_box.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive
                
                if self.frame1_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.pos = (300, 450)
                    self.rect = self.frame.get_rect(topleft = self.pos)
                elif self.frame2_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.pos = (460, 450)
                    self.rect = self.frame.get_rect(topleft = self.pos)
                elif self.frame3_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.pos = (640, 450)
                    self.rect = self.frame.get_rect(topleft = self.pos)
                elif self.frame4_rect.collidepoint(mouse_pos):
                    self.button_sound.play()
                    self.pos = (800, 450)
                    self.rect = self.frame.get_rect(topleft = self.pos)
                    
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 20:
                        self.text += event.unicode
        return 3
        

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.font.render_to(self.screen, (300, 150), self.name, (255, 255, 255))

        self.font.render_to(self.screen,(self.input_box.x+5, self.input_box.y+5) ,self.text, (255, 255, 255))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)

        self.font.render_to(self.screen, (340, 380), self.title, (255, 255, 255))
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

if __name__ == "__main__":
    char = Character()
    char.run()