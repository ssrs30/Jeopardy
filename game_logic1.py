import json
import pygame
import sys
import LLM
import random
import threading
from shop import Shop
from home import Homepage
from pause import pause_window
from char import Character

# colors that can be used in UI
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
DARK_BLUE = (20, 30, 80)

# font size and type
SMALL = pygame.font.Font(None, 24)
MEDIUM = pygame.font.Font(None, 36)
LARGE = pygame.font.Font(None, 48)

# screen initiation
HEIGHT = 800
WIDTH = 1000

# Main window UI: BOARD | WAGER | QUESTION | RESULT | SHOP | GAMEOVER
SHOP_BTN_RECT = pygame.Rect(700, 20, 80, 40)


def run_homepage(screen: pygame.Surface, clock: pygame.time.Clock) -> bool:
    """Run start menu, return True if user starts game."""
    homepage = Homepage(screen)
    while True:
        events = pygame.event.get()

        action = homepage.update(events)
        homepage.draw()
        pygame.display.flip()
        clock.tick(60)

        if action == 3:  # start
            return True
        if action == 2:  # quit
            return False


def text_line_break(text: str, word_font: pygame.font.Font, max_width: int) -> list[str]:
    lines = []
    each_line = ""
    for word in text.split():
        if word_font.size(each_line + word)[0] > max_width:
            lines.append(each_line)
            each_line = word
        else:
            each_line += (" " + word)
    lines.append(each_line)
    return lines

def generate_questions(result: dict) -> None:
    data = LLM.q_generate(LLM.prompt)
    start = data.find("{")
    end = data.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found")
    json_str = data[start:end]
    result["all_data"] = json.loads(json_str)

def draw_loading_screen():
    screen.fill(BLACK)
    text = LARGE.render("Generating questions with AI...", True, WHITE)
    text_pos = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_pos)
    pygame.display.flip()

STATE_FILE = "stats.json"
def load_state() -> dict:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "best_score": int(data.get("best_score", 0)),
                "win_streak": int(data.get("win_streak", 0)),
            }
    except (FileNotFoundError, ValueError, TypeError):
        return {"best_score": 0, "win_streak": 0}

def save_state(best_score: int, win_streak: int) -> None:
    data = {"best_score": best_score, "win_streak": win_streak}
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# produce questions and check the answer
class Question:
    def __init__(self, question_text: str, value: int, options: list[str], correct: int):
        self.question_text = question_text
        self.value = value
        self.options = options
        self.correct = correct

    def check_answer(self, user_answer: int) -> bool:
        return user_answer == self.correct


# manage table
class Board:
    def __init__(self, categories: list[str], values: list[int], questions_dict: dict[tuple[int, int], dict]):
        self.categories = categories
        self.values = values
        self.row = len(values)
        self.col = len(categories)
        # question_dict is initialized in Game.__init__
        self.grid = [[None] * self.col for i in range(self.row)]  # list[list[Question]]
        for (col, row), items in questions_dict.items():
            self.grid[row][col] = Question(items["question_text"], items["value"], items["options"], items["correct"])
        self.answered = [[False] * self.col for i in range(self.row)]  # list[list[bool]]

    def get_question(self, row: int, col: int) -> Question:
        return self.grid[row][col]

    # mark the question as answered
    def mark_answered(self, row: int, col: int) -> None:
        self.answered[row][col] = True

    # whether a question has answered
    def is_answered(self, row: int, col: int) -> bool:
        return self.answered[row][col]

    # whether all questions has answered
    def all_answered(self) -> bool:
        for row in self.answered:
            for question_state in row:
                if not question_state:
                    return False
        return True


# ai player and user
class Player:
    def __init__(self, name="User"):
        self.name = name
        self.score = 0
        self.coins = 0
        self.inventory = {
            "skips": 0,
            "fifty_fifty": 0,
            "shields": 0,
            "double_award": 0,  # Ensure this matches the item system
        }

    def add_score(self, points):
        self.score += points

    def subtract_score(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0


# ================== Item Manager Class ==================
class ItemManager:
    def __init__(self, game):
        self.game = game
        
        # Item status activated for this turn
        self.shield_active = False
        self.double_award_active = False
        self.eliminated_options = []  # Store indices of options eliminated by 50/50

        # Define UI positions for item buttons
        self.item_buttons = {
            "skips": pygame.Rect(100, HEIGHT - 80, 150, 50),
            "fifty_fifty": pygame.Rect(300, HEIGHT - 80, 150, 50),
            "shields": pygame.Rect(500, HEIGHT - 80, 150, 50),
            "double_award": pygame.Rect(700, HEIGHT - 80, 150, 50)
        }
        
        # Item display names and colors
        self.item_info = {
            "skips": ("Skip", ORANGE),
            "fifty_fifty": ("50/50", BLUE),
            "shields": ("Shield", GRAY),
            "double_award": ("Double", GOLD)
        }

    def reset_turn(self):
        """Reset item status before each question starts"""
        self.shield_active = False
        self.double_award_active = False
        self.eliminated_options = []

    def draw(self, screen):
        """Draw item buttons at the bottom of the question screen"""
        for item_key, rect in self.item_buttons.items():
            count = self.game.player.inventory.get(item_key, 0)
            
            # Determine button state
            is_usable = count > 0
            if item_key == "fifty_fifty" and len(self.eliminated_options) > 0:
                is_usable = False
            if item_key == "shields" and self.shield_active:
                is_usable = False
            if item_key == "double_award" and self.double_award_active:
                is_usable = False

            # Set color based on availability
            color = self.item_info[item_key][1] if is_usable else (50, 50, 50)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            
            text_str = f"{self.item_info[item_key][0]} (x{count})"
            text_surface = SMALL.render(text_str, True, WHITE)
            text_pos = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_pos)

    def handle_click(self, pos):
        """Handle item click events"""
        for item_key, rect in self.item_buttons.items():
            if rect.collidepoint(pos):
                self.use_item(item_key)
                return True
        return False

    def use_item(self, item_key):
        count = self.game.player.inventory.get(item_key, 0)
        if count <= 0:
            return  

        row, col = self.game.current_question_pos
        question = self.game.board.get_question(row, col)

        if item_key == "skips":
            self.game.player.inventory["skips"] -= 1
            self.game.board.mark_answered(row, col)
            self.game.result_text = "Question Skipped! No penalty."
            self.game.result_color = YELLOW
            self.game.timer_running = False
            self.game.ui_state = "RESULT"
            self.game.result_timer = 180
            self.game._check_round_end() # Uniformly call round end check

        elif item_key == "fifty_fifty":
            if len(self.eliminated_options) == 0:
                self.game.player.inventory["fifty_fifty"] -= 1
                correct_idx = question.correct
                wrong_indices = [i for i in range(4) if i != correct_idx]
                self.eliminated_options = random.sample(wrong_indices, 2)

        elif item_key == "shields":
            if not self.shield_active:
                self.game.player.inventory["shields"] -= 1
                self.shield_active = True

        elif item_key == "double_award":
            if not self.double_award_active:
                self.game.player.inventory["double_award"] -= 1
                self.double_award_active = True
# ================================================


# game running
class Game:
    def __init__(self, all_data: dict):
        if "round1" not in all_data:
            print("Round 1 data doesn't exist.")  # check
            sys.exit(1)
        if "round2" not in all_data:
            print("Round 2 data doesn't exist.")
            sys.exit(1)
        if "round3" not in all_data:
            print("Round 3 data doesn't exist.")
            sys.exit(1)

        round1_data = self._normalize_round_data(all_data["round1"])
        round2_data = self._normalize_round_data(all_data["round2"])
        round3_data = self._normalize_round_data(all_data["round3"])

        categories = []  # categpries shown on the top of the board
        data_1 = {}  # dictionary that contains all questions in round 1
        data_2 = {}  # dictionary that contains all questions in round 2
        data_3 = {}  # dictionary that contains all questions in round 3
        self.data = {"round1": data_1, "round2": data_2, "round3": data_3}

        for column, category in enumerate(round1_data):
            categories.append(category.get("name"))
            questions_1 = category.get("questions")
            values_1 = [items["value"] for items in questions_1]
            for row, items in enumerate(questions_1):
                data_1[(column, row)] = {"question_text": items["question"], "options": items["options"], "correct": items["correct"], "value": items["value"]}

        for column, category in enumerate(round2_data):
            questions_2 = category.get("questions")
            values_2 = [items["value"] for items in questions_2]
            for row, items in enumerate(questions_2):
                data_2[(column, row)] = {"question_text": items["question"], "options": items["options"], "correct": items["correct"], "value": items["value"]}

        for column, category in enumerate(round3_data):
            questions_3 = category.get("questions")
            for row, items in enumerate(questions_3):
                data_3[(column, row)] = {"question_text": items["question"], "options": items["options"], "correct": items["correct"], "value": items["value"]}
        

        self.categories = categories  # list[str]
        self.values = values_1
        self.rows = len(round1_data[0]["questions"])  # int
        self.cols = len(categories)  # int
        self.cell_width = WIDTH // self.cols  # int
        self.cell_height = (HEIGHT - 100) // (self.rows + 1)  # int

        self.board = Board(self.categories, self.values, data_1)
        self.player = Player()

        self.ui_state = "ROUND"  # str
        self.go_to_gameover_after_result = False

        self.double_row_round_1, self.double_col_round_1 = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self.double_row_round_2_1, self.double_row_round_2_2 = random.sample(range(self.rows), 2)
        self.double_col_round_2_1, self.double_col_round_2_2 = random.sample(range(self.cols), 2)

        self.current_round = 1
        self.current_question_pos = None
        self.result_text = ""
        self.result_color = GREEN
        self.result_timer = 0
        self.option_areas = []
        self.selected_option = -1
        self.timer = 5
        self.timer_running = False
        self.last_record = 0
        self.wager_amount = 0
        self.wager_input = ""   
        self.wager_error = ""
        self.wager_input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 44)    # wager input rectangle
        self.wager_confirm_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 48)     # wager confirm rectangle
        self.clear_bonus = False
        self.next_round = False  # whether to go to the next round
        self.best_score = 0
        self.win_streak = 0
        self.gameover_stats_applied = False
        
        # Instantiate the Item Manager
        self.item_manager = ItemManager(self)

    @staticmethod
    def _normalize_round_data(round_data):
        """
        Normalize round data to list[dict].
        Some models return final round as a single dict, not a list.
        """
        if isinstance(round_data, dict):
            return [round_data]
        if isinstance(round_data, list):
            return round_data
        raise ValueError("Invalid round data format from AI response.")

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if self.timer_running and self.ui_state == "QUESTION":
            if current_time - self.last_record >= 1000:
                self.timer -= 1
                self.last_record = current_time
        if self.timer < 0 and self.ui_state == "QUESTION":
            self.check_answer()

    def handle_click(self, pos, shop: "Shop", shop_btn: pygame.Rect) -> bool:
        if self.ui_state == "BOARD":
            if shop_btn.collidepoint(pos):
                self.ui_state = "SHOP"
                return True

            x, y = pos
            if y > 100:
                col = x // self.cell_width
                if 0 <= col < self.cols:
                    col_y = y - 100
                    row = col_y // self.cell_height - 1
                    if 0 <= row < self.rows and not self.board.is_answered(row, col):
                        self.current_question_pos = (row, col)
                        self.selected_option = -1
                        if self.current_round == 2:
                            if row == self.double_row_round_2_1 and col == self.double_col_round_2_1 or (row == self.double_row_round_2_2 and col == self.double_col_round_2_2):
                                self.ui_state = "WAGER"
                                self.wager_amount = 0
                                self.wager_input = ""
                                self.wager_error = ""
                                return True
                        elif self.current_round == 1:
                            if row == self.double_row_round_1 and col == self.double_col_round_1:
                                self.ui_state = "WAGER"
                                self.wager_amount = 0
                                self.wager_input = ""
                                self.wager_error = ""
                                return True
                        elif self.current_round == 3:
                            self.ui_state = "WAGER"
                            self.wager_amount = 0
                            self.wager_input = ""
                            self.wager_error = ""
                            return True
                        self.ui_state = "QUESTION"
                        self.timer = 5
                        self.timer_running = True
                        self.last_record = pygame.time.get_ticks()
                        self.item_manager.reset_turn() # Start new question, reset items
                        return True
            return True

        if self.ui_state == "WAGER":
            if self.wager_confirm_rect.collidepoint(pos):
                self.try_confirm_wager()
            return True

        if self.ui_state == "SHOP":
            react = shop.handle_click(pos)
            if react == "EXIT":
                self.ui_state = "BOARD"
            return True

        if self.ui_state == "QUESTION":
            # Intercept item clicks first
            if self.item_manager.handle_click(pos):
                return True

            for i, region in enumerate(self.option_areas):
                # Exclude options eliminated by 50/50
                if i in self.item_manager.eliminated_options:
                    continue
                
                if region.collidepoint(pos):
                    self.selected_option = i
                    self.check_answer()
                    return True
        return True

    def try_confirm_wager(self) -> bool:
        if self.current_question_pos is None:
            return False
        row, col = self.current_question_pos
        question = self.board.get_question(row, col)
        max_w = max(self.player.score, question.value)
        min_w = 1
        raw = self.wager_input.strip()
        if not raw:
            self.wager_error = "Please input the wager amount"
            print(self.wager_error)
            return False
        try:
            val = int(raw)
        except ValueError:
            self.wager_error = "Please input a valid integer"
            print(self.wager_error)
            return False
        if not (min_w <= val <= max_w):
            self.wager_error = f"The wager must be between {min_w} and {max_w}"
            print(self.wager_error)
            return False
        self.wager_amount = val
        self.wager_error = ""
        self.ui_state = "QUESTION"
        self.timer = 5
        self.timer_running = True
        self.last_record = pygame.time.get_ticks()
        self.item_manager.reset_turn() # Reset items if entering Question from Wager
        return True

    def _check_round_end(self):
        """Extract round end check logic for reuse in special cases like Skip"""
        self.next_round = False
        if self.player.score == 0:
            self.go_to_gameover_after_result = True
        elif self.board.all_answered() and self.current_round == 3:
            self.go_to_gameover_after_result = True
        else:
            self.go_to_gameover_after_result = False

        if self.board.all_answered() and self.current_round < 3 and self.player.score > 0:
            self.next_round = True

    def check_answer(self):
        if self.current_question_pos is None:
            return

        self.timer_running = False
        self.timer = 0

        row, col = self.current_question_pos
        question = self.board.get_question(row, col)
        if (
            (self.current_round == 1 and row == self.double_row_round_1 and col == self.double_col_round_1)
            or (
                self.current_round == 2
                and (
                    row == self.double_row_round_2_1 and col == self.double_col_round_2_1
                    or row == self.double_row_round_2_2 and col == self.double_col_round_2_2
                )
            )
            or self.current_round == 3
        ):
            is_double_daily = True
        else:
            is_double_daily = False
            
        if is_double_daily:
            pts = self.wager_amount
        else:
            pts = question.value

        correct = question.check_answer(self.selected_option)
        if correct:
            if self.item_manager.double_award_active:
                pts *= 2
                self.result_text = f"Correct! +{pts} (Double Award!)"
            else:
                self.result_text = f"Correct! +{pts}"
            
            self.player.add_score(pts)
            self.result_color = GREEN
        else:
            show_correct_answer = question.options[question.correct]
            
            if self.item_manager.shield_active:
                self.result_text = f"Wrong! Shield Protected! Correct: {show_correct_answer}"
                self.result_color = ORANGE
            else:
                self.player.subtract_score(pts)
                self.result_text = f"Wrong! -{pts} Correct answer: {show_correct_answer}"
                self.result_color = RED
                
            if self.player.score == 0:
                self.result_text = "Your score is 0."

        self.board.mark_answered(row, col)
        self.ui_state = "RESULT"
        self.result_timer = 180
        self._check_round_end() # Call unified settlement logic

    def ui_state_for_drawing(self) -> str:
        return self.ui_state

    def draw_wager_screen(self):
        overlay_wager_screen = pygame.Surface((WIDTH, HEIGHT))
        overlay_wager_screen.set_alpha(0)
        overlay_wager_screen.fill(GOLD)
        screen.blit(overlay_wager_screen, (0, 0))

        title = LARGE.render("Daily Double — Input the wager", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140)))

        if self.current_question_pos:
            row, col = self.current_question_pos
            question = self.board.get_question(row, col)
            max_w = max(self.player.score, question.value)
            hint = SMALL.render(f"Valid range: 1 —— {max_w}(input with number, enter or click CONFIRM)", True, WHITE)
            screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 95)))

        pygame.draw.rect(screen, WHITE, self.wager_input_rect, 2)
        inner = self.wager_input_rect.inflate(-8, -8)
        pygame.draw.rect(screen, BLACK, inner)
        display = self.wager_input if self.wager_input else " "
        display_text = MEDIUM.render(display, True, WHITE)
        screen.blit(display_text, (self.wager_input_rect.x + 8, self.wager_input_rect.centery - display_text.get_height() // 2))

        if self.wager_error:
            error = MEDIUM.render(self.wager_error, True, RED)
            screen.blit(error, error.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        pygame.draw.rect(screen, GREEN, self.wager_confirm_rect)
        pygame.draw.rect(screen, WHITE, self.wager_confirm_rect, 2)
        c = MEDIUM.render("CONFIRM", True, BLACK)
        screen.blit(c, c.get_rect(center=self.wager_confirm_rect.center))

    def draw_board_screen(self):
        # category text
        for col in range(self.cols):
            rectangle = pygame.Rect(col * self.cell_width, 100, self.cell_width, self.cell_height)
            pygame.draw.rect(screen, BLUE, rectangle)
            pygame.draw.rect(screen, WHITE, rectangle, 2)
            category_text = MEDIUM.render(self.categories[col], True, WHITE)
            category_text_pos = category_text.get_rect(center=rectangle.center)
            screen.blit(category_text, category_text_pos)

        # question text
        for row in range(self.rows):
            y = 100 + self.cell_height * (row + 1)
            for col in range(self.cols):
                x = col * self.cell_width
                rectangle = pygame.Rect(x, y, self.cell_width, self.cell_height)
                if self.board.is_answered(row, col):
                    color = GRAY
                else:
                    color = BLUE
                pygame.draw.rect(screen, color, rectangle)
                pygame.draw.rect(screen, WHITE, rectangle, 2)
                question = self.board.get_question(row, col)
                value_text = MEDIUM.render(str(question.value), True, WHITE)
                value_text_pos = value_text.get_rect(center=rectangle.center)
                screen.blit(value_text, value_text_pos)

    def draw_question_screen(self):
        question_screen = pygame.Surface((WIDTH, HEIGHT))
        question_screen.fill(BLACK)
        question_screen.set_alpha(200)
        screen.blit(question_screen, (0, 0))

        row, col = self.current_question_pos
        question = self.board.get_question(row, col)

        max_width = WIDTH - 80
        q_text_lines = text_line_break(question.question_text, LARGE, max_width)
        for i, line in enumerate(q_text_lines):
            q_text = LARGE.render(line, True, WHITE)
            q_text_pos = q_text.get_rect(center=(WIDTH // 2, 150 + i * 30))
            screen.blit(q_text, q_text_pos)

        self.option_areas = []  # the list of the area of four option buttons
        option_height = 80
        option_width = 500
        start_y = 280
        space_between = 20

        colors = [BLUE, BLUE, BLUE, BLUE]  # color list for buttons
        if self.selected_option != -1:
            colors[self.selected_option] = ORANGE

        for i, option in enumerate(question.options):
            x = WIDTH // 2 - option_width // 2
            y = start_y + i * (option_height + space_between)
            rectangle = pygame.Rect(x, y, option_width, option_height)
            self.option_areas.append(rectangle)

            # --- Draw only gray box and skip text for options eliminated by 50/50 ---
            if i in self.item_manager.eliminated_options:
                pygame.draw.rect(screen, (30, 30, 30), rectangle) 
                pygame.draw.rect(screen, (100, 100, 100), rectangle, 3)
                continue  

            pygame.draw.rect(screen, colors[i], rectangle)
            pygame.draw.rect(screen, WHITE, rectangle, 3)

            option_text = MEDIUM.render(option, True, BLACK)
            option_text_pos = option_text.get_rect(center=rectangle.center)
            screen.blit(option_text, option_text_pos)

        # Draw item bar at the bottom
        self.item_manager.draw(screen)

        if (
            (self.current_round == 1 and row == self.double_row_round_1 and col == self.double_col_round_1)
            or (
                self.current_round == 2
                and (
                    row == self.double_row_round_2_1 and col == self.double_col_round_2_1
                    or row == self.double_row_round_2_2 and col == self.double_col_round_2_2
                )
            )
            or self.current_round == 3
        ):
            is_daily_doubled = True
        else:
            is_daily_doubled = False
        new_value = self.wager_amount if is_daily_doubled else question.value
        daily_double_suffix = " (Daily Double!)" if is_daily_doubled else ""
        value_text = MEDIUM.render(f"Value: {new_value}{daily_double_suffix}", True, YELLOW)
        value_text_pos = value_text.get_rect(center=(WIDTH // 2, 210))
        screen.blit(value_text, value_text_pos)

    def draw_result(self):
        overlay_result_screen = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        overlay_result_screen.set_alpha(150)
        overlay_result_screen.fill(BLACK)
        overlay_pos = overlay_result_screen.get_rect(center=screen.get_rect().center)
        screen.blit(overlay_result_screen, (overlay_pos))

        result_text_pattern = LARGE.render(self.result_text, True, self.result_color)
        result_text_pos = result_text_pattern.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(result_text_pattern, result_text_pos)

        timer_text = MEDIUM.render(f"Return to board in {self.result_timer // 60 + 1}", True, WHITE)
        timer_text_pos = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(timer_text, timer_text_pos)

    def draw_round_screen(self):
        overlay_gameover_screen = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        overlay_gameover_screen.set_alpha(0)
        overlay_gameover_screen.fill(BLACK)
        screen.blit(overlay_gameover_screen, (0, 0))
        round_text = LARGE.render(f"Round {self.current_round}", True, WHITE)
        round_text_pos = round_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(round_text, round_text_pos)

        show_score_text = MEDIUM.render(f"Your score is: {self.player.score}", True, YELLOW)
        show_score_text_pos = show_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(show_score_text, show_score_text_pos)

        continue_text = MEDIUM.render("Press any key to continue", True, WHITE)
        continue_text_pos = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(continue_text, continue_text_pos)

    def draw_game_over_screen(self):
        overlay_gameover_screen = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        overlay_gameover_screen.set_alpha(0)
        overlay_gameover_screen.fill(BLACK)
        screen.blit(overlay_gameover_screen, (0, 0))

        if self.player.score == 0:
            game_over_text = LARGE.render("You lose!", True, RED)
            score_text = LARGE.render(f"Game Over!", True, YELLOW)
        else:
            game_over_text = LARGE.render("You win!", True, GREEN)
            score_text = LARGE.render(f"Final Score: {self.player.score}", True, YELLOW)
        score_text_pos = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        game_over_text_pos = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(game_over_text, game_over_text_pos)
        screen.blit(score_text, score_text_pos)

        best_text = MEDIUM.render(f"Best Score: {self.best_score}", True, WHITE)
        streak_text = MEDIUM.render(f"Current Win Streak: {self.win_streak}", True, WHITE)
        screen.blit(best_text, best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        screen.blit(streak_text, streak_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))

        quit_text = MEDIUM.render("Press ESC to quit", True, WHITE)
        quit_text_pos = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(quit_text, quit_text_pos)
        restart_text = MEDIUM.render("Press ENTER to restart", True, WHITE)
        restart_text_pos = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_text_pos)

def run_game():
    global screen
    result = {}
    threading.Thread(target=generate_questions, args=(result,), daemon=True).start()
    
    state = load_state()
    best_score = state["best_score"]
    win_streak = state["win_streak"]

    # 1. Run Home UI
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Jeopardy!")
    if not run_homepage(screen, clock):
        pygame.quit()
        sys.exit(0)

    # 2. Run new character + username UI
    character_ui = Character(screen)
    user_name, _avatar_path = character_ui.run()

    # 3. Setup Main Game Window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Jeopardy!')
    screen.fill(BLACK)
    pygame.display.flip()
    
    # Initialize Game with data from Login
    game = None
    shop = None
    running = True
    pending_quit_on_loading = False
    pause_modal = pause_window(screen)
    confirm_quit = False

    while running:
        if game is None:
            if "all_data" not in result:
                for event in pygame.event.get():
                    if not pending_quit_on_loading and event.type in (pygame.QUIT,):
                        pending_quit_on_loading = True
                    elif not pending_quit_on_loading and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pending_quit_on_loading = True
                    elif pending_quit_on_loading:
                        choice = pause_modal.update([event], 1)
                        if choice == 0:
                            pygame.quit()
                            sys.exit(0)
                        if choice == 1:
                            pending_quit_on_loading = False
                draw_loading_screen()
                if pending_quit_on_loading:
                    pause_modal.draw()
                pygame.display.flip()
                clock.tick(60)
                continue
            else:
                game = Game(result["all_data"])
                game.player.name = user_name
                shop = Shop(screen, game.player)
                game.best_score = best_score
                game.win_streak = win_streak

        screen.fill((0, 0, 0))
        base = game.ui_state_for_drawing()

        if base == "BOARD":
            screen.blit(LARGE.render(f"Score: {game.player.score}", True, YELLOW), (20, 20))
            game.draw_board_screen()
            pygame.draw.rect(screen, (128, 0, 128), SHOP_BTN_RECT)
            screen.blit(pygame.font.Font(None, 24).render("SHOP", True, (255, 255, 255)), (715, 30))
        elif base == "WAGER":
            screen.blit(LARGE.render(f"Score: {game.player.score}", True, YELLOW), (20, 20))
            game.draw_wager_screen()
        elif base == "QUESTION":
            game.update_timer()
            screen.blit(LARGE.render(f"Score: {game.player.score}", True, YELLOW), (20, 20))
            if game.timer_running:
                tc = RED if game.timer <= 3 else WHITE
                ts = LARGE.render(f"Time: {game.timer}", True, tc)
                screen.blit(ts, ts.get_rect(topright=(WIDTH - 400, 20)))
            game.draw_question_screen()
        elif base == "RESULT":
            screen.blit(LARGE.render(f"Score: {game.player.score}", True, YELLOW), (20, 20))
            if game.result_timer > 0:
                game.draw_result()
                game.result_timer -= 1
                if game.result_timer <= 0:
                    game.current_question_pos = None
                    if game.next_round:
                        game.next_round = False
                        game.current_round += 1
                        game.board = Board(
                            game.categories,
                            game.values,
                            game.data[f"round{game.current_round}"],
                        )
                        game.double_row_round_1 = random.randint(0, game.rows - 1)
                        game.double_col_round_1 = random.randint(0, game.cols - 1)
                        game.double_row_round_2_1, game.double_row_round_2_2 = random.sample(range(game.rows), 2)
                        game.double_col_round_2_1, game.double_col_round_2_2 = random.sample(range(game.cols), 2)
                        game.clear_bonus = False
                        game.ui_state = "ROUND"
                    elif game.go_to_gameover_after_result:
                        if not game.gameover_stats_applied:
                            best_score = max(best_score, game.player.score)
                            if game.player.score > 0:
                                win_streak += 1
                            else:
                                win_streak = 0
                            game.best_score = best_score
                            game.win_streak = win_streak
                            save_state(best_score, win_streak)
                            game.gameover_stats_applied = True  # prevent double application of state
                        game.ui_state = "GAMEOVER"
                    else:
                        game.ui_state = "BOARD"
        elif base == "SHOP":
            shop.draw()
        elif base == "ROUND":
            game.draw_round_screen()            
        elif base == "GAMEOVER":
            game.draw_game_over_screen()

        if game.board.all_answered() and not game.clear_bonus:
            game.player.coins += 1000
            game.clear_bonus = True

        for event in pygame.event.get():
            if not confirm_quit and event.type in (pygame.QUIT,):
                confirm_quit = True
                continue
            if not confirm_quit and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                confirm_quit = True
                continue
            if confirm_quit:
                choice = pause_modal.update([event], 1)
                if choice == 0:
                    running = False
                elif choice == 1:
                    confirm_quit = False
                continue

            if event.type == pygame.KEYDOWN:
                if game.ui_state == "ROUND":
                    game.ui_state = "BOARD"
                    continue
                if game.ui_state == "GAMEOVER":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        result = {}
                        threading.Thread(target=generate_questions, args=(result,), daemon=True).start()
                        game = None
                        shop = None
                        pending_quit_on_loading = False
                        confirm_quit = False
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        confirm_quit = True
                    continue
                if game.ui_state == "WAGER":
                    if event.key == pygame.K_BACKSPACE:
                        game.wager_input = game.wager_input[:-1]
                        game.wager_error = ""
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        game.try_confirm_wager()
                    elif event.unicode and event.unicode.isdigit() and len(game.wager_input) < 10:
                        game.wager_input += event.unicode
                        game.wager_error = ""
                elif game.ui_state == "QUESTION":
                    # Add condition: prevent keyboard selection of options eliminated by 50/50
                    if event.key == pygame.K_1 and 0 not in game.item_manager.eliminated_options:
                        game.selected_option = 0
                        game.check_answer()
                    elif event.key == pygame.K_2 and 1 not in game.item_manager.eliminated_options:
                        game.selected_option = 1
                        game.check_answer()
                    elif event.key == pygame.K_3 and 2 not in game.item_manager.eliminated_options:
                        game.selected_option = 2
                        game.check_answer()
                    elif event.key == pygame.K_4 and 3 not in game.item_manager.eliminated_options:
                        game.selected_option = 3
                        game.check_answer()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.ui_state == "ROUND":
                    game.ui_state = "BOARD"
                    continue
                if not game.handle_click(event.pos, shop, SHOP_BTN_RECT):
                    running = False

        if confirm_quit:
            pause_modal.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()