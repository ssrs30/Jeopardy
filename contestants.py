import random
import pygame


def _ai_timing_and_accuracy_for_round(round_no: int) -> tuple[float, float, float]:
    if round_no <= 1:
        return (3.0, 6.0, 0.90)
    if round_no == 2:
        return (5.0, 8.0, 0.70)
    return (8.0, 10.0, 0.50)


def placeholder_avatar_surface(label, bg_color, fg_color=(255, 255, 255)):
    surf = pygame.Surface((50, 50))
    surf.fill(bg_color)
    pygame.draw.rect(surf, fg_color, surf.get_rect(), 2)
    font = pygame.font.Font(None, 22)
    text = font.render(label[:4], True, fg_color)
    surf.blit(text, text.get_rect(center=surf.get_rect().center))
    return surf


class Player:
    """Optional duel-mode avatar/score holder"""

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.avatar_img = placeholder_avatar_surface("?", (200, 200, 200))
        self.is_ai = False

    def add_score(self, points):
        self.score += points

    def subtract_score(self, points):
        self.score -= points


class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_ai = True
        self.correct_clues = 0  
        self.target_time_ms = 0
        self.will_answer_index = None
        self.is_ready_to_answer = False
        self.avatar_img = placeholder_avatar_surface("AI", (40, 80, 120))

    def prepare_choice(self, correct_option_index, num_options, current_time_ms, round_no: int = 1):
        self.is_ready_to_answer = True
        delay_lo, delay_hi, accuracy = _ai_timing_and_accuracy_for_round(round_no)
        delay_sec = random.uniform(delay_lo, delay_hi)
        self.target_time_ms = current_time_ms + int(delay_sec * 1000)
        if random.random() < accuracy:
            self.will_answer_index = correct_option_index
        else:
            wrong = [i for i in range(num_options) if i != correct_option_index]
            self.will_answer_index = random.choice(wrong)

    def check_time_and_answer(self, current_time_ms):
        if self.is_ready_to_answer and current_time_ms >= self.target_time_ms:
            self.is_ready_to_answer = False
            return self.will_answer_index
        return None

    def cancel_pending(self):
        self.is_ready_to_answer = False
