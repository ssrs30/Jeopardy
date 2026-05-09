import pygame
import pygame.freetype
from pathlib import Path
import json
import Text_wrapper

pygame.init()
pygame.font.init()

class Question:
    def __init__(self, screen):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)
        
        current_dir = Path(__file__).parent
        frame_option_path = current_dir / "Game Assets" / "frame_option.png"
        frame_option_pressed_path = current_dir / "Game Assets" / "frame_option_pressed.png"
        items_path = current_dir / "Game Assets" / "ITEMS.png"
        items_pressed_path = current_dir / "Game Assets" / "ITEMS_pressed.png"
        shop_path = current_dir / "Game Assets" / "SHOP.png"
        shop_pressed_path = current_dir / "Game Assets" / "SHOP_pressed.png"
        top_button_path = current_dir / "Game Assets" / "top_button.png"
        top_button_pressed_path = current_dir / "Game Assets" / "top_button_pressed.png"

        button_sound_path = current_dir / "Sound Effect" / "button.mp3"
        self.button_sound = pygame.mixer.Sound(button_sound_path)
        
        self.frame = pygame.image.load(str(frame_option_path)).convert_alpha()
        self.frame_pressed = pygame.image.load(str(frame_option_pressed_path)).convert_alpha()
        self.frame1_rect = self.frame.get_rect(center = (600, 400))
        self.frame2_rect = self.frame.get_rect(center = (600, 500))
        self.frame3_rect = self.frame.get_rect(center = (600, 600))

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

        self.font = pygame.freetype.Font(current_dir / "Pix32.ttf", 50)

    def update_question(self, round_no, question_list, question_no: tuple[int]):
        self.question = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["question"]
        self.question_rect = pygame.Rect(600, 200, 800, 200)
        self.options = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["options"]
        self.answer = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["correct"]

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()

        self.current_frame1 = self.frame_pressed if self.frame1_rect.collidepoint(mouse_pos) else self.frame
        self.current_frame2 = self.frame_pressed if self.frame2_rect.collidepoint(mouse_pos) else self.frame
        self.current_frame3 = self.frame_pressed if self.frame3_rect.collidepoint(mouse_pos) else self.frame

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
                if self.frame1_rect.collidepoint(event.pos):
                    if self.answer == 0:
                        return 0
                    else:
                        return 0
                if self.frame2_rect.collidepoint(event.pos):
                    if self.answer == 1:
                        return 0
                    else:
                        return 0
                if self.frame3_rect.collidepoint(event.pos):
                    if self.answer == 2:
                        return 0
                    else:
                        return 0
                if self.top_button_items_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
                if self.top_button_shop_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
        
        return 1


    def draw(self):
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.current_frame1, self.frame1_rect)
        self.screen.blit(self.current_frame2, self.frame2_rect)
        self.screen.blit(self.current_frame3, self.frame3_rect)

        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)

        Text_wrapper.draw_wrapped_text(self.screen, self.question, self.font, (255, 255, 255), self.question_rect, True)

        self.option1_text, self.option1_rect = self.font.render(self.options[0], (255, 255, 255))
        self.option1_rect.center = self.frame1_rect.center
        self.screen.blit(self.option1_text, self.option1_rect)
        self.option2_text, self.option2_rect = self.font.render(self.options[1], (255, 255, 255))
        self.option2_rect.center = self.frame2_rect.center
        self.screen.blit(self.option2_text, self.option2_rect)
        self.option3_text, self.option3_rect = self.font.render(self.options[2], (255, 255, 255))
        self.option3_rect.center = self.frame3_rect.center
        self.screen.blit(self.option3_text, self.option3_rect)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    char_path = Path(__file__).parent / "Game Assets" / "Characters" / "c1.png"
    question = Question(screen)
    clock = pygame.time.Clock()
    num = 1
    running = True

    with open(Path(__file__).parent / "questions.json", "r") as file:
        questions = json.load(file)

    question.update_question(1, questions, (2, 1))

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 1:
            num= question.update(events)
            question.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()