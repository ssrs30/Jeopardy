import json
import pygame
import sys
import os

# --- Initialization ---
pygame.init()

# Color and Font Configuration
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128) # For Shop UI

SMALL = pygame.font.Font(None, 24)
MEDIUM = pygame.font.Font(None, 36)
LARGE = pygame.font.Font(None, 48)

HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeopardy! Game System')

# ==================== 1. Login Screen Class ====================
class LoginScreen:
    def __init__(self):
        self.username = ""
        self.input_active = False
        self.avatar_folder = "avatar"
        self.selected_path = None
        self.avatars = []
        self.error_msg = ""
        
        # Ensure the avatar directory exists
        if not os.path.exists(self.avatar_folder):
            os.makedirs(self.avatar_folder)
        self.load_avatars()

    def load_avatars(self):
        """Scan the folder and load images as thumbnails"""
        self.avatars = []
        valid_exts = ('.png', '.jpg', '.jpeg')
        if os.path.exists(self.avatar_folder):
            files = [f for f in os.listdir(self.avatar_folder) if f.lower().endswith(valid_exts)]
            for f in files:
                path = os.path.join(self.avatar_folder, f)
                try:
                    img = pygame.image.load(path).convert_alpha()
                    display_img = pygame.transform.smoothscale(img, (60, 60))
                    self.avatars.append({"path": path, "img": display_img})
                except: continue

    def run(self):
        """Main loop for Login Screen"""
        clock = pygame.time.Clock()
        while True:
            screen.fill(WHITE)
            # Draw UI Elements
            title = LARGE.render("LOGIN SYSTEM", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            # Input Box
            input_rect = pygame.Rect(250, 150, 300, 40)
            pygame.draw.rect(screen, BLUE if self.input_active else GRAY, input_rect, 2)
            name_surf = MEDIUM.render(self.username, True, BLACK)
            screen.blit(name_surf, (input_rect.x + 5, input_rect.y + 5))
            
            # Avatar Grid
            screen.blit(SMALL.render("Select Your Avatar:", True, BLACK), (100, 220))
            avatar_rects = []
            for i, data in enumerate(self.avatars):
                x, y = 100 + (i % 8) * 75, 250 + (i // 8) * 75
                rect = pygame.Rect(x, y, 60, 60)
                avatar_rects.append((rect, data['path']))
                if self.selected_path == data['path']:
                    pygame.draw.rect(screen, GOLD, rect.inflate(10, 10), 3) # Highlight selected
                screen.blit(data['img'], (x, y))

            # Login Button
            btn_login = pygame.Rect(300, 480, 200, 50)
            pygame.draw.rect(screen, BLUE, btn_login)
            screen.blit(MEDIUM.render("START GAME", True, WHITE), (325, 490))
            
            if self.error_msg:
                screen.blit(SMALL.render(self.error_msg, True, RED), (300, 450))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos): self.input_active = True
                    else: self.input_active = False
                    
                    for rect, path in avatar_rects:
                        if rect.collidepoint(event.pos): self.selected_path = path
                        
                    if btn_login.collidepoint(event.pos):
                        if not self.username.strip(): self.error_msg = "Username required!"
                        elif not self.selected_path: self.error_msg = "Choose an avatar!"
                        else: return self.username, self.selected_path
                        
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                    else: self.username += event.unicode
            
            pygame.display.flip()
            clock.tick(60)

# ==================== 2. Player Class ====================
class Player:
    def __init__(self, name, avatar_path):
        self.name = name
        self.score = 0
        self.coins = 1000  # Initial coins
        self.skips = 0     # Number of skip items owned
        
        # Load and scale player avatar
        try:
            raw_img = pygame.image.load(avatar_path).convert_alpha()
            self.avatar_img = pygame.transform.smoothscale(raw_img, (50, 50))
        except:
            self.avatar_img = pygame.Surface((50, 50))
            self.avatar_img.fill(GRAY)

    def add_score(self, points): self.score += points
    def subtract_score(self, points): 
        self.score -= points
        if self.score < 0: self.score = 0

# ==================== 3. Game Logic Classes ====================
class Question:
    def __init__(self, text, value, options, correct):
        self.question_text = text
        self.value = value
        self.options = options
        self.correct = correct
        
    def check_answer(self, user_answer): return user_answer == self.correct

class Board:
    def __init__(self, categories, values, questions_dict):
        self.categories = categories
        self.values = values
        self.grid = [[None] * len(categories) for _ in range(len(values))]
        for (col, row), items in questions_dict.items():
            self.grid[row][col] = Question(items["question_text"], items["value"], items["options"], items["correct"])
        self.answered = [[False] * len(categories) for _ in range(len(values))]
    
    def all_answered(self): return all(all(row) for row in self.answered)

class Game:
    def __init__(self, username, avatar_path, questions_file="questions.json"):
        # Load question data from JSON
        try:
            with open(questions_file, 'r') as fp:
                all_data = json.load(fp)
        except:
            print("Error: Could not find or read questions.json"); sys.exit(1)

        round1_data = all_data["round1"]
        categories = [cat.get("name") for cat in round1_data]
        data_1 = {}
        for col, cat in enumerate(round1_data):
            for row, q in enumerate(cat.get("questions")):
                data_1[(col, row)] = {"question_text": q["question"], "options": q["options"], "correct": q["correct"], "value": q["value"]}
        
        self.board = Board(categories, [q["value"] for q in round1_data[0]["questions"]], data_1)
        self.player = Player(username, avatar_path)
        
        # Dynamic grid sizing
        self.cell_width = WIDTH // len(categories)
        self.cell_height = (HEIGHT - 120) // (len(self.board.values) + 1)

        # Game States: MAIN, QUESTION, SHOP, GAMEOVER
        self.state = "MAIN" 
        self.current_q_pos = None
        self.show_result = False
        self.result_text = ""
        self.result_timer = 0
        self.option_areas = []

    def draw(self):
        """Master draw function based on game state"""
        screen.fill(BLACK)
        
        # Header Info: Avatar, Name, Score, Coins
        screen.blit(self.player.avatar_img, (20, 10))
        info_txt = SMALL.render(f"{self.player.name} | Coins: {self.player.coins} | Skips: {self.player.skips}", True, WHITE)
        screen.blit(info_txt, (80, 15))
        score_txt = MEDIUM.render(f"Score: {self.player.score}", True, YELLOW)
        screen.blit(score_txt, (80, 40))

        if self.state == "MAIN":
            self.draw_board_screen()
        elif self.state == "QUESTION":
            if self.show_result: self.draw_result()
            else: self.draw_question_screen()
        elif self.state == "SHOP":
            self.draw_shop_screen()
        elif self.state == "GAMEOVER":
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_board_screen(self):
        """Draw the main Jeopardy grid and Shop button"""
        self.btn_shop = pygame.Rect(WIDTH - 120, 20, 100, 40)
        pygame.draw.rect(screen, PURPLE, self.btn_shop)
        screen.blit(SMALL.render("SHOP", True, WHITE), (WIDTH - 90, 30))

        for col in range(len(self.board.categories)):
            # Category headers
            rect = pygame.Rect(col * self.cell_width, 100, self.cell_width, self.cell_height)
            pygame.draw.rect(screen, BLUE, rect); pygame.draw.rect(screen, WHITE, rect, 1)
            txt = SMALL.render(self.board.categories[col], True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))
            
            # Money values
            for row in range(len(self.board.values)):
                y = 100 + self.cell_height * (row + 1)
                rect = pygame.Rect(col * self.cell_width, y, self.cell_width, self.cell_height)
                color = GRAY if self.board.answered[row][col] else BLUE
                pygame.draw.rect(screen, color, rect); pygame.draw.rect(screen, WHITE, rect, 1)
                val = MEDIUM.render(str(self.board.values[row]), True, WHITE)
                screen.blit(val, val.get_rect(center=rect.center))

    def draw_shop_screen(self):
        """Draw the Currency Shop UI"""
        title = LARGE.render("GAME SHOP", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        
        # Item purchase button
        self.btn_buy_skip = pygame.Rect(200, 250, 400, 80)
        pygame.draw.rect(screen, BLUE, self.btn_buy_skip)
        screen.blit(MEDIUM.render("Buy 'Skip Token' - 500 Coins", True, WHITE), (250, 275))
        
        self.btn_exit_shop = pygame.Rect(300, 450, 200, 50)
        pygame.draw.rect(screen, GRAY, self.btn_exit_shop)
        screen.blit(MEDIUM.render("BACK", True, BLACK), (365, 460))

    def draw_question_screen(self):
        """Draw current question and options"""
        row, col = self.current_q_pos
        q = self.board.grid[row][col]
        q_surf = MEDIUM.render(q.question_text, True, WHITE)
        screen.blit(q_surf, q_surf.get_rect(center=(WIDTH//2, 150)))
        
        # Use Skip Token Button (visible if player has skips)
        self.btn_use_skip = pygame.Rect(WIDTH - 150, HEIGHT - 80, 130, 50)
        if self.player.skips > 0:
            pygame.draw.rect(screen, ORANGE, self.btn_use_skip)
            screen.blit(SMALL.render("USE SKIP", True, BLACK), (WIDTH - 120, HEIGHT - 65))

        self.option_areas = []
        for i, opt in enumerate(q.options):
            rect = pygame.Rect(WIDTH//2 - 250, 220 + i*70, 500, 50)
            self.option_areas.append(rect)
            pygame.draw.rect(screen, BLUE, rect); pygame.draw.rect(screen, WHITE, rect, 2)
            screen.blit(SMALL.render(opt, True, WHITE), (rect.x + 20, rect.y + 15))

    def draw_result(self):
        """Display feedback after answering"""
        txt = LARGE.render(self.result_text, True, GOLD)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
        self.result_timer -= 1
        if self.result_timer <= 0:
            self.show_result = False
            self.state = "MAIN"
            if self.board.all_answered(): 
                self.state = "GAMEOVER"
                self.player.coins += 1000 # Reward for game completion

    def draw_game_over_screen(self):
        """End of game reward screen"""
        txt = LARGE.render(f"GAME CLEAR! Reward +1000 Coins", True, GREEN)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, 250)))
        score = MEDIUM.render(f"Final Score: {self.player.score}", True, WHITE)
        screen.blit(score, score.get_rect(center=(WIDTH//2, 320)))

    def control_events(self):
        """Handle all mouse and keyboard inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.state == "MAIN":
                    if self.btn_shop.collidepoint(pos): self.state = "SHOP"
                    else:
                        col = pos[0] // self.cell_width
                        row = (pos[1] - 100) // self.cell_height - 1
                        if 0 <= col < len(self.board.categories) and 0 <= row < len(self.board.values):
                            if not self.board.answered[row][col]:
                                self.current_q_pos = (row, col)
                                self.state = "QUESTION"
                                
                elif self.state == "SHOP":
                    if self.btn_exit_shop.collidepoint(pos): self.state = "MAIN"
                    if self.btn_buy_skip.collidepoint(pos) and self.player.coins >= 500:
                        self.player.coins -= 500
                        self.player.skips += 1
                        
                elif self.state == "QUESTION" and not self.show_result:
                    if self.player.skips > 0 and self.btn_use_skip.collidepoint(pos):
                        self.player.skips -= 1
                        self.handle_answer(is_skip=True)
                    for i, area in enumerate(self.option_areas):
                        if area.collidepoint(pos): self.handle_answer(i)
        return True

    def handle_answer(self, index=None, is_skip=False):
        """Process question outcome"""
        row, col = self.current_q_pos
        q = self.board.grid[row][col]
        if is_skip:
            self.result_text = "QUESTION SKIPPED!"
        else:
            if q.check_answer(index):
                self.player.add_score(q.value)
                self.result_text = f"CORRECT! +{q.value}"
            else:
                self.player.subtract_score(q.value)
                self.result_text = f"WRONG! -{q.value}"
        
        self.board.answered[row][col] = True
        self.show_result = True
        self.result_timer = 90 # Frame duration for result screen

    def run(self):
        """Game execution loop"""
        clock = pygame.time.Clock()
        while self.control_events():
            self.draw()
            clock.tick(60)
        pygame.quit(); sys.exit()

# ==================== 4. Execution Logic ====================
if __name__ == "__main__":
    # 1. Start with Login screen
    login = LoginScreen()
    user_name, avatar_path = login.run()
    
    # 2. Start game with login data
    game = Game(username=user_name, avatar_path=avatar_path)
    game.run()