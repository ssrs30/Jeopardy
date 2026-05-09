import pygame
import pygame.freetype
from pathlib import Path
import json

pygame.init()
pygame.font.init()
pygame.mixer.init()

class question_board:
    def __init__(self, screen, round_no):
        self.screen = screen
        self.round_no = round_no
        
        current_dir = Path(__file__).parent
        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 30)
        bg_path = current_dir / "Game Assets" / "bg.png"
        board_path = current_dir / "Game Assets" / "board.png"
        board_pressed_path = current_dir / "Game Assets" / "board_pressed.png"
        board_grey_path = current_dir / "Game Assets" / "board_grey.png"
        frame_player_path = current_dir / "Game Assets" / "frame_player.png"
        frame_AI_path = current_dir / "Game Assets" / "frame_AI.png"
        quit_button_path = current_dir / "Game Assets" / "quit_button.png"
        items_path = current_dir / "Game Assets" / "ITEMS.png"
        items_pressed_path = current_dir / "Game Assets" / "ITEMS_pressed.png"
        shop_path = current_dir / "Game Assets" / "SHOP.png"
        shop_pressed_path = current_dir / "Game Assets" / "SHOP_pressed.png"
        top_button_path = current_dir / "Game Assets" / "top_button.png"
        top_button_pressed_path = current_dir / "Game Assets" / "top_button_pressed.png"

        self.bg_music_path = current_dir / "Sound Effect" / "Game_BGM.mp3"
        button_sound_path = current_dir / "Sound Effect" / "button.mp3"
        self.button_sound = pygame.mixer.Sound(button_sound_path)

        self.music_started = False
        
        self.bg = pygame.image.load(str(bg_path)).convert_alpha()
        self.frame_player = pygame.image.load(str(frame_player_path)).convert_alpha()
        self.frame_AI = pygame.image.load(str(frame_AI_path)).convert_alpha()
        
        self.quit_button = pygame.image.load(str(quit_button_path)).convert_alpha()
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.items = pygame.image.load(str(items_path)).convert_alpha()
        self.items_pressed = pygame.image.load(str(items_pressed_path)).convert_alpha()
        self.items_rect = self.items.get_rect(center = (1050, 50))

        self.shop = pygame.image.load(str(shop_path)).convert_alpha()
        self.shop_pressed = pygame.image.load(str(shop_pressed_path)).convert_alpha()
        self.shop_rect = self.shop.get_rect(center = (875, 50))

        self.top_button = pygame.image.load(str(top_button_path)).convert_alpha()
        self.top_button_pressed = pygame.image.load(str(top_button_pressed_path)).convert_alpha()
        self.top_button_items_rect = self.top_button.get_rect(center = (1050, 50))
        self.top_button_shop_rect = self.top_button.get_rect(center = (875, 50))

        self.board = pygame.image.load(str(board_path)).convert_alpha()
        self.board_pressed = pygame.image.load(str(board_pressed_path)).convert_alpha()
        self.board_grey = pygame.image.load(str(board_grey_path)).convert_alpha

        self.board01_rect = self.board.get_rect(center = (200, 195))
        self.board02_rect = self.board.get_rect(center = (400, 195))
        self.board03_rect = self.board.get_rect(center = (600, 195))
        self.board04_rect = self.board.get_rect(center = (800, 195))
        self.board05_rect = self.board.get_rect(center = (1000, 195))
        self.board11_rect = self.board.get_rect(center = (200, 285))
        self.board12_rect = self.board.get_rect(center = (400, 285))
        self.board13_rect = self.board.get_rect(center = (600, 285))
        self.board14_rect = self.board.get_rect(center = (800, 285))
        self.board15_rect = self.board.get_rect(center = (1000, 285))
        self.board21_rect = self.board.get_rect(center = (200, 375))
        self.board22_rect = self.board.get_rect(center = (400, 375))
        self.board23_rect = self.board.get_rect(center = (600, 375))
        self.board24_rect = self.board.get_rect(center = (800, 375))
        self.board25_rect = self.board.get_rect(center = (1000, 375))
        self.board31_rect = self.board.get_rect(center = (200, 465))
        self.board32_rect = self.board.get_rect(center = (400, 465))
        self.board33_rect = self.board.get_rect(center = (600, 465))
        self.board34_rect = self.board.get_rect(center = (800, 465))
        self.board35_rect = self.board.get_rect(center = (1000, 465))
        self.board41_rect = self.board.get_rect(center = (200, 555))
        self.board42_rect = self.board.get_rect(center = (400, 555))
        self.board43_rect = self.board.get_rect(center = (600, 555))
        self.board44_rect = self.board.get_rect(center = (800, 555))
        self.board45_rect = self.board.get_rect(center = (1000, 555))
        self.board51_rect = self.board.get_rect(center = (200, 645))
        self.board52_rect = self.board.get_rect(center = (400, 645))
        self.board53_rect = self.board.get_rect(center = (600, 645))
        self.board54_rect = self.board.get_rect(center = (800, 645))
        self.board55_rect = self.board.get_rect(center = (1000, 645))

        self.board11_pressed = False
        self.board12_pressed = False
        self.board13_pressed = False
        self.board14_pressed = False
        self.board15_pressed = False
        self.board21_pressed = False
        self.board22_pressed = False
        self.board23_pressed = False
        self.board24_pressed = False
        self.board25_pressed = False
        self.board31_pressed = False
        self.board32_pressed = False
        self.board33_pressed = False
        self.board34_pressed = False
        self.board35_pressed = False
        self.board41_pressed = False
        self.board42_pressed = False
        self.board43_pressed = False
        self.board44_pressed = False
        self.board45_pressed = False
        self.board51_pressed = False
        self.board52_pressed = False
        self.board53_pressed = False
        self.board54_pressed = False
        self.board55_pressed = False


    def update_questions(self, questions: list, round_no):
        self.questions = questions
        self._sort_questions(round_no)
    
    def update_character(self, char_path):
        self.char = pygame.image.load(str(char_path)).convert_alpha()

    def update(self, events) -> tuple[int]:
        if not self.music_started:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load(self.bg_music_path)
            pygame.mixer.music.play(-1)
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
            self.current_board225 = self.board_grey
        elif self.board25_rect.collidepoint(mouse_pos):
            self.current_board25 = self.board_pressed
        else:
            self.current_board25 = self.board

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
                    return 6, 0, 0
                if not self.board12_pressed and self.board12_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board12_pressed = True
                    return 6, 0, 1
                if not self.board13_pressed and self.board13_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board13_pressed = True
                    return 6, 0, 2
                if not self.board14_pressed and self.board14_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board14_pressed = True
                    return 6, 0, 3
                if not self.board15_pressed and self.board15_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board15_pressed = True
                    return 6, 0, 4
                if not self.board21_pressed and self.board21_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board21_pressed = True
                    return 6, 1, 0
                if not self.board22_pressed and self.board22_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board22_pressed = True
                    return 6, 1, 1
                if not self.board23_pressed and self.board23_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board23_pressed = True
                    return 6, 1, 2
                if not self.board24_pressed and self.board24_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board24_pressed = True
                    return 6, 1, 3
                if not self.board25_pressed and self.board25_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board25_pressed = True
                    return 6, 1, 4
                if not self.board31_pressed and self.board31_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board31_pressed = True
                    return 6, 2, 0
                if not self.board32_pressed and self.board32_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board32_pressed = True
                    return 6, 2, 1
                if not self.board33_pressed and self.board33_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board33_pressed = True
                    return 6, 2, 2
                if not self.board34_pressed and self.board34_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board34_pressed = True
                    return 6, 2, 3
                if not self.board35_pressed and self.board35_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board35_pressed = True
                    return 6, 2, 4
                if not self.board41_pressed and self.board41_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board41_pressed = True
                    return 6, 3, 0
                if not self.board42_pressed and self.board42_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board42_pressed = True
                    return 6, 3, 1
                if not self.board43_pressed and self.board43_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board43_pressed = True
                    return 6, 3, 2
                if not self.board44_pressed and self.board44_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board44_pressed = True
                    return 6, 3, 3
                if not self.board45_pressed and self.board45_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board45_pressed = True
                    return 6, 3, 4
                if not self.board51_pressed and self.board51_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board51_pressed = True
                    return 6, 4, 0
                if not self.board52_pressed and self.board52_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board52_pressed = True
                    return 6, 4, 1
                if not self.board53_pressed and self.board53_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board53_pressed = True
                    return 6, 4, 2
                if not self.board54_pressed and self.board54_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board54_pressed = True
                    return 6, 4, 3
                if not self.board55_pressed and self.board55_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.board55_pressed = True
                    return 6, 4, 4
                
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2, -1, -1
                if self.top_button_items_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2, -1, -1
                if self.top_button_shop_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2, -1, -1
        
        return 4, -1, -1
            
    def _sort_questions(self, round_no: int):
        self.round_questions = self.questions[f"round{round_no}"]
        self.category = []
        self.values = [[] for k in range(5)]
        for i in range(0, 5):
            self.category.append(self.round_questions[i]["name"])
            for j in range(0, 5):
                self.values[i].append(self.round_questions[i]["questions"][j]["value"])

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.frame_player, (15, 10))
        self.screen.blit(self.frame_AI, (350, 20))
        self.screen.blit(self.frame_AI, (350, 80))
        self.screen.blit(self.char, (55, 40))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        self.screen.blit(self.board, self.board01_rect)
        self.screen.blit(self.board, self.board02_rect)
        self.screen.blit(self.board, self.board03_rect)
        self.screen.blit(self.board, self.board04_rect)
        self.screen.blit(self.board, self.board05_rect)

        self.screen.blit(self.current_board11, self.board11_rect)
        self.screen.blit(self.current_board12, self.board12_rect)
        self.screen.blit(self.current_board13, self.board13_rect)
        self.screen.blit(self.current_board14, self.board14_rect)
        self.screen.blit(self.current_board15, self.board15_rect)
        self.screen.blit(self.current_board21, self.board21_rect)
        self.screen.blit(self.current_board22, self.board22_rect)
        self.screen.blit(self.current_board23, self.board23_rect)
        self.screen.blit(self.current_board24, self.board24_rect)
        self.screen.blit(self.current_board25, self.board25_rect)
        self.screen.blit(self.current_board31, self.board31_rect)
        self.screen.blit(self.current_board32, self.board32_rect)
        self.screen.blit(self.current_board33, self.board33_rect)
        self.screen.blit(self.current_board34, self.board34_rect)
        self.screen.blit(self.current_board35, self.board35_rect)
        self.screen.blit(self.current_board41, self.board41_rect)
        self.screen.blit(self.current_board42, self.board42_rect)
        self.screen.blit(self.current_board43, self.board43_rect)
        self.screen.blit(self.current_board44, self.board44_rect)
        self.screen.blit(self.current_board45, self.board45_rect)
        self.screen.blit(self.current_board51, self.board51_rect)
        self.screen.blit(self.current_board52, self.board52_rect)
        self.screen.blit(self.current_board53, self.board53_rect)
        self.screen.blit(self.current_board54, self.board54_rect)
        self.screen.blit(self.current_board55, self.board55_rect)

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
    question.update_character(char_path)

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