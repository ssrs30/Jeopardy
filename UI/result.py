import pygame
import pygame.freetype

from .assets import load_font, load_image, load_sound

pygame.init()

class Result:
    """Answer outcome"""

    def __init__(self, screen):
        self.screen = screen
        self.correct = True

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        self.button_sound = load_sound("Sound Effect", "button.mp3")
        self.correct_sound = load_sound("Sound Effect", "correct_answer.mp3")
        self.wrong_sound = load_sound("Sound Effect", "wrong_answer.mp3")
        self.wrong_sound.set_volume(0.7)

        self.frame_continue = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_continue_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_continue_rect = self.frame_continue.get_rect(center = (600, 700))

        self.continue_text = load_image("Game Assets", "CONTINUE.png", size=(180, 50), label="CONTINUE")
        self.continue_pressed = load_image("Game Assets", "CONTINUE_pressed.png", size=(180, 50), label="CONTINUE")
        self.continue_rect = self.continue_text.get_rect(center = (600, 700))

        self.font = load_font(50)

        self.name = ""
        self.score = 0
        self.gain = False
        self.text = f"{self.name} answered correctly!"
        self.score_text = f"+{self.score}"
        self.custom_mode = False
        self.answer_text = ""
        self.fj_result_mode = False
        self.fj_headline = ""
        self.fj_player_rows: list[tuple[str, str]] = []
        self.fj_correct_answer = ""

    def set_final_jeopardy_result(
        self, headline: str, player_rows: list[tuple[str, str]], correct_answer: str
    ) -> None:
        self.custom_mode = True
        self.fj_result_mode = True
        self.fj_headline = headline
        self.fj_player_rows = list(player_rows)
        self.fj_correct_answer = correct_answer or ""
        self.text = headline
        self.score_text = ""
        self.answer_text = ""

    def update_result(self, name: str, score: int, gain: bool, play_feedback_sound: bool = True):
        self.custom_mode = False
        self.fj_result_mode = False
        self.name = name
        self.score = score
        self.gain = gain
        self.text = f"{self.name} answered correctly!" if gain else f"{self.name} answered incorrectly!"
        sign = "+" if gain else "-"
        self.score_text = f"{sign}{self.score}"
        self.answer_text = ""
        if play_feedback_sound:
            if gain:
                self.correct_sound.play()
            else:
                self.wrong_sound.play()

    def set_correct_answer(self, answer_text: str):
        self.answer_text = answer_text

    def update_custom_message(self, text: str, score_text: str = "", answer_text: str = ""):
        self.custom_mode = True
        self.fj_result_mode = False
        self.text = text
        self.score_text = score_text
        # Always assign so a new custom screen clears stale data (e.g. skip after a wrong answer).
        self.answer_text = answer_text

    def update(self, events):
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()

        if self.frame_continue_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_continue_pressed
            self.current_continue = self.continue_pressed
        else:
            self.current_button = self.frame_continue
            self.current_continue = self.continue_text


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame_continue_rect.collidepoint(event.pos) or self.continue_rect.collidepoint(
                    event.pos
                ):
                    self.button_sound.play()
                    return 2

        return 1

    def draw(self):
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.current_button, self.frame_continue_rect)
        self.screen.blit(self.current_continue, self.continue_rect)

        if self.fj_result_mode:
            head_surf, head_rect = self.font.render(self.fj_headline, (255, 255, 255))
            head_rect.center = (600, 130)
            self.screen.blit(head_surf, head_rect)
            y = 200
            for main_msg, money_msg in self.fj_player_rows:
                main_surf, main_rect = self.font.render(main_msg, (255, 255, 255))
                main_rect.center = (600, y)
                self.screen.blit(main_surf, main_rect)
                y += 52
                money_surf, money_rect = self.font.render(money_msg, (255, 255, 0))
                money_rect.center = (600, y)
                self.screen.blit(money_surf, money_rect)
                y += 70
            if self.fj_correct_answer:
                ans_surf, ans_rect = self.font.render(
                    f"Correct answer: {self.fj_correct_answer}", (255, 150, 150)
                )
                ans_rect.center = (600, 610)
                self.screen.blit(ans_surf, ans_rect)
            return

        self.text_surf, self.text_rect = self.font.render(self.text, (255, 255, 255))
        self.text_rect.center = (600, 320)
        self.screen.blit(self.text_surf, self.text_rect)
        if self.score_text:
            self.font.render_to(self.screen, (520, 410), self.score_text, (255, 255, 0))
        if self.answer_text:
            self.answer_surf, self.answer_rect = self.font.render(f"Correct answer: {self.answer_text}", (255, 150, 150))
            self.answer_rect.center = (600, 500)
            self.screen.blit(self.answer_surf, self.answer_rect)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Result(screen)
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