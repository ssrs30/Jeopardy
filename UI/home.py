import pygame

from .assets import load_image, load_sound, play_music

pygame.init()
pygame.font.init()
pygame.mixer.init()


class Homepage:

    def __init__(self, screen):
        self.screen = screen
        self.button_sound = load_sound("Sound Effect", "button.mp3")
        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.title = load_image("Game Assets", "JEOPARDY.png", size=(840, 160), label="JEOPARDY")
        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright=(1190, 10))
        self.start = load_image("Game Assets", "START.png", size=(220, 70), label="START")
        self.start_pressed = load_image("Game Assets", "START_hover.png", size=(220, 70), label="START")
        self.start_rect = self.start.get_rect(center=(600, 496))
        self.startframe = load_image("Game Assets", "frame_start.png", size=(280, 92), label="")
        self.startframe_pressed = load_image("Game Assets", "frame_start_hover.png", size=(280, 92), label="")
        self.startframe_rect = self.startframe.get_rect(center=(600, 496))
        self.music_started = False
        self.currentframe_start = self.startframe
        self.current_start = self.start
        self.help = load_image("Game Assets", "HELP.png", size=(220, 70), label="HELP")
        self.help_pressed = load_image("Game Assets", "HELP_pressed.png", size=(220, 70), label="HELP")
        self.help_rect = self.help.get_rect(center=(600, 650))
        self.button = load_image("Game Assets", "button.png", size=(280, 92), label="")
        self.button_pressed = load_image("Game Assets", "button_pressed.png", size=(280, 92), label="")
        self.button_rect = self.button.get_rect(center=(600, 650))

    def update(self, events) -> int:
        """Handle clicks and hover."""
        if not self.music_started:
            play_music("Sound Effect", "menu_BGM.mp3")
            self.music_started = True
        mouse_pos = pygame.mouse.get_pos()
        if self.startframe_rect.collidepoint(mouse_pos):
            self.currentframe_start = self.startframe_pressed
            self.current_start = self.start_pressed
        else:
            self.currentframe_start = self.startframe
            self.current_start = self.start
        if self.button_rect.collidepoint(mouse_pos):
            self.current_button = self.button_pressed
            self.current_help = self.help_pressed
        else:
            self.current_button = self.button
            self.current_help = self.help

        for event in events:
            if event.type == pygame.QUIT:
                return 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.music_started = False
                    return 2
                if self.startframe_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.music_started = False
                    return 3
                if self.button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 4
        return 1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.currentframe_start, self.startframe_rect)
        self.screen.blit(self.current_button, self.button_rect)
        self.screen.blit(self.title, (180, 200))
        self.screen.blit(self.current_start, self.start_rect)
        self.screen.blit(self.current_help, self.help_rect)
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