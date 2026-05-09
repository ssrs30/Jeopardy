import pygame
import json
import threading
from pathlib import Path
import home
import pause
import char
import board
import loading
import question
import LLM

pygame.init()
pygame.font.init()

# windows = ["Quit", "Home", "Paused", "Char", "Board", "Loading", "Question", "Result"]
# num = [0, 1, 2, 3, 4, 5, 6, 7]

class Game:
    def __init__(self):
        self.running = True
        self.data_ready = False
        self.window_num = 5
        self.pre_window_num = 1
        self.round_no = 1
        self.category = -1
        self.question_no = -1

        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

        self.loading_window = loading.loading(self.screen)
        self.home_window = home.Homepage(self.screen)
        self.pause_window = pause.pause_window(self.screen)
        self.character_window = char.Character(self.screen)
        self.question_board = board.question_board(self.screen, self.round_no)
        self.question_window = question.Question(self.screen)

        current_dir = Path(__file__).parent
        self.player_name = ""
        self.player_char = current_dir / "Game Assets" / "Characters" / "c1.png"
    
    def _generate_questions(self):
        json_string = LLM.q_generate(LLM.prompt)
        self.question_list = json.loads(json_string)
        self.question_board.update_questions(self.question_list, 1)
        self.data_ready = True
    
    def run(self):
        threading.Thread(target = self._generate_questions(), daemon=True).start()

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
    
            if self.window_num == 0:
                self.running = False
            elif self.window_num == 1:
                self.window_num = self.home_window.update(events)
                self.home_window.draw()
                self.pre_window_num = 1
            elif self.window_num == 2:
                if self.pre_window_num == 1:
                    self.home_window.draw()
                elif self.pre_window_num == 3:
                    self.character_window.draw()

                self.window_num = self.pause_window.update(events, self.pre_window_num)
                self.pause_window.draw()
            elif self.window_num == 3:
                self.window_num = self.character_window.update(events)
                self.character_window.draw()
                self.pre_window_num = 3
            elif self.window_num == 4:
                self.window_num, self.category, self.question_no = self.question_board.update(events)
                self.question_window.update_question(self.round_no, self.question_list, (self.category, self.question_no))
                self.question_board.draw()
            elif self.window_num == 5:
                self.window_num = self.loading_window.update(events, self.data_ready)
                self.loading_window.draw()
            elif self.window_num == 6:
                self.window_num = self.question_window.update(events)
                self.question_window.draw()

    
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()