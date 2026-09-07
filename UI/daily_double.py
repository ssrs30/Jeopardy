import pygame
import pygame.freetype
from . import Text_wrapper
from .assets import load_font, load_image

pygame.init()
pygame.font.init()

class dailydouble:
    """Wager entry for Daily Double or Final Jeopardy"""
    def __init__(self, screen):
        """Load continue button, fonts, input box colors, and default title/wager copy."""
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(150)

        self.font = load_font(50)
        self.font_warning = load_font(32)
        self.title = "YOU FOUND A DAILY DOUBLE!"
        self.wager_text = "YOUR WAGER:"

        self.frame_continue = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_continue_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_continue_rect = self.frame_continue.get_rect(center = (600, 700))

        self.continue_text = load_image("Game Assets", "CONTINUE.png", size=(180, 50), label="CONTINUE")
        self.continue_pressed = load_image("Game Assets", "CONTINUE_pressed.png", size=(180, 50), label="CONTINUE")
        self.continue_rect = self.continue_text.get_rect(center = (600, 700))

        self.current_warning = ""
        self.warning_text1 = "Error: invalid value. Please input integers only."
        self.warning_rect = pygame.Rect(300, 450, 600, 100)
        self.wager_min = 5

        self.input_box = pygame.Rect(300, 400, 600, 50)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_inactive = pygame.Color('gray15')
        self.color = self.color_inactive

        self.text = ''
        self.active = False

    def wager_out_of_range_message(self, score: int) -> str:
        """Human-readable error message"""
        hi = max(0, int(score))
        if self.wager_min == 0:
            return f"Error: value is out of range. Enter an integer from 0 to {hi}."
        if hi >= self.wager_min:
            return f"Error: value is out of range. Enter an integer from {self.wager_min} to {hi}."
        return "Error: value is out of range. Your score is below 5; you must wager exactly 5."

    def update(self, events, score):
        """Handle text input and continue"""
        mouse_pos = pygame.mouse.get_pos()
        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_button = self.frame_continue
            self.current_continue = self.continue_text

        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.input_box.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive

                if self.frame_continue_rect.collidepoint(event.pos):
                    try:
                        num = int(self.text)
                        hi = max(0, int(score))
                        lo = self.wager_min
                        if lo == 0:
                            valid = 0 <= num <= hi
                        elif hi >= lo:
                            valid = lo <= num <= hi
                        else:
                            valid = num == 5
                        if valid:
                            return 2, int(self.text)
                        else:
                            self.current_warning = self.wager_out_of_range_message(score)
                    except ValueError:
                        self.current_warning = self.warning_text1
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 10:
                        self.text += event.unicode
        return 1, 0
    
    def update_character(self, char_path):
        try:
            self.char = pygame.image.load(str(char_path)).convert_alpha()
        except Exception:
            self.char = None

    def draw(self):
        self.screen.blit(self.dark_surface, (0, 0))
        
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