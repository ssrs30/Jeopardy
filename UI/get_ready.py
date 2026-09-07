import pygame
import pygame.freetype
from . import Text_wrapper
from .assets import load_font, load_image, load_sound
import threading

pygame.init()
pygame.font.init()
pygame.mixer.init()


def round_display_name(round_no: int) -> str:
    if round_no == 1:
        return "Single Jeopardy"
    if round_no == 2:
        return "Double Jeopardy"
    if round_no == 3:
        return "Final Jeopardy"
    return f"Round {round_no}"


class GetReady:

    def __init__(self, screen, round_no):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(150)

        self.get_ready_sound = load_sound("Sound Effect", "next_round.mp3")
        self.button_sound = load_sound("Sound Effect", "button.mp3")

        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.frame_player = load_image("Game Assets", "frame_player.png", size=(280, 90), label="")

        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.frame_continue = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_continue_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_continue_rect = self.frame_continue.get_rect(center = (600, 700))

        self.continue_text = load_image("Game Assets", "CONTINUE.png", size=(180, 50), label="CONTINUE")
        self.continue_pressed = load_image("Game Assets", "CONTINUE_pressed.png", size=(180, 50), label="CONTINUE")
        self.continue_rect = self.continue_text.get_rect(center = (600, 700))

        self.items = load_image("Game Assets", "ITEMS.png", size=(160, 48), label="ITEMS")
        self.items_pressed = load_image("Game Assets", "ITEMS_pressed.png", size=(160, 48), label="ITEMS")
        self.items_rect = self.items.get_rect(center = (1050, 50))

        self.shop = load_image("Game Assets", "SHOP.png", size=(160, 48), label="SHOP")
        self.shop_pressed = load_image("Game Assets", "SHOP_pressed.png", size=(160, 48), label="SHOP")
        self.shop_rect = self.shop.get_rect(center = (875, 50))

        self.top_button = load_image("Game Assets", "top_button.png", size=(180, 56), label="")
        self.top_button_pressed = load_image("Game Assets", "top_button_pressed.png", size=(180, 56), label="")
        self.top_button_items_rect = self.top_button.get_rect(center = (1050, 50))
        self.top_button_shop_rect = self.top_button.get_rect(center = (875, 50))

        self.round_no = round_no
        self.text = f"Get Ready for {round_display_name(round_no)}!"
        self.text_rect = pygame.Rect(600, 300, 800, 250)
        self.font = load_font(100)
        self.summary_font = load_font(36)
        self.summary_title_font = load_font(52)

        self.ready = False
        self.thread_start = False
        self.summary_mode = False
        self.summary_lines = []
        self.summary_title = ""
        self._play_get_ready_sound_once = True

    def ountdown(self):
        """Start a 2 second timer thread"""
        threading.Timer(2.0, self._change_state).start()
    
    def _change_state(self):
        """allow the player to press CONTINUE button"""
        self.ready = True

    @staticmethod
    def all_boards_pressed(board_window) -> bool:
        """True if every question has been selected."""
        pressed = [v for k, v in vars(board_window).items() if k.endswith("_pressed")]
        return bool(pressed) and all(pressed)

    def sync_round_no(self, round_no: int, windows: list[object] | None = None):
        """update round number"""
        self.round_no = round_no
        self.text = f"Get Ready for {round_display_name(round_no)}!"
        if windows:
            for win in windows:
                try:
                    setattr(win, "round_no", round_no)
                except Exception:
                    pass

    def try_advance_round(self, board_window, windows: list[object] | None = None) -> bool:
        """check board press state"""
        if not self.all_boards_pressed(board_window):
            return False
        self.sync_round_no(self.round_no + 1, windows)
        return True

    def set_round_summary(self, round_no: int, player_name: str, player_score: int, ai1: int, ai2: int):
        self.summary_mode = True
        self.ready = True
        self.thread_start = True
        self.summary_title = f"{round_display_name(round_no)} Summary"
        ranked = [
            (f"{player_name}: {player_score}", player_score),
            (f"AI 1: {ai1}", ai1),
            (f"AI 2: {ai2}", ai2),
        ]
        ranked.sort(key=lambda row: row[1], reverse=True)
        self.summary_lines = [line for line, _ in ranked]

    def clear_summary(self):
        self.summary_mode = False
        self.summary_lines = []
        self.summary_title = ""
        self.ready = False
        self.thread_start = False
    
    def update(self, events):
        """Handle clicks and hover."""
        if self.summary_mode:
            mouse_pos = pygame.mouse.get_pos()
            if self.frame_continue_rect.collidepoint(mouse_pos):
                self.current_button = self.frame_continue_pressed
                self.current_continue = self.continue_pressed
            else:
                self.current_button = self.frame_continue
                self.current_continue = self.continue_text
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame_continue_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 4
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return 4
                if event.type == pygame.MOUSEBUTTONDOWN and self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
            return 1

        if not self.thread_start:

            self.ountdown()
            self.thread_start = True
        
        mouse_pos = pygame.mouse.get_pos()

        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_button = self.frame_continue
            self.current_continue = self.continue_text

        if self.top_button_items_rect.collidepoint(mouse_pos):
            self.current_top_button_items = self.top_button_pressed
            self.current_items = self.items_pressed
        else:
            self.current_top_button_items = self.top_button
            self.current_items = self.items
        
        if self.top_button_shop_rect.collidepoint(mouse_pos):
            self.current_top_button_shop = self.top_button_pressed
            self.current_shop = self.shop_pressed
        else:
            self.current_top_button_shop = self.top_button
            self.current_shop = self.shop
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
                if self.ready and self.frame_continue_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 4
                if self.top_button_items_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 11
                if self.top_button_shop_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 10
                
        return 1

    def draw(self):
        if self._play_get_ready_sound_once:
            if not self.summary_mode:
                self.get_ready_sound.play()
            self._play_get_ready_sound_once = False

        if self.summary_mode:
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.dark_surface, (0, 0))
            self.screen.blit(self.quit_button, self.quit_button_rect)
            self.screen.blit(self.current_button, self.frame_continue_rect)
            self.screen.blit(self.current_continue, self.continue_rect)
            Text_wrapper.draw_wrapped_text(
                self.screen,
                self.summary_title,
                self.summary_title_font,
                (255, 255, 255),
                pygame.Rect(600, 180, 900, 120),
                True,
            )
            y = 320
            for line in self.summary_lines:
                surf, rect = self.summary_font.render(line, (255, 255, 255))
                rect.center = (600, y)
                self.screen.blit(surf, rect)
                y += 55
            return

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        if self.ready:
            self.screen.blit(self.current_button, self.frame_continue_rect)
            self.screen.blit(self.current_continue, self.continue_rect)

        Text_wrapper.draw_wrapped_text(self.screen, self.text, self.font, (255, 255, 255), self.text_rect, True)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = GetReady(screen, 2)
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