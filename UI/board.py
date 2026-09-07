import pygame
import pygame.freetype
from pathlib import Path

from .assets import load_font, load_image, load_sound, play_music

pygame.init()
pygame.font.init()
pygame.mixer.init()

class question_board:
    """include categories, values, and cell pick"""

    def __init__(self, screen, round_no):
        self.screen = screen
        self.round_no = round_no

        self.font = load_font(30)
        self.button_sound = load_sound("Sound Effect", "button.mp3")
        self.music_started = False

        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.frame_player = load_image("Game Assets", "frame_player.png", size=(280, 90), label="P")
        self.frame_AI = load_image("Game Assets", "frame_AI.png", size=(200, 50), label="AI")

        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

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

        self.board = load_image("Game Assets", "board.png", size=(160, 70), label="")
        self.board_pressed = load_image("Game Assets", "board_pressed.png", size=(160, 70), label="")
        self.board_grey = load_image("Game Assets", "board_grey.png", size=(160, 70), label="")

        self.board01_rect = self.board.get_rect(center = (155, 250))
        self.board02_rect = self.board.get_rect(center = (333, 250))
        self.board03_rect = self.board.get_rect(center = (511, 250))
        self.board04_rect = self.board.get_rect(center = (689, 250))
        self.board05_rect = self.board.get_rect(center = (867, 250))
        self.board06_rect = self.board.get_rect(center = (1045, 250))
        self.board11_rect = self.board.get_rect(center = (155, 330))
        self.board12_rect = self.board.get_rect(center = (333, 330))
        self.board13_rect = self.board.get_rect(center = (511, 330))
        self.board14_rect = self.board.get_rect(center = (689, 330))
        self.board15_rect = self.board.get_rect(center = (867, 330))
        self.board16_rect = self.board.get_rect(center = (1045, 330))
        self.board21_rect = self.board.get_rect(center = (155, 410))
        self.board22_rect = self.board.get_rect(center = (333, 410))
        self.board23_rect = self.board.get_rect(center = (511, 410))
        self.board24_rect = self.board.get_rect(center = (689, 410))
        self.board25_rect = self.board.get_rect(center = (867, 410))
        self.board26_rect = self.board.get_rect(center = (1045, 410))
        self.board31_rect = self.board.get_rect(center = (155, 490))
        self.board32_rect = self.board.get_rect(center = (333, 490))
        self.board33_rect = self.board.get_rect(center = (511, 490))
        self.board34_rect = self.board.get_rect(center = (689, 490))
        self.board35_rect = self.board.get_rect(center = (867, 490))
        self.board36_rect = self.board.get_rect(center = (1045, 490))
        self.board41_rect = self.board.get_rect(center = (155, 570))
        self.board42_rect = self.board.get_rect(center = (333, 570))
        self.board43_rect = self.board.get_rect(center = (511, 570))
        self.board44_rect = self.board.get_rect(center = (689, 570))
        self.board45_rect = self.board.get_rect(center = (867, 570))
        self.board46_rect = self.board.get_rect(center = (1045, 570))
        self.board51_rect = self.board.get_rect(center = (155, 650))
        self.board52_rect = self.board.get_rect(center = (333, 650))
        self.board53_rect = self.board.get_rect(center = (511, 650))
        self.board54_rect = self.board.get_rect(center = (689, 650))
        self.board55_rect = self.board.get_rect(center = (867, 650))
        self.board56_rect = self.board.get_rect(center = (1045, 650))

        self.board11_pressed = False
        self.board12_pressed = False
        self.board13_pressed = False
        self.board14_pressed = False
        self.board15_pressed = False
        self.board16_pressed = False
        self.board21_pressed = False
        self.board22_pressed = False
        self.board23_pressed = False
        self.board24_pressed = False
        self.board25_pressed = False
        self.board26_pressed = False
        self.board31_pressed = False
        self.board32_pressed = False
        self.board33_pressed = False
        self.board34_pressed = False
        self.board35_pressed = False
        self.board36_pressed = False
        self.board41_pressed = False
        self.board42_pressed = False
        self.board43_pressed = False
        self.board44_pressed = False
        self.board45_pressed = False
        self.board46_pressed = False
        self.board51_pressed = False
        self.board52_pressed = False
        self.board53_pressed = False
        self.board54_pressed = False
        self.board55_pressed = False
        self.board56_pressed = False

        self.player_name = ""
        self.player_score = 0
        self.AI_score1 = 0
        self.AI_score2 = 0


    def update_questions(self, questions: list, round_no):
        """Update and sort question data"""
        self.questions = questions
        self._sort_questions(round_no)
    
    def update_character(self, player_name, char_path):
        """Load player name and character."""
        self.player_name = player_name
        try:
            self.char = pygame.image.load(str(char_path)).convert_alpha()
        except Exception:
            self.char = load_image("Game Assets", "Characters", "c1.png", size=(80, 80), label="P")

    def update_score(self, player_score, AI_score1, AI_score2):
        """Update scores shown next to human and AI labels"""
        self.player_score = player_score
        self.AI_score1 = AI_score1
        self.AI_score2 = AI_score2

    def update(self, events) -> tuple[int]:
        """Handle music, hover and clicks. Return command to Client."""
        if not self.music_started:
            play_music("Sound Effect", "Game_BGM.mp3")
            self.music_started = True
            
        mouse_pos = pygame.mouse.get_pos()

        if self.board11_pressed:
            self.current_board11 = self.board_grey
        elif self.board11_rect.collidepoint(mouse_pos):
            self.current_board11 = self.board_pressed
        else:
            self.current_board11 = self.board

        if self.board12_pressed:
            self.current_board12 = self.board_grey
        elif self.board12_rect.collidepoint(mouse_pos):
            self.current_board12 = self.board_pressed
        else:
            self.current_board12 = self.board

        if self.board13_pressed:
            self.current_board13 = self.board_grey
        elif self.board13_rect.collidepoint(mouse_pos):
            self.current_board13 = self.board_pressed
        else:
            self.current_board13 = self.board

        if self.board14_pressed:
            self.current_board14 = self.board_grey
        elif self.board14_rect.collidepoint(mouse_pos):
            self.current_board14 = self.board_pressed
        else:
            self.current_board14 = self.board

        if self.board15_pressed:
            self.current_board15 = self.board_grey
        elif self.board15_rect.collidepoint(mouse_pos):
            self.current_board15 = self.board_pressed
        else:
            self.current_board15 = self.board

        if self.board16_pressed:
            self.current_board16 = self.board_grey
        elif self.board16_rect.collidepoint(mouse_pos):
            self.current_board16 = self.board_pressed
        else:
            self.current_board16 = self.board

        if self.board21_pressed:
            self.current_board21 = self.board_grey
        elif self.board21_rect.collidepoint(mouse_pos):
            self.current_board21 = self.board_pressed
        else:
            self.current_board21 = self.board

        if self.board22_pressed:
            self.current_board22 = self.board_grey
        elif self.board22_rect.collidepoint(mouse_pos):
            self.current_board22 = self.board_pressed
        else:
            self.current_board22 = self.board

        if self.board23_pressed:
            self.current_board23 = self.board_grey
        elif self.board23_rect.collidepoint(mouse_pos):
            self.current_board23 = self.board_pressed
        else:
            self.current_board23 = self.board

        if self.board24_pressed:
            self.current_board24 = self.board_grey
        elif self.board24_rect.collidepoint(mouse_pos):
            self.current_board24 = self.board_pressed
        else:
            self.current_board24 = self.board

        if self.board25_pressed:
            self.current_board25 = self.board_grey
        elif self.board25_rect.collidepoint(mouse_pos):
            self.current_board25 = self.board_pressed
        else:
            self.current_board25 = self.board

        if self.board26_pressed:
            self.current_board26 = self.board_grey
        elif self.board26_rect.collidepoint(mouse_pos):
            self.current_board26 = self.board_pressed
        else:
            self.current_board26 = self.board

        if self.board31_pressed:
            self.current_board31 = self.board_grey
        elif self.board31_rect.collidepoint(mouse_pos):
            self.current_board31 = self.board_pressed
        else:
            self.current_board31 = self.board

        if self.board32_pressed:
            self.current_board32 = self.board_grey
        elif self.board32_rect.collidepoint(mouse_pos):
            self.current_board32 = self.board_pressed
        else:
            self.current_board32 = self.board

        if self.board33_pressed:
            self.current_board33 = self.board_grey
        elif self.board33_rect.collidepoint(mouse_pos):
            self.current_board33 = self.board_pressed
        else:
            self.current_board33 = self.board

        if self.board34_pressed:
            self.current_board34 = self.board_grey
        elif self.board34_rect.collidepoint(mouse_pos):
            self.current_board34 = self.board_pressed
        else:
            self.current_board34 = self.board

        if self.board35_pressed:
            self.current_board35 = self.board_grey
        elif self.board35_rect.collidepoint(mouse_pos):
            self.current_board35 = self.board_pressed
        else:
            self.current_board35 = self.board

        if self.board36_pressed:
            self.current_board36 = self.board_grey
        elif self.board36_rect.collidepoint(mouse_pos):
            self.current_board36 = self.board_pressed
        else:
            self.current_board36 = self.board

        if self.board41_pressed:
            self.current_board41 = self.board_grey
        elif self.board41_rect.collidepoint(mouse_pos):
            self.current_board41 = self.board_pressed
        else:
            self.current_board41 = self.board

        if self.board42_pressed:
            self.current_board42 = self.board_grey
        elif self.board42_rect.collidepoint(mouse_pos):
            self.current_board42 = self.board_pressed
        else:
            self.current_board42 = self.board

        if self.board43_pressed:
            self.current_board43 = self.board_grey
        elif self.board43_rect.collidepoint(mouse_pos):
            self.current_board43 = self.board_pressed
        else:
            self.current_board43 = self.board

        if self.board44_pressed:
            self.current_board44 = self.board_grey
        elif self.board44_rect.collidepoint(mouse_pos):
            self.current_board44 = self.board_pressed
        else:
            self.current_board44 = self.board

        if self.board45_pressed:
            self.current_board45 = self.board_grey
        elif self.board45_rect.collidepoint(mouse_pos):
            self.current_board45 = self.board_pressed
        else:
            self.current_board45 = self.board

        if self.board46_pressed:
            self.current_board46 = self.board_grey
        elif self.board46_rect.collidepoint(mouse_pos):
            self.current_board46 = self.board_pressed
        else:
            self.current_board46 = self.board

        if self.board51_pressed:
            self.current_board51 = self.board_grey
        elif self.board51_rect.collidepoint(mouse_pos):
            self.current_board51 = self.board_pressed
        else:
            self.current_board51 = self.board

        if self.board52_pressed:
            self.current_board52 = self.board_grey
        elif self.board52_rect.collidepoint(mouse_pos):
            self.current_board52 = self.board_pressed
        else:
            self.current_board52 = self.board

        if self.board53_pressed:
            self.current_board53 = self.board_grey
        elif self.board53_rect.collidepoint(mouse_pos):
            self.current_board53 = self.board_pressed
        else:
            self.current_board53 = self.board

        if self.board54_pressed:
            self.current_board54 = self.board_grey
        elif self.board54_rect.collidepoint(mouse_pos):
            self.current_board54 = self.board_pressed
        else:
            self.current_board54 = self.board

        if self.board55_pressed:
            self.current_board55 = self.board_grey
        elif self.board55_rect.collidepoint(mouse_pos):
            self.current_board55 = self.board_pressed
        else:
            self.current_board55 = self.board

        if self.board56_pressed:
            self.current_board56 = self.board_grey
        elif self.board56_rect.collidepoint(mouse_pos):
            self.current_board56 = self.board_pressed
        else:
            self.current_board56 = self.board

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
                if not self.board11_pressed and self.board11_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board11_pressed = True
                    return 8, 0, 0
                if not self.board12_pressed and self.board12_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board12_pressed = True
                    return 8, 0, 1
                if not self.board13_pressed and self.board13_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board13_pressed = True
                    return 8, 0, 2
                if not self.board14_pressed and self.board14_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board14_pressed = True
                    return 8, 0, 3
                if not self.board15_pressed and self.board15_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board15_pressed = True
                    return 8, 0, 4
                if not self.board16_pressed and self.board16_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board16_pressed = True
                    return 8, 0, 5
                if not self.board21_pressed and self.board21_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board21_pressed = True
                    return 8, 1, 0
                if not self.board22_pressed and self.board22_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board22_pressed = True
                    return 8, 1, 1
                if not self.board23_pressed and self.board23_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board23_pressed = True
                    return 8, 1, 2
                if not self.board24_pressed and self.board24_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board24_pressed = True
                    return 8, 1, 3
                if not self.board25_pressed and self.board25_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board25_pressed = True
                    return 8, 1, 4
                if not self.board26_pressed and self.board26_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board26_pressed = True
                    return 8, 1, 5
                if not self.board31_pressed and self.board31_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board31_pressed = True
                    return 8, 2, 0
                if not self.board32_pressed and self.board32_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board32_pressed = True
                    return 8, 2, 1
                if not self.board33_pressed and self.board33_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board33_pressed = True
                    return 8, 2, 2
                if not self.board34_pressed and self.board34_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board34_pressed = True
                    return 8, 2, 3
                if not self.board35_pressed and self.board35_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board35_pressed = True
                    return 8, 2, 4
                if not self.board36_pressed and self.board36_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board36_pressed = True
                    return 8, 2, 5
                if not self.board41_pressed and self.board41_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board41_pressed = True
                    return 8, 3, 0
                if not self.board42_pressed and self.board42_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board42_pressed = True
                    return 8, 3, 1
                if not self.board43_pressed and self.board43_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board43_pressed = True
                    return 8, 3, 2
                if not self.board44_pressed and self.board44_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board44_pressed = True
                    return 8, 3, 3
                if not self.board45_pressed and self.board45_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board45_pressed = True
                    return 8, 3, 4
                if not self.board46_pressed and self.board46_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board46_pressed = True
                    return 8, 3, 5
                if not self.board51_pressed and self.board51_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board51_pressed = True
                    return 8, 4, 0
                if not self.board52_pressed and self.board52_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board52_pressed = True
                    return 8, 4, 1
                if not self.board53_pressed and self.board53_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board53_pressed = True
                    return 8, 4, 2
                if not self.board54_pressed and self.board54_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board54_pressed = True
                    return 8, 4, 3
                if not self.board55_pressed and self.board55_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board55_pressed = True
                    return 8, 4, 4
                if not self.board56_pressed and self.board56_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board56_pressed = True
                    return 8, 4, 5

                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2, -1, -1
                if self.top_button_items_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 11, -1, -1
                if self.top_button_shop_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 10, -1, -1
        
        return 6, -1, -1
            
    def _sort_questions(self, round_no: int):
        """Fill category names and values grid from self.questions"""
        self.round_questions = self.questions[f"round{round_no}"]
        self.category = []
        self.values = [[] for k in range(6)]
        for i in range(0, 6):
            self.category.append(self.round_questions[i]["name"])
            for j in range(0, 5):
                self.values[i].append(self.round_questions[i]["questions"][j]["value"])

    def draw(self):
        """Draw full board"""
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.frame_player, (15, 10))
        self.screen.blit(self.frame_AI, (350, 20))
        self.screen.blit(self.frame_AI, (350, 80))
        self.screen.blit(self.char, (55, 40))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.font.render_to(self.screen, (150, 45), self.player_name, (255, 255, 255))
        self.font.render_to(self.screen, (150, 80), str(self.player_score), (255, 255, 255))
        self.font.render_to(self.screen, (365, 38), "AI1", (255, 255, 255))
        self.font.render_to(self.screen, (365, 98), "AI2", (255, 255, 255))
        self.font.render_to(self.screen, (420, 38), str(self.AI_score1), (255, 255, 255))
        self.font.render_to(self.screen, (420, 98), str(self.AI_score2), (255, 255, 255))

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        self.screen.blit(self.board, self.board01_rect)
        self.screen.blit(self.board, self.board02_rect)
        self.screen.blit(self.board, self.board03_rect)
        self.screen.blit(self.board, self.board04_rect)
        self.screen.blit(self.board, self.board05_rect)
        self.screen.blit(self.board, self.board06_rect)
        self.screen.blit(self.current_board11, self.board11_rect)
        self.screen.blit(self.current_board12, self.board12_rect)
        self.screen.blit(self.current_board13, self.board13_rect)
        self.screen.blit(self.current_board14, self.board14_rect)
        self.screen.blit(self.current_board15, self.board15_rect)
        self.screen.blit(self.current_board16, self.board16_rect)
        self.screen.blit(self.current_board21, self.board21_rect)
        self.screen.blit(self.current_board22, self.board22_rect)
        self.screen.blit(self.current_board23, self.board23_rect)
        self.screen.blit(self.current_board24, self.board24_rect)
        self.screen.blit(self.current_board25, self.board25_rect)
        self.screen.blit(self.current_board26, self.board26_rect)
        self.screen.blit(self.current_board31, self.board31_rect)
        self.screen.blit(self.current_board32, self.board32_rect)
        self.screen.blit(self.current_board33, self.board33_rect)
        self.screen.blit(self.current_board34, self.board34_rect)
        self.screen.blit(self.current_board35, self.board35_rect)
        self.screen.blit(self.current_board36, self.board36_rect)
        self.screen.blit(self.current_board41, self.board41_rect)
        self.screen.blit(self.current_board42, self.board42_rect)
        self.screen.blit(self.current_board43, self.board43_rect)
        self.screen.blit(self.current_board44, self.board44_rect)
        self.screen.blit(self.current_board45, self.board45_rect)
        self.screen.blit(self.current_board46, self.board46_rect)
        self.screen.blit(self.current_board51, self.board51_rect)
        self.screen.blit(self.current_board52, self.board52_rect)
        self.screen.blit(self.current_board53, self.board53_rect)
        self.screen.blit(self.current_board54, self.board54_rect)
        self.screen.blit(self.current_board55, self.board55_rect)
        self.screen.blit(self.current_board56, self.board56_rect)

        self.text01, self.text01_rect = self.font.render(self.category[0], (255, 255, 255))
        self.text01_rect.center = self.board01_rect.center
        self.screen.blit(self.text01, self.text01_rect)
        self.text02, self.text02_rect = self.font.render(self.category[1], (255, 255, 255))
        self.text02_rect.center = self.board02_rect.center
        self.screen.blit(self.text02, self.text02_rect)
        self.text03, self.text03_rect = self.font.render(self.category[2], (255, 255, 255))
        self.text03_rect.center = self.board03_rect.center
        self.screen.blit(self.text03, self.text03_rect)
        self.text04, self.text04_rect = self.font.render(self.category[3], (255, 255, 255))
        self.text04_rect.center = self.board04_rect.center
        self.screen.blit(self.text04, self.text04_rect)
        self.text05, self.text05_rect = self.font.render(self.category[4], (255, 255, 255))
        self.text05_rect.center = self.board05_rect.center
        self.screen.blit(self.text05, self.text05_rect)
        self.text06, self.text06_rect = self.font.render(self.category[5], (255, 255, 255))
        self.text06_rect.center = self.board06_rect.center
        self.screen.blit(self.text06, self.text06_rect)
        self.text11, self.text11_rect = self.font.render(str(self.values[0][0]), (255, 255, 255))
        self.text11_rect.center = self.board11_rect.center
        self.screen.blit(self.text11, self.text11_rect)
        self.text12, self.text12_rect = self.font.render(str(self.values[1][0]), (255, 255, 255))
        self.text12_rect.center = self.board12_rect.center
        self.screen.blit(self.text12, self.text12_rect)
        self.text13, self.text13_rect = self.font.render(str(self.values[2][0]), (255, 255, 255))
        self.text13_rect.center = self.board13_rect.center
        self.screen.blit(self.text13, self.text13_rect)
        self.text14, self.text14_rect = self.font.render(str(self.values[3][0]), (255, 255, 255))
        self.text14_rect.center = self.board14_rect.center
        self.screen.blit(self.text14, self.text14_rect)
        self.text15, self.text15_rect = self.font.render(str(self.values[4][0]), (255, 255, 255))
        self.text15_rect.center = self.board15_rect.center
        self.screen.blit(self.text15, self.text15_rect)
        self.text16, self.text16_rect = self.font.render(str(self.values[5][0]), (255, 255, 255))
        self.text16_rect.center = self.board16_rect.center
        self.screen.blit(self.text16, self.text16_rect)
        self.text21, self.text21_rect = self.font.render(str(self.values[0][1]), (255, 255, 255))
        self.text21_rect.center = self.board21_rect.center
        self.screen.blit(self.text21, self.text21_rect)
        self.text22, self.text22_rect = self.font.render(str(self.values[1][1]), (255, 255, 255))
        self.text22_rect.center = self.board22_rect.center
        self.screen.blit(self.text22, self.text22_rect)
        self.text23, self.text23_rect = self.font.render(str(self.values[2][1]), (255, 255, 255))
        self.text23_rect.center = self.board23_rect.center
        self.screen.blit(self.text23, self.text23_rect)
        self.text24, self.text24_rect = self.font.render(str(self.values[3][1]), (255, 255, 255))
        self.text24_rect.center = self.board24_rect.center
        self.screen.blit(self.text24, self.text24_rect)
        self.text25, self.text25_rect = self.font.render(str(self.values[4][1]), (255, 255, 255))
        self.text25_rect.center = self.board25_rect.center
        self.screen.blit(self.text25, self.text25_rect)
        self.text26, self.text26_rect = self.font.render(str(self.values[5][1]), (255, 255, 255))
        self.text26_rect.center = self.board26_rect.center
        self.screen.blit(self.text26, self.text26_rect)
        self.text31, self.text31_rect = self.font.render(str(self.values[0][2]), (255, 255, 255))
        self.text31_rect.center = self.board31_rect.center
        self.screen.blit(self.text31, self.text31_rect)
        self.text32, self.text32_rect = self.font.render(str(self.values[1][2]), (255, 255, 255))
        self.text32_rect.center = self.board32_rect.center
        self.screen.blit(self.text32, self.text32_rect)
        self.text33, self.text33_rect = self.font.render(str(self.values[2][2]), (255, 255, 255))
        self.text33_rect.center = self.board33_rect.center
        self.screen.blit(self.text33, self.text33_rect)
        self.text34, self.text34_rect = self.font.render(str(self.values[3][2]), (255, 255, 255))
        self.text34_rect.center = self.board34_rect.center
        self.screen.blit(self.text34, self.text34_rect)
        self.text35, self.text35_rect = self.font.render(str(self.values[4][2]), (255, 255, 255))
        self.text35_rect.center = self.board35_rect.center
        self.screen.blit(self.text35, self.text35_rect)
        self.text36, self.text36_rect = self.font.render(str(self.values[5][2]), (255, 255, 255))
        self.text36_rect.center = self.board36_rect.center
        self.screen.blit(self.text36, self.text36_rect)
        self.text41, self.text41_rect = self.font.render(str(self.values[0][3]), (255, 255, 255))
        self.text41_rect.center = self.board41_rect.center
        self.screen.blit(self.text41, self.text41_rect)
        self.text42, self.text42_rect = self.font.render(str(self.values[1][3]), (255, 255, 255))
        self.text42_rect.center = self.board42_rect.center
        self.screen.blit(self.text42, self.text42_rect)
        self.text43, self.text43_rect = self.font.render(str(self.values[2][3]), (255, 255, 255))
        self.text43_rect.center = self.board43_rect.center
        self.screen.blit(self.text43, self.text43_rect)
        self.text44, self.text44_rect = self.font.render(str(self.values[3][3]), (255, 255, 255))
        self.text44_rect.center = self.board44_rect.center
        self.screen.blit(self.text44, self.text44_rect)
        self.text45, self.text45_rect = self.font.render(str(self.values[4][3]), (255, 255, 255))
        self.text45_rect.center = self.board45_rect.center
        self.screen.blit(self.text45, self.text45_rect)
        self.text46, self.text46_rect = self.font.render(str(self.values[5][3]), (255, 255, 255))
        self.text46_rect.center = self.board46_rect.center
        self.screen.blit(self.text46, self.text46_rect)
        self.text51, self.text51_rect = self.font.render(str(self.values[0][4]), (255, 255, 255))
        self.text51_rect.center = self.board51_rect.center
        self.screen.blit(self.text51, self.text51_rect)
        self.text52, self.text52_rect = self.font.render(str(self.values[1][4]), (255, 255, 255))
        self.text52_rect.center = self.board52_rect.center
        self.screen.blit(self.text52, self.text52_rect)
        self.text53, self.text53_rect = self.font.render(str(self.values[2][4]), (255, 255, 255))
        self.text53_rect.center = self.board53_rect.center
        self.screen.blit(self.text53, self.text53_rect)
        self.text54, self.text54_rect = self.font.render(str(self.values[3][4]), (255, 255, 255))
        self.text54_rect.center = self.board54_rect.center
        self.screen.blit(self.text54, self.text54_rect)
        self.text55, self.text55_rect = self.font.render(str(self.values[4][4]), (255, 255, 255))
        self.text55_rect.center = self.board55_rect.center
        self.screen.blit(self.text55, self.text55_rect)
        self.text56, self.text56_rect = self.font.render(str(self.values[5][4]), (255, 255, 255))
        self.text56_rect.center = self.board56_rect.center
        self.screen.blit(self.text56, self.text56_rect)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    char_path = Path(__file__).parent / "Game Assets" / "Characters" / "c1.png"
    question = question_board(screen, 1)
    clock = pygame.time.Clock()
    num = 4
    running = True

    with open(Path(__file__).parent / "questions.json", "r") as file:
        questions = json.load(file)
    question.update_questions(questions, 1)
    question.update_character("Happy",char_path)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 4:
            num, cat, val = question.update(events)
            question.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()