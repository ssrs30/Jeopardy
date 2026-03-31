"""
Single Jeopardy, Double Jeopardy, Final Jeopardy
目前只做了single jeopardy
"""

import json
import os
import pygame
import sys
import LLM
import threading


pygame.init()

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
DARK_GRAY = (150, 150, 150)
BLUE_LOGIN = (0, 120, 255)
PURPLE = (128, 0, 128)
DARK_BLUE = (30, 30, 60)

# font size and type
SMALL = pygame.font.Font(None, 24)
MEDIUM = pygame.font.Font(None, 36)
LARGE = pygame.font.Font(None, 48)

# screen initiation
HEIGHT = 800
WIDTH = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeopardy!')
screen.fill(BLACK)

pygame.display.flip()


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
    data = LLM.q_generate(LLM.prompt1)
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


# ================== Login（头像路径相对本文件，保证 avatar 图片能加载）==================
class LoginScreen:
    def __init__(self):
        self.username = ""
        self.input_active = False
        self.error_msg = ""
        self.selected_path = None
        self.avatars = []
        base = os.path.dirname(os.path.abspath(__file__))
        self.avatar_folder = os.path.join(base, "avatar")
        if not os.path.isdir(self.avatar_folder):
            os.makedirs(self.avatar_folder, exist_ok=True)
        self.load_avatars()

    def load_avatars(self):
        self.avatars = []
        valid_exts = (".png", ".jpg", ".jpeg", ".bmp")
        if not os.path.isdir(self.avatar_folder):
            return
        files = [f for f in os.listdir(self.avatar_folder) if f.lower().endswith(valid_exts)]
        for f in files:
            path = os.path.join(self.avatar_folder, f)
            try:
                img = pygame.image.load(path).convert_alpha()
                display_img = pygame.transform.smoothscale(img, (80, 80))
                self.avatars.append({"path": path, "img": display_img})
            except pygame.error as e:
                print(f"Avatar load failed {path}: {e}")

    def run(self):
        clock = pygame.time.Clock()
        while True:
            screen.fill(WHITE)

            title_surf = LARGE.render("USER LOGIN", True, BLACK)
            screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 40))

            input_rect = pygame.Rect(WIDTH // 2 - 150, 140, 300, 50)
            border_color = BLUE_LOGIN if self.input_active else DARK_GRAY
            pygame.draw.rect(screen, border_color, input_rect, 2)

            name_surf = MEDIUM.render(
                self.username + ("|" if self.input_active else ""), True, BLACK
            )
            screen.blit(name_surf, (input_rect.x + 10, input_rect.y + 15))

            label_name = SMALL.render("Username:", True, BLACK)
            screen.blit(label_name, (input_rect.x, input_rect.y - 28))

            grid_label = MEDIUM.render("Select your Avatar:", True, BLACK)
            screen.blit(grid_label, (80, 228))

            grid_x = max(40, (WIDTH - (6 * (80 + 20) - 20)) // 2)
            grid_y = 260
            avatar_rects = []

            if not self.avatars:
                warn_surf = SMALL.render(
                    "(No images in /avatar — you can still LOGIN with name only)", True, RED
                )
                screen.blit(warn_surf, (grid_x, grid_y))

            for i, data in enumerate(self.avatars):
                col = i % 6
                row = i // 6
                x = grid_x + col * (80 + 20)
                y = grid_y + row * (80 + 20)
                rect = pygame.Rect(x, y, 80, 80)
                avatar_rects.append((rect, data["path"]))
                if self.selected_path == data["path"]:
                    pygame.draw.rect(screen, GOLD, rect.inflate(10, 10), 4)
                screen.blit(data["img"], (x, y))

            btn_login = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 55)
            pygame.draw.rect(screen, BLUE_LOGIN, btn_login, border_radius=10)
            btn_text = MEDIUM.render("LOGIN", True, WHITE)
            screen.blit(
                btn_text,
                (
                    btn_login.centerx - btn_text.get_width() // 2,
                    btn_login.centery - btn_text.get_height() // 2,
                ),
            )

            if self.error_msg:
                error_surf = SMALL.render(self.error_msg, True, RED)
                screen.blit(error_surf, (WIDTH // 2 - error_surf.get_width() // 2, HEIGHT - 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

                    for rect, path in avatar_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_path = path

                    if btn_login.collidepoint(event.pos):
                        if not self.username.strip():
                            self.error_msg = "Please enter a username!"
                        elif self.avatars and not self.selected_path:
                            self.error_msg = "Please select an avatar!"
                        else:
                            return self.username.strip(), self.selected_path

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.input_active = False
                    else:
                        if len(self.username) < 16:
                            self.username += event.unicode

            pygame.display.flip()
            clock.tick(60)


# ================== Shop ==================
class Shop:
    def __init__(self, screen, player, sw: int, sh: int):
        self.screen = screen
        self.player = player
        self.font_m = pygame.font.Font(None, 36)
        self.font_s = pygame.font.Font(None, 24)
        ox = max(0, (sw - 800) // 2)
        self.items = [
            {
                "id": "skip",
                "name": "Skip Card",
                "price": 500,
                "desc": "Skip one question safely",
                "rect": pygame.Rect(100 + ox, 150, 280, 100),
            },
            {
                "id": "fifty_fifty",
                "name": "50/50",
                "price": 300,
                "desc": "Remove 2 wrong options",
                "rect": pygame.Rect(420 + ox, 150, 280, 100),
            },
            {
                "id": "shield",
                "name": "Point Shield",
                "price": 400,
                "desc": "No penalty for wrong answer",
                "rect": pygame.Rect(100 + ox, 280, 280, 100),
            },
            {
                "id": "double",
                "name": "Double Chance",
                "price": 600,
                "desc": "Two attempts for one question",
                "rect": pygame.Rect(420 + ox, 280, 280, 100),
            },
        ]
        self.exit_button = pygame.Rect(sw // 2 - 75, min(480, sh - 80), 150, 50)
        self.message = ""
        self.msg_timer = 0

    def draw(self):
        self.screen.fill(DARK_BLUE)
        w = self.screen.get_width()
        title = self.font_m.render("GAME SHOP", True, GOLD)
        self.screen.blit(title, (w // 2 - title.get_width() // 2, 40))

        coin_txt = self.font_m.render(f"Your Coins: {self.player.coins}", True, WHITE)
        self.screen.blit(coin_txt, (50, 90))

        inv_txt = self.font_s.render(
            f"Inventory -> Skip: {self.player.inventory.get('skips', 0)} | "
            f"50/50: {self.player.inventory.get('fifty_fifty', 0)} | "
            f"Shield: {self.player.inventory.get('shields', 0)}",
            True,
            GRAY,
        )
        self.screen.blit(inv_txt, (50, 120))

        for item in self.items:
            pygame.draw.rect(self.screen, BLUE_LOGIN, item["rect"], border_radius=10)
            pygame.draw.rect(self.screen, WHITE, item["rect"], 2, border_radius=10)
            name_surf = self.font_m.render(item["name"], True, WHITE)
            price_surf = self.font_m.render(f"${item['price']}", True, GOLD)
            desc_surf = self.font_m.render(item["desc"], True, GRAY)
            self.screen.blit(name_surf, (item["rect"].x + 15, item["rect"].y + 15))
            self.screen.blit(price_surf, (item["rect"].x + 200, item["rect"].y + 15))
            self.screen.blit(desc_surf, (item["rect"].x + 15, item["rect"].y + 60))

        pygame.draw.rect(self.screen, PURPLE, self.exit_button, border_radius=5)
        exit_txt = self.font_m.render("EXIT", True, WHITE)
        self.screen.blit(
            exit_txt,
            (
                self.exit_button.centerx - exit_txt.get_width() // 2,
                self.exit_button.centery - exit_txt.get_height() // 2,
            ),
        )

        if self.msg_timer > 0:
            msg_surf = self.font_s.render(self.message, True, GOLD)
            self.screen.blit(msg_surf, (w // 2 - msg_surf.get_width() // 2, 440))
            self.msg_timer -= 1

    def handle_click(self, pos):
        if self.exit_button.collidepoint(pos):
            return "EXIT"
        for item in self.items:
            if item["rect"].collidepoint(pos):
                if self.player.coins >= item["price"]:
                    self.player.coins -= item["price"]
                    self._update_inventory(item["id"])
                    self.message = f"Purchased {item['name']}!"
                    self.msg_timer = 90
                else:
                    self.message = "Not enough coins!"
                    self.msg_timer = 90
        return None

    def _update_inventory(self, item_id: str):
        if item_id == "skip":
            self.player.inventory["skips"] = self.player.inventory.get("skips", 0) + 1
        elif item_id == "fifty_fifty":
            self.player.inventory["fifty_fifty"] = self.player.inventory.get("fifty_fifty", 0) + 1
        elif item_id == "shield":
            self.player.inventory["shields"] = self.player.inventory.get("shields", 0) + 1
        elif item_id == "double":
            self.player.inventory["double_chance"] = self.player.inventory.get("double_chance", 0) + 1


# ================== Lobby（登录后、Jeopardy 前）==================
class Lobby:
    def __init__(self, player: "Player"):
        self.player = player
        self.shop = Shop(screen, player, WIDTH, HEIGHT)
        self.in_shop = False
        self.avatar_surf = None
        self._load_avatar()

    def _load_avatar(self):
        if not self.player.avatar_path:
            return
        p = self.player.avatar_path
        if not os.path.isfile(p):
            return
        try:
            img = pygame.image.load(p).convert_alpha()
            self.avatar_surf = pygame.transform.smoothscale(img, (72, 72))
        except pygame.error:
            self.avatar_surf = None

    def run(self) -> None:
        clock = pygame.time.Clock()
        while True:
            screen.fill(BLACK)
            if self.avatar_surf:
                screen.blit(self.avatar_surf, (20, 16))
                pygame.draw.rect(screen, GOLD, pygame.Rect(20, 16, 72, 72), 2)
            name_x = 108 if self.avatar_surf else 20
            screen.blit(LARGE.render(self.player.name, True, YELLOW), (name_x, 20))
            screen.blit(MEDIUM.render(f"Coins: {self.player.coins}", True, WHITE), (name_x, 72))
            screen.blit(
                SMALL.render("S: Shop  |  J: Start Jeopardy", True, GRAY),
                (name_x, 112),
            )

            if self.in_shop:
                self.shop.draw()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_s:
                        self.in_shop = not self.in_shop
                    elif e.key == pygame.K_j and not self.in_shop:
                        return
                if e.type == pygame.MOUSEBUTTONDOWN and self.in_shop:
                    if self.shop.handle_click(e.pos) == "EXIT":
                        self.in_shop = False

            pygame.display.flip()
            clock.tick(60)


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
    def __init__(self, name="User", coins=1000, inventory=None, avatar_path=None):
        self.name = name
        self.score = 0
        self.coins = coins
        self.inventory = inventory if inventory is not None else {}
        self.avatar_path = avatar_path

    def add_score(self, points):
        self.score += points

    def subtract_score(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0


# game running
class Game:
    def __init__(self, all_data: dict, player: Player | None = None):
        if "round1" not in all_data:
            print("Round 1 data doesn't exist.")  # check
            sys.exit(1)

        round1_data = all_data["round1"]

        categories = []  # categpries shown on the top of the board
        data_1 = {}  # dictionary that contains all questions in round 1

        for column, category in enumerate(round1_data):
            categories.append(category.get("name"))
            questions = category.get("questions")
            for row, items in enumerate(questions):
                data_1[(column, row)] = {"question_text": items["question"], "options": items["options"], "correct": items["correct"], "value": items["value"]}
        values = [items["value"] for items in round1_data[0]["questions"]]  # same value in each category

        self.categories = categories  # list[str]
        self.values = values  # list[int]
        self.rows = len(values)  # int
        self.cols = len(categories)  # int
        self.cell_width = WIDTH // self.cols  # int
        self.cell_height = (HEIGHT - 100) // (self.rows + 1)  # int

        self.board = Board(self.categories, self.values, data_1)
        if player is not None:
            self.player = player
            self.player.score = 0
        else:
            self.player = Player()

        # other state
        self.current_question_pos = None
        self.result_screen = False
        self.result_text = ""
        self.result_color = GREEN
        self.result_timer = 0
        self.question_screen = False
        self.game_over = False
        self.option_areas = []
        self.nextround = False  # turn TRUE when all questions has answered
        self.selected_option = -1  # which option is chosen
        self.timer = 5  # count down
        self.timer_running = False
        self.last_record = 0
        self.quit_screen = False
        self.quit_buttons_areas = []

    def control_events(self) -> bool:
        current_time = pygame.time.get_ticks()
        if self.timer_running and self.question_screen and not self.result_screen and not self.quit_screen:
            if current_time - self.last_record >= 1000:
                self.timer -= 1
                self.last_record = current_time
        if self.timer < 0 and self.question_screen and not self.result_screen:
            self.check_answer()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_screen = True
                    continue

                if self.quit_screen:
                    if event.key == pygame.K_y:
                        return False
                    elif event.key == pygame.K_n:
                        self.quit_screen = False
                        continue

                if self.question_screen and not self.result_screen and not self.quit_screen:  # use numbers on keyboard to control
                    if event.key == pygame.K_1:
                        self.selected_option = 0
                        self.check_answer()
                    elif event.key == pygame.K_2:
                        self.selected_option = 1
                        self.check_answer()
                    elif event.key == pygame.K_3:
                        self.selected_option = 2
                        self.check_answer()
                    elif event.key == pygame.K_4:
                        self.selected_option = 3
                        self.check_answer()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_screen:
                    for button in self.quit_buttons_areas:
                        if button["area"].collidepoint(event.pos):
                            if button["action"] == "quit":
                                return False          
                            elif button["action"] == "cancel":
                                self.quit_screen = False
                            break
                    continue

                if not self.question_screen and not self.game_over:
                    self.handle_click(pygame.mouse.get_pos())
                elif self.question_screen and not self.result_screen:
                    for i, region in enumerate(self.option_areas):
                        if region.collidepoint(event.pos):
                            self.selected_option = i
                            if self.selected_option != -1:
                                self.check_answer()
                                break
        return True

    def handle_click(self, position):  # position contains x coordinate and y coordinate
        x, y = position
        if y > 100:
            col = x // self.cell_width
            if (0 <= col < self.cols):
                col_y = y - 100
                row = col_y // self.cell_height - 1
                if (0 <= row < self.rows):
                    if not self.board.is_answered(row, col):
                        self.current_question_pos = (row, col)
                        self.question_screen = True
                        self.selected_option = -1
                        self.result_screen = False
                        self.timer = 5
                        self.timer_running = True
                        self.last_record = pygame.time.get_ticks()

    def check_answer(self):
        if self.current_question_pos is None:
            return

        self.timer_running = False
        self.timer = 0

        row, col = self.current_question_pos
        question = self.board.get_question(row, col)

        correct = question.check_answer(self.selected_option)
        if correct:
            self.player.add_score(question.value)
            self.result_text = f"Correct! +{question.value}"
            self.result_color = GREEN
        else:
            self.player.subtract_score(question.value)
            show_correct_answer = question.options[question.correct]
            self.result_text = f"Wrong! -{question.value} Correct answer: {show_correct_answer}"
            self.result_color = RED

        self.board.mark_answered(row, col)
        self.result_screen = True
        self.result_timer = 180

        if self.board.all_answered():
            self.game_over = True
            self.result_text = f"Next Round! Your score: {self.player.score}"

    def draw(self):
        screen.fill(BLACK)

        score_text = LARGE.render(
            f"{self.player.name}  |  Score: {self.player.score}", True, YELLOW
        )
        screen.blit(score_text, (20, 20))

        if self.question_screen and not self.result_screen and self.timer_running:
            timer_color = RED if self.timer <= 3 else WHITE
            timer_text = LARGE.render(f"Time: {self.timer}", True, timer_color)
            timer_text_pos = timer_text.get_rect(topright=(WIDTH - 400, 20))
            screen.blit(timer_text, timer_text_pos)

        if self.game_over:
            self.draw_game_over_screen()
        elif self.question_screen:
            if self.result_screen and self.result_timer > 0:
                self.draw_result()
                self.result_timer -= 1
                if self.result_timer <= 0:
                    self.question_screen = False
                    self.result_screen = False
                    self.current_question_pos = None
            else:
                self.draw_question_screen()
        else:
            self.draw_board_screen()

        if self.quit_screen:
            self.draw_quit_screen()

        pygame.display.flip()

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
                value_text = MEDIUM.render(str(self.values[row]), True, WHITE)
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

        value_text = MEDIUM.render(f"Value: {question.value}", True, YELLOW)
        value_text_pos = value_text.get_rect(center=(WIDTH // 2, 210))
        screen.blit(value_text, value_text_pos)

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
            pygame.draw.rect(screen, colors[i], rectangle)
            pygame.draw.rect(screen, WHITE, rectangle, 3)

            option_text = MEDIUM.render(option, True, BLACK)
            option_text_pos = option_text.get_rect(center=rectangle.center)
            screen.blit(option_text, option_text_pos)

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

    def draw_game_over_screen(self):
        overlay_gameover_screen = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        overlay_gameover_screen.set_alpha(200)
        overlay_gameover_screen.fill(BLACK)
        screen.blit(overlay_gameover_screen, (0, 0))

        game_over_text = LARGE.render("Game Over!", True, RED)
        game_over_text_pos = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(game_over_text, game_over_text_pos)

        score_text = LARGE.render(f"Final Score: {self.player.score}", True, YELLOW)
        score_text_pos = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_text, score_text_pos)

        restart_text = MEDIUM.render("Press ESC to quit", True, WHITE)
        restart_text_pos = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_text_pos)

    def draw_quit_screen(self):
        overlay_quit_screen = pygame.Surface((WIDTH, HEIGHT))
        overlay_quit_screen.set_alpha(0)
        overlay_quit_screen.fill(BLACK)
        screen.blit(overlay_quit_screen, (0, 0))

        dialog_width = 400
        dialog_height = 200
        dialog_rectangle = pygame.Rect(WIDTH//2 - dialog_width//2, HEIGHT//2 - dialog_height//2, dialog_width, dialog_height)
        pygame.draw.rect(screen, WHITE, dialog_rectangle)
        pygame.draw.rect(screen, BLACK, dialog_rectangle, 3)

        quit_text = MEDIUM.render("Do you really want to quit?", True, BLACK)
        quit_text_pos = quit_text.get_rect(center=(dialog_rectangle.centerx, dialog_rectangle.centery - 40))
        screen.blit(quit_text, quit_text_pos)

        button_width = 100
        button_height = 40
        yes_button_pos = pygame.Rect(dialog_rectangle.centerx - button_width - 20, dialog_rectangle.centery + 20, button_width, button_height)
        no_button_pos = pygame.Rect(dialog_rectangle.centerx + 20, dialog_rectangle.centery + 20, button_width, button_height)

        pygame.draw.rect(screen, GREEN, yes_button_pos)
        pygame.draw.rect(screen, RED, no_button_pos)
        pygame.draw.rect(screen, BLACK, yes_button_pos, 2)
        pygame.draw.rect(screen, BLACK, no_button_pos, 2)

        yes_text = MEDIUM.render("Yes", True, BLACK)
        no_text = MEDIUM.render("No", True, BLACK)
        screen.blit(yes_text, yes_text.get_rect(center=yes_button_pos.center))
        screen.blit(no_text, no_text.get_rect(center=no_button_pos.center))

        self.quit_buttons_areas = [{"area": yes_button_pos, "action": "quit"}, {"area": no_button_pos, "action": "cancel"}]

    def run(self):
        clock = pygame.time.Clock()
        fps = 60
        running = True
        while running:
            clock.tick(fps)
            running = self.control_events()
            self.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    login = LoginScreen()
    username, avatar_path = login.run()
    profile = Player(name=username, coins=1000, avatar_path=avatar_path)

    lobby = Lobby(profile)
    lobby.run()

    result = {}
    threading.Thread(target=generate_questions, args=(result,), daemon=True).start()
    while "all_data" not in result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        draw_loading_screen()

    game = Game(result["all_data"], player=profile)
    game.run()