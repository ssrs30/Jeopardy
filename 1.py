"""
Single Jeopardy, Double Jeopardy, Final Jeopardy
目前只做了single jeopardy
"""

import json
import pygame
import sys
import LLM


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


# question_data.json是临时用于测试的，之后要接入LLM


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

    def add_score(self, points):
        self.score += points

    def subtract_score(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0


# game running
class Game:
    def __init__(self):
        data = LLM.q_generate(LLM.prompt1)
        start = data.find("{")
        end = data.rfind("}") + 1
        if start == -1 or end == 0:
            return ValueError("No JSON object found")
        json_str = data[start:end]
        all_data = json.loads(json_str)

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

        score_text = LARGE.render(f"Score: {self.player.score}", True, YELLOW)
        screen.blit(score_text, (20, 20))

        if self.question_screen and not self.result_screen and self.timer_running:
            timer_color = RED if self.timer <= 3 else WHITE
            timer_text = LARGE.render(f"Time: {self.timer}", True, timer_color)
            timer_text_pos = timer_text.get_rect(topright=(WIDTH - 20, 20))
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

    def start_screen(self):
        start_screen = pygame.Surface((WIDTH, HEIGHT))

    def show_loading_screen(self):
        screen.fill(BLACK)
        text = LARGE.render("Generating questions with AI...", True, WHITE)
        text_pos = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_pos)
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

        q_text = LARGE.render(question.question_text, True, WHITE)
        q_text_pos = q_text.get_rect(center=(WIDTH // 2, 150))
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
    game = Game()
    game.run()
