"""shared guideline UI"""

from __future__ import annotations

from pathlib import Path

import pygame
import pygame.freetype

try:
    from . import Text_wrapper
    from .assets import load_font, load_image, load_sound
except ImportError:
    import Text_wrapper
    from assets import load_font, load_image, load_sound

pygame.init()
pygame.font.init()


class GuidelinesBase:
    """base class for guideline pages."""

    def __init__(self, screen: pygame.Surface, filename: Path | str):
        with open(filename, "r", encoding="utf-8") as f:
            self.text = f.readlines()

        self.screen = screen
        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(150)

        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.button = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.button_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.button_rect = self.button.get_rect(center=(1030, 730))
        self.return_text = load_image("Game Assets", "RETURN.png", size=(180, 50), label="RETURN")
        self.return_pressed = load_image("Game Assets", "RETURN_pressed.png", size=(180, 50), label="RETURN")
        self.return_rect = self.return_text.get_rect(center=(1030, 730))

        self.font = load_font(20)

    def update_return_hover(self, mouse_pos: tuple[int, int]) -> None:
        if self.button_rect.collidepoint(mouse_pos):
            self.current_button = self.button_pressed
            self.current_return = self.return_pressed
        else:
            self.current_button = self.button
            self.current_return = self.return_text

    def _draw_background(self) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))

    def _draw_return_row(self) -> None:
        self.screen.blit(self.current_button, self.button_rect)
        self.screen.blit(self.current_return, self.return_rect)


class GuidelinesPage1(GuidelinesBase):

    def __init__(self, screen: pygame.Surface, filename: Path | str):
        super().__init__(screen, filename)

        self.text_rect0 = pygame.Rect(50, 50, 1100, 30)
        self.text_rect1 = pygame.Rect(50, 80, 1100, 30)
        self.text_rect2 = pygame.Rect(50, 110, 1100, 30)
        self.text_rect3 = pygame.Rect(50, 140, 1100, 30)
        self.text_rect4 = pygame.Rect(50, 170, 1100, 90)
        self.text_rect5 = pygame.Rect(50, 260, 1100, 50)
        self.text_rect6 = pygame.Rect(50, 310, 1100, 50)
        self.text_rect7 = pygame.Rect(50, 360, 1100, 90)
        self.text_rect8 = pygame.Rect(50, 450, 1100, 90)
        self.text_rect9 = pygame.Rect(50, 540, 1100, 50)
        self.text_rect10 = pygame.Rect(50, 590, 1100, 50)

        self.prev = load_image("Game Assets", "prev_grey.png", size=(80, 50), label="<")
        self.next = load_image("Game Assets", "next.png", size=(80, 50), label=">")
        self.next_rect = self.next.get_rect(topleft=(650, 700))
        self.button_sound = load_sound("Sound Effect", "button.mp3")

    def update(self, events: list[pygame.event.Event]) -> int:
        mouse_pos = pygame.mouse.get_pos()
        self.update_return_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 5
                if self.next_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2

        return 1

    def draw(self) -> None:
        self._draw_background()

        Text_wrapper.draw_wrapped_text(self.screen, self.text[0], self.font, (255, 255, 255), self.text_rect0)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[1], self.font, (255, 255, 255), self.text_rect1)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[2], self.font, (255, 255, 255), self.text_rect2)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[3], self.font, (255, 255, 255), self.text_rect3)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[4], self.font, (255, 255, 255), self.text_rect4)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[5], self.font, (255, 255, 255), self.text_rect5)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[6], self.font, (255, 255, 255), self.text_rect6)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[7], self.font, (255, 255, 255), self.text_rect7)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[8], self.font, (255, 255, 255), self.text_rect8)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[9], self.font, (255, 255, 255), self.text_rect9)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[10], self.font, (255, 255, 255), self.text_rect10)

        self._draw_return_row()
        self.screen.blit(self.next, self.next_rect)
        self.screen.blit(self.prev, (550, 700))


class GuidelinesPage2(GuidelinesBase):

    def __init__(self, screen: pygame.Surface, filename: Path | str):
        super().__init__(screen, filename)

        self.text_rect11 = pygame.Rect(50, 50, 1100, 30)
        self.text_rect12 = pygame.Rect(50, 80, 1100, 30)
        self.text_rect13 = pygame.Rect(50, 110, 1100, 50)
        self.text_rect14 = pygame.Rect(50, 160, 1100, 50)
        self.text_rect15 = pygame.Rect(50, 210, 1100, 30)
        self.text_rect16 = pygame.Rect(50, 240, 1100, 30)
        self.text_rect17 = pygame.Rect(50, 270, 1100, 30)
        self.text_rect18 = pygame.Rect(50, 300, 1100, 30)
        self.text_rect19 = pygame.Rect(50, 330, 1100, 30)
        self.text_rect20 = pygame.Rect(50, 360, 1100, 30)
        self.text_rect21 = pygame.Rect(50, 390, 1100, 30)
        self.text_rect22 = pygame.Rect(50, 420, 1100, 30)
        self.text_rect23 = pygame.Rect(50, 450, 1100, 30)
        self.text_rect24 = pygame.Rect(50, 480, 1100, 30)
        self.text_rect25 = pygame.Rect(50, 510, 1100, 30)
        self.text_rect26 = pygame.Rect(50, 540, 1100, 30)
        self.text_rect27 = pygame.Rect(50, 570, 1100, 30)
        self.text_rect28 = pygame.Rect(50, 600, 1100, 30)

        self.prev = load_image("Game Assets", "prev.png", size=(80, 50), label="<")
        self.next = load_image("Game Assets", "next.png", size=(80, 50), label=">")
        self.prev_rect = self.prev.get_rect(topleft=(550, 700))
        self.next_rect = self.next.get_rect(topleft=(650, 700))
        self.button_sound = load_sound("Sound Effect", "button.mp3")


    def update(self, events: list[pygame.event.Event]) -> int:
        mouse_pos = pygame.mouse.get_pos()
        self.update_return_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 5
                if self.prev_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 1
                if self.next_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 3

        return 2

    def draw(self) -> None:
        self._draw_background()

        Text_wrapper.draw_wrapped_text(self.screen, self.text[11], self.font, (255, 255, 255), self.text_rect11)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[12], self.font, (255, 255, 255), self.text_rect12)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[13], self.font, (255, 255, 255), self.text_rect13)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[14], self.font, (255, 255, 255), self.text_rect14)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[15], self.font, (255, 255, 255), self.text_rect15)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[16], self.font, (255, 255, 255), self.text_rect16)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[17], self.font, (255, 255, 255), self.text_rect17)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[18], self.font, (255, 255, 255), self.text_rect18)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[19], self.font, (255, 255, 255), self.text_rect19)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[20], self.font, (255, 255, 255), self.text_rect20)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[21], self.font, (255, 255, 255), self.text_rect21)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[22], self.font, (255, 255, 255), self.text_rect22)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[23], self.font, (255, 255, 255), self.text_rect23)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[24], self.font, (255, 255, 255), self.text_rect24)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[25], self.font, (255, 255, 255), self.text_rect25)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[26], self.font, (255, 255, 255), self.text_rect26)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[27], self.font, (255, 255, 255), self.text_rect27)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[28], self.font, (255, 255, 255), self.text_rect28)

        self._draw_return_row()
        self.screen.blit(self.next, self.next_rect)
        self.screen.blit(self.prev, (550, 700))


class GuidelinesPage3(GuidelinesBase):

    def __init__(self, screen: pygame.Surface, filename: Path | str):
        super().__init__(screen, filename)

        self.text_rect29 = pygame.Rect(50, 50, 1100, 30)
        self.text_rect30 = pygame.Rect(50, 80, 1100, 30)
        self.text_rect31 = pygame.Rect(50, 110, 1100, 30)
        self.text_rect32 = pygame.Rect(50, 140, 1100, 30)
        self.text_rect33 = pygame.Rect(50, 170, 1100, 30)
        self.text_rect34 = pygame.Rect(50, 200, 1100, 30)
        self.text_rect35 = pygame.Rect(50, 230, 1100, 30)
        self.text_rect36 = pygame.Rect(50, 260, 1100, 30)
        self.text_rect37 = pygame.Rect(50, 290, 1100, 30)
        self.text_rect38 = pygame.Rect(50, 320, 1100, 50)
        self.text_rect39 = pygame.Rect(50, 370, 1100, 30)
        self.text_rect40 = pygame.Rect(50, 400, 1100, 30)
        self.text_rect41 = pygame.Rect(50, 430, 1100, 30)
        self.text_rect42 = pygame.Rect(50, 460, 1100, 30)
        self.text_rect43 = pygame.Rect(50, 490, 1100, 30)
        self.text_rect44 = pygame.Rect(50, 520, 1100, 30)
        self.text_rect45 = pygame.Rect(50, 550, 1100, 30)
        self.text_rect46 = pygame.Rect(50, 580, 1100, 30)
        self.text_rect47 = pygame.Rect(50, 610, 1100, 30)
        self.text_rect48 = pygame.Rect(50, 640, 1100, 30)

        self.prev = load_image("Game Assets", "prev.png", size=(80, 50), label="<")
        self.next = load_image("Game Assets", "next.png", size=(80, 50), label=">")
        self.prev_rect = self.prev.get_rect(topleft=(550, 700))
        self.next_rect = self.next.get_rect(topleft=(650, 700))
        self.button_sound = load_sound("Sound Effect", "button.mp3")

    def update(self, events: list[pygame.event.Event]) -> int:
        mouse_pos = pygame.mouse.get_pos()
        self.update_return_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 5
                if self.prev_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
                if self.next_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 4

        return 3

    def draw(self) -> None:
        self._draw_background()

        Text_wrapper.draw_wrapped_text(self.screen, self.text[29], self.font, (255, 255, 255), self.text_rect29)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[30], self.font, (255, 255, 255), self.text_rect30)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[31], self.font, (255, 255, 255), self.text_rect31)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[32], self.font, (255, 255, 255), self.text_rect32)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[33], self.font, (255, 255, 255), self.text_rect33)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[34], self.font, (255, 255, 255), self.text_rect34)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[35], self.font, (255, 255, 255), self.text_rect35)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[36], self.font, (255, 255, 255), self.text_rect36)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[37], self.font, (255, 255, 255), self.text_rect37)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[38], self.font, (255, 255, 255), self.text_rect38)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[39], self.font, (255, 255, 255), self.text_rect39)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[40], self.font, (255, 255, 255), self.text_rect40)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[41], self.font, (255, 255, 255), self.text_rect41)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[42], self.font, (255, 255, 255), self.text_rect42)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[43], self.font, (255, 255, 255), self.text_rect43)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[44], self.font, (255, 255, 255), self.text_rect44)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[45], self.font, (255, 255, 255), self.text_rect45)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[46], self.font, (255, 255, 255), self.text_rect46)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[47], self.font, (255, 255, 255), self.text_rect47)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[48], self.font, (255, 255, 255), self.text_rect48)

        self._draw_return_row()
        self.screen.blit(self.prev, self.prev_rect)
        self.screen.blit(self.next, self.next_rect)

    
class GuidelinesPage4(GuidelinesBase):

    def __init__(self, screen: pygame.Surface, filename: Path | str):
        super().__init__(screen, filename)

        self.text_rect49 = pygame.Rect(50, 50, 1100, 30)
        self.text_rect50 = pygame.Rect(50, 80, 1100, 30)
        self.text_rect51 = pygame.Rect(50, 110, 1100, 30)
        self.text_rect52 = pygame.Rect(50, 140, 1100, 30)
        self.text_rect53 = pygame.Rect(50, 170, 1100, 30)
        self.text_rect54 = pygame.Rect(50, 200, 1100, 30)
        self.text_rect55 = pygame.Rect(50, 230, 1100, 30)
        self.text_rect56 = pygame.Rect(50, 260, 1100, 30)
        self.text_rect57 = pygame.Rect(50, 290, 1100, 30)
        self.text_rect58 = pygame.Rect(50, 320, 1100, 30)
        self.text_rect59 = pygame.Rect(50, 350, 1100, 30)
        self.text_rect60 = pygame.Rect(50, 380, 1100, 30)
        self.text_rect61 = pygame.Rect(50, 410, 1100, 30)
        self.text_rect62 = pygame.Rect(50, 440, 1100, 30)
        self.text_rect63 = pygame.Rect(50, 470, 1100, 30)
        self.text_rect64 = pygame.Rect(50, 500, 1100, 30)
        self.text_rect65 = pygame.Rect(50, 530, 1100, 30)
        self.text_rect66 = pygame.Rect(50, 560, 1100, 30)
        self.text_rect67 = pygame.Rect(50, 590, 1100, 30)
        self.text_rect68 = pygame.Rect(50, 620, 1100, 30)
        self.text_rect69 = pygame.Rect(50, 650, 1100, 30)
        self.text_rect70 = pygame.Rect(50, 680, 1100, 30)
        self.text_rect71 = pygame.Rect(50, 710, 1100, 30)

        self.prev = load_image("Game Assets", "prev.png", size=(80, 50), label="<")
        self.next = load_image("Game Assets", "next_grey.png", size=(80, 50), label=">")
        self.prev_rect = self.prev.get_rect(topleft=(550, 700))
        self.button_sound = load_sound("Sound Effect", "button.mp3")

    def update(self, events: list[pygame.event.Event]) -> int:
        mouse_pos = pygame.mouse.get_pos()
        self.update_return_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 5
                if self.prev_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 3

        return 4
    
    def draw(self) -> None:
        self._draw_background()

        Text_wrapper.draw_wrapped_text(self.screen, self.text[49], self.font, (255, 255, 255), self.text_rect49)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[50], self.font, (255, 255, 255), self.text_rect50)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[51], self.font, (255, 255, 255), self.text_rect51)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[52], self.font, (255, 255, 255), self.text_rect52)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[53], self.font, (255, 255, 255), self.text_rect53)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[54], self.font, (255, 255, 255), self.text_rect54)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[55], self.font, (255, 255, 255), self.text_rect55)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[56], self.font, (255, 255, 255), self.text_rect56)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[57], self.font, (255, 255, 255), self.text_rect57)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[58], self.font, (255, 255, 255), self.text_rect58)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[59], self.font, (255, 255, 255), self.text_rect59)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[60], self.font, (255, 255, 255), self.text_rect60)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[61], self.font, (255, 255, 255), self.text_rect61)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[62], self.font, (255, 255, 255), self.text_rect62)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[63], self.font, (255, 255, 255), self.text_rect63)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[64], self.font, (255, 255, 255), self.text_rect64)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[65], self.font, (255, 255, 255), self.text_rect65)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[66], self.font, (255, 255, 255), self.text_rect66)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[67], self.font, (255, 255, 255), self.text_rect67)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[68], self.font, (255, 255, 255), self.text_rect68)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[69], self.font, (255, 255, 255), self.text_rect69)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[70], self.font, (255, 255, 255), self.text_rect70)
        Text_wrapper.draw_wrapped_text(self.screen, self.text[71], self.font, (255, 255, 255), self.text_rect71)

        self._draw_return_row()
        self.screen.blit(self.prev, self.prev_rect)
        self.screen.blit(self.next, (650, 700))

if __name__ == "__main__":
    pygame.display.set_caption("Guidelines Pages (test)")
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()

    guide_file = Path(__file__).resolve().parent.parent / "Guideline.txt"
    page1 = GuidelinesPage1(screen, guide_file)
    page2 = GuidelinesPage2(screen, guide_file)
    page3 = GuidelinesPage3(screen, guide_file)
    page4 = GuidelinesPage4(screen, guide_file)
    page = 1
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if page == 1:
            code = page1.update(events)
            page1.draw()
        elif page == 2:
            code = page2.update(events)
            page2.draw()
        elif page == 3:
            code = page3.update(events)
            page3.draw()
        elif page == 4:
            code = page4.update(events)
            page4.draw()
        else:
            code = 1
            page = 1

        if code == 2:
            page = 2
        elif code == 1:
            page = 1
        elif code == 3:
            page = 3
        elif code == 4:
            page = 4
        elif code == 5:
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
