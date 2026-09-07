import pygame
import pygame.freetype
from . import Text_wrapper
from .assets import load_font, load_image, load_sound

pygame.init()
pygame.mixer.init()
pygame.font.init()


class Question:

    def __init__(self, screen):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(128)

        self.button_sound = load_sound("Sound Effect", "button.mp3")

        self.frame = load_image("Game Assets", "frame_option.png", size=(700, 80), label="")
        self.frame_pressed = load_image("Game Assets", "frame_option_pressed.png", size=(700, 80), label="")
        self._fj_shared_shift_x = -100  # Final Jeopardy: clue/options/timer vs rounds 1–2
        self.frame1_rect = self.frame.get_rect(center=(600, 470))
        self.frame2_rect = self.frame.get_rect(center=(600, 570))
        self.frame3_rect = self.frame.get_rect(center=(600, 670))

        self.font = load_font(50)
        self.countdown_secs = None
        self.countdown_font = load_font(34)
        self.hidden_options = set()

        self.what_is, self.what_is_rect = self.font.render("What is _______?", (255, 255, 255))
        self.what_is_rect.center = (600, 400)

        self.fj_frame_continue = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.fj_frame_continue_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.fj_continue_text = load_image("Game Assets", "CONTINUE.png", size=(180, 50), label="CONTINUE")
        self.fj_continue_pressed = load_image("Game Assets", "CONTINUE_pressed.png", size=(180, 50), label="CONTINUE")
        self.fj_frame_continue_rect = self.fj_frame_continue.get_rect(center=(1050, 600))
        self.fj_continue_img_rect = self.fj_continue_text.get_rect(center=(1050, 600))
        self.fj_current_continue_frame = self.fj_frame_continue
        self.fj_current_continue_img = self.fj_continue_text

        self._is_final_jeopardy = False
        self.fj_eligible_human = True
        self.fj_human_answered = False
        self.fj_sidebar_rows: list[dict] = []
        self.fj_show_continue = False
        self.sidebar_font = load_font(20)
        self.fj_panel_rect = pygame.Rect(930, 200, 250, 360)

    def refresh_shared_layout_positions(self) -> None:
        dx = self._fj_shared_shift_x if self._is_final_jeopardy else 0
        self.frame1_rect = self.frame.get_rect(center=(600 + dx, 470))
        self.frame2_rect = self.frame.get_rect(center=(600 + dx, 570))
        self.frame3_rect = self.frame.get_rect(center=(600 + dx, 670))
        self.question_rect = pygame.Rect(600 + dx, 200, 800, 200)
        self.what_is_rect.center = (600 + dx, 400)

    def update_question(self, round_no, question_list, question_no: tuple[int]):
        """Put question text, options, and correct index"""
        self.question = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["question"]
        self.options = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["options"]
        self.answer = question_list[f"round{round_no}"][question_no[1]]["questions"][question_no[0]]["correct"]
        self.refresh_shared_layout_positions()

    def set_countdown(self, secs: int | None):
        self.countdown_secs = secs

    def set_hidden_options(self, hidden_options: set[int] | None):
        self.hidden_options = set(hidden_options or set())

    def configure_final_jeopardy(self, eligible_human: bool):
        self._is_final_jeopardy = True
        self.fj_eligible_human = eligible_human
        self.fj_human_answered = False
        self.fj_show_continue = False
        self.fj_sidebar_rows = []
        self.refresh_shared_layout_positions()

    def reset_final_jeopardy_mode(self):
        self._is_final_jeopardy = False
        self.fj_human_answered = False
        self.fj_show_continue = False
        self.fj_sidebar_rows = []
        self.refresh_shared_layout_positions()

    def set_final_jeopardy_overlay(self, rows: list[dict], show_continue: bool, human_answered: bool) -> None:
        self.fj_sidebar_rows = list(rows)
        self.fj_show_continue = show_continue
        self.fj_human_answered = human_answered

    def draw_fj_status_panel(self, pr: pygame.Rect) -> None:
        pygame.draw.rect(self.screen, (40, 40, 40), pr, 0)
        pygame.draw.rect(self.screen, (160, 160, 90), pr, 2)
        title_s, _tr = self.sidebar_font.render("STATUS", (255, 220, 120))
        self.screen.blit(title_s, (pr.x + 10, pr.y + 10))

        _, sample_r = self.sidebar_font.render("Mg", (255, 255, 255))
        line_h = max(20, sample_r.height + 4)
        y = pr.y + 38
        max_y = pr.bottom - 12
        lx = pr.x + 8
        val_right = pr.right - 10
        col_label = (190, 190, 190)
        col_value = (235, 235, 235)
        col_name = (255, 248, 210)
        col_answering = (255, 70, 70)
        col_answered = (90, 210, 110)

        def blit_pair(label: str, value: str, vcolor: tuple[int, int, int] = col_value) -> int:
            if y > max_y:
                return y
            lab_s, _lr = self.sidebar_font.render(label, col_label)
            val_s, val_r = self.sidebar_font.render(value, vcolor)
            self.screen.blit(lab_s, (lx, y))
            self.screen.blit(val_s, (val_right - val_r.width, y))
            return y + line_h

        for row in self.fj_sidebar_rows:
            if y > max_y:
                break
            kind = row.get("kind")
            if kind == "sep":
                mid = y + line_h // 2
                pygame.draw.line(self.screen, (110, 110, 110), (lx, mid), (val_right, mid), 1)
                y += line_h + 2
                continue
            if kind != "player":
                continue

            name = str(row.get("name", ""))
            can_play = bool(row.get("can_play"))
            wager = int(row.get("wager", 0))
            score = int(row.get("score", 0))
            phase = str(row.get("phase", "spectator"))

            head = f"{name}: Cannot play" if not can_play else name
            h_s, _hr = self.sidebar_font.render(head, col_name if can_play else col_value)
            self.screen.blit(h_s, (lx, y))
            y += line_h

            if not can_play:
                y = blit_pair("Wager:", f"${wager}", col_value)
                y = blit_pair("Score:", f"${score}", col_value)
                y += 2
                continue

            y = blit_pair("Wager:", f"${wager}", col_value)
            y = blit_pair("Score:", f"${score}", col_value)

            lab_s, _ = self.sidebar_font.render("Status:", col_label)
            if phase == "answering":
                st, st_col = "answering…", col_answering
            elif phase == "answered":
                st, st_col = "answered", col_answered
            else:
                st, st_col = "—", (150, 150, 150)
            st_s, st_r = self.sidebar_font.render(st, st_col)
            self.screen.blit(lab_s, (lx, y))
            self.screen.blit(st_s, (val_right - st_r.width, y))
            y += line_h + 2

    def fj_human_can_pick(self) -> bool:
        return self.fj_eligible_human and not self.fj_human_answered

    def fj_lock_all_option_frames_visual(self) -> None:
        self.current_frame1 = self.current_frame2 = self.current_frame3 = self.frame_pressed

    def update(self, events):
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()

        if self._is_final_jeopardy:
            if self.fj_show_continue:
                on_cont = self.fj_frame_continue_rect.collidepoint(mouse_pos)
                if on_cont:
                    self.fj_current_continue_frame = self.fj_frame_continue_pressed
                    self.fj_current_continue_img = self.fj_continue_pressed
                else:
                    self.fj_current_continue_frame = self.fj_frame_continue
                    self.fj_current_continue_img = self.fj_continue_text

            can_pick = self.fj_human_can_pick()
            if (self.fj_eligible_human and self.fj_human_answered) or not self.fj_eligible_human:
                self.fj_lock_all_option_frames_visual()
            else:
                for i, rect in enumerate((self.frame1_rect, self.frame2_rect, self.frame3_rect)):
                    if can_pick and i not in self.hidden_options and rect.collidepoint(mouse_pos):
                        setattr(self, f"current_frame{i + 1}", self.frame_pressed)
                    else:
                        setattr(self, f"current_frame{i + 1}", self.frame)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.fj_show_continue and self.fj_frame_continue_rect.collidepoint(event.pos):
                        self.button_sound.play()
                        return 7, True
                    if not can_pick:
                        continue
                    if self.frame1_rect.collidepoint(event.pos) and 0 not in self.hidden_options:
                        self.button_sound.play()
                        self.fj_lock_all_option_frames_visual()
                        return (9, True) if self.answer == 0 else (9, False)
                    if self.frame2_rect.collidepoint(event.pos) and 1 not in self.hidden_options:
                        self.button_sound.play()
                        self.fj_lock_all_option_frames_visual()
                        return (9, True) if self.answer == 1 else (9, False)
                    if self.frame3_rect.collidepoint(event.pos) and 2 not in self.hidden_options:
                        self.button_sound.play()
                        self.fj_lock_all_option_frames_visual()
                        return (9, True) if self.answer == 2 else (9, False)
            return 8, True

        self.current_frame1 = self.frame_pressed if self.frame1_rect.collidepoint(mouse_pos) else self.frame
        self.current_frame2 = self.frame_pressed if self.frame2_rect.collidepoint(mouse_pos) else self.frame
        self.current_frame3 = self.frame_pressed if self.frame3_rect.collidepoint(mouse_pos) else self.frame

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame1_rect.collidepoint(event.pos) and 0 not in self.hidden_options:
                    self.button_sound.play()
                    if self.answer == 0:
                        return 9, True
                    else:
                        return 9, False
                if self.frame2_rect.collidepoint(event.pos) and 1 not in self.hidden_options:
                    self.button_sound.play()
                    if self.answer == 1:
                        return 9, True
                    else:
                        return 9, False
                if self.frame3_rect.collidepoint(event.pos) and 2 not in self.hidden_options:
                    self.button_sound.play()
                    if self.answer == 2:
                        return 9, True
                    else:
                        return 9, False

        return 8, True

    def draw(self):
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.current_frame1, self.frame1_rect)
        self.screen.blit(self.current_frame2, self.frame2_rect)
        self.screen.blit(self.current_frame3, self.frame3_rect)

        Text_wrapper.draw_wrapped_text(self.screen, self.question, self.font, (255, 255, 255), self.question_rect, True)

        self.screen.blit(self.what_is, self.what_is_rect)

        if self._is_final_jeopardy and not self.fj_eligible_human:
            lock_msg = "You cannot answer (score must be positive). Wager locked at $0."
            lx = 300 + self._fj_shared_shift_x
            self.sidebar_font.render_to(self.screen, (lx, 730), lock_msg, (200, 200, 200))

        option_1 = self.options[0] if 0 not in self.hidden_options else "----"
        self.option1_text, self.option1_rect = self.font.render(option_1, (255, 255, 255))
        self.option1_rect.center = self.frame1_rect.center
        self.screen.blit(self.option1_text, self.option1_rect)
        option_2 = self.options[1] if 1 not in self.hidden_options else "----"
        self.option2_text, self.option2_rect = self.font.render(option_2, (255, 255, 255))
        self.option2_rect.center = self.frame2_rect.center
        self.screen.blit(self.option2_text, self.option2_rect)
        option_3 = self.options[2] if 2 not in self.hidden_options else "----"
        self.option3_text, self.option3_rect = self.font.render(option_3, (255, 255, 255))
        self.option3_rect.center = self.frame3_rect.center
        self.screen.blit(self.option3_text, self.option3_rect)

        if self.countdown_secs is None:
            t_surf, t_rect = self.countdown_font.render("Time: Unlimited", (255, 255, 255))
        else:
            color = (255, 80, 80) if self.countdown_secs <= 3 else (255, 255, 255)
            t_surf, t_rect = self.countdown_font.render(f"Time: {self.countdown_secs}s", color)
        t_rect.topright = (1170, 120)
        self.screen.blit(t_surf, t_rect)

        if self._is_final_jeopardy:
            self.draw_fj_status_panel(self.fj_panel_rect)

            if self.fj_show_continue:
                self.screen.blit(self.fj_current_continue_frame, self.fj_frame_continue_rect)
                self.screen.blit(self.fj_current_continue_img, self.fj_continue_img_rect)