import pygame
from pathlib import Path

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Homepage:
    def __init__(self, screen):
        self.screen = screen

        current_dir = Path(__file__).parent
        bg_path = current_dir / "Game Assets" / "bg.png"
        image_path = current_dir / "Game Assets" / "frame.png"
        title_path = current_dir / "Game Assets" / "JEOPARDY.png"
        start_path = current_dir / "Game Assets" / "START.png"
        startframe_path = current_dir / "Game Assets" / "frame_start.png"
        start_pressed_path = current_dir / "Game Assets" / "START_hover.png"
        startframe_pressed_path = current_dir / "Game Assets" / "frame_start_hover.png"
        quit_frame_path = current_dir / "Game Assets" / "quit_frame.png"
        quitting_path = current_dir / "Game Assets" / "QUITTING.png"
        button_path = current_dir / "Game Assets" / "button.png"
        button_pressed_path = current_dir / "Game Assets" / "button_pressed.png"
        yes_path = current_dir / "Game Assets" / "YES.png"
        no_path = current_dir / "Game Assets" / "NO.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        
        self.menu_BGM_path = current_dir / "Sound Effect" / "menu_BGM.mp3"
        button_sound_path = current_dir / "Sound Effect" / "button.mp3"
        self.button_sound = pygame.mixer.Sound(button_sound_path)

        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.frame = pygame.image.load(str(image_path)).convert_alpha()
        self.title = pygame.image.load(str(title_path)).convert_alpha()
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

        self.start = pygame.image.load(str(start_path)).convert_alpha()
        self.start_pressed = pygame.image.load(str(start_pressed_path)).convert_alpha()
        self.start_rect = self.start.get_rect(center = (600, 496))

        self.startframe = pygame.image.load(str(startframe_path)).convert_alpha()
        self.startframe_pressed = pygame.image.load(str(startframe_pressed_path)).convert_alpha()
        self.startframe_rect = self.startframe.get_rect(center = (600, 496))
        
        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        self.music_started = False

    def update(self, events) -> int:
        if not self.music_started:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load(self.menu_BGM_path)
            pygame.mixer.music.play(-1)
            self.music_started = True

        mouse_pos = pygame.mouse.get_pos()
        
        if self.startframe_rect.collidepoint(mouse_pos):
            self.currentframe_start = self.startframe_pressed
            self.current_start = self.start_pressed
        else:
            self.currentframe_start = self.startframe
            self.current_start = self.start

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.music_started = False
                    return 2
                if self.startframe_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.music_started = False
                    return 3
        
        return 1
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.currentframe_start, self.startframe_rect)
        self.screen.blit(self.title, (180, 200))
        self.screen.blit(self.current_start, self.start_rect)
        self.screen.blit(self.quit_button, self.quit_button_rect)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Homepage(screen)
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