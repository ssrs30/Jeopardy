import pygame
from pathlib import Path

pygame.init()

class GameOver:
    def __init__(self, screen):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        current_dir = Path(__file__).parent
        bg_path = current_dir / "Game Assets" / "bg.png"
        game_over_path = current_dir / "Game Assets" / "GAMEOVER.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        frame_player_path = current_dir / "Game Assets" / "frame_player.png"
        back_path = current_dir / "Game Assets" / "Back.png"
        back_pressed_path = current_dir / "Game Assets" / "Back_pressed.png"
        back_frame_path = current_dir / "Game Assets" / "back_frame.png"
        back_frame_pressed_path = current_dir / "Game Assets" / "back_frame_pressed.png"
        trophy_path = current_dir / "Game Assets" / "trophy.png"

        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.frame_player = pygame.image.load(str(frame_player_path)).convert_alpha()
        self.game_over = pygame.image.load(str(game_over_path)).convert_alpha()
        self.trophy = pygame.image.load(str(trophy_path)).convert_alpha()

        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.back_text = pygame.image.load(str(back_path)).convert_alpha()
        self.back_pressed = pygame.image.load(str(back_pressed_path)).convert_alpha()
        self.back_rect = self.back_text.get_rect(center = (600, 700))
        
        self.back_frame = pygame.image.load(str(back_frame_path)).convert_alpha()
        self.back_frame_pressed = pygame.image.load(str(back_frame_pressed_path)).convert_alpha()
        self.back_frame_rect = self.back_frame.get_rect(center = (600, 700))

    def update_result(self, result: list[list[str | int]]): #[[player_char, player_name, player_score]]
        self.firstPlace = result[0]
        self.secondPlace = result[1]
        self.thirdPlace = result[2]
    
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()

        if self.back_frame_rect.collidepoint(mouse_pos):
            self.current_back = self.back_pressed
            self.current_back_frame = self.back_frame_pressed
        else:
            self.current_back = self.back_text
            self.current_back_frame = self.back_frame
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(event.pos):
                    return 2
                if self.back_frame_rect.collidepoint(event.pos):
                    return 2
        
        return 1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.game_over, (200, 100))
        self.screen.blit(self.frame_player, (440, 320))
        self.screen.blit(self.frame_player, (200, 450))
        self.screen.blit(self.frame_player, (680, 450))
        self.screen.blit(self.trophy, (700, 300))

        self.screen.blit(self.current_back_frame, self.back_frame_rect)
        self.screen.blit(self.current_back, self.back_rect)
        


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = GameOver(screen)
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