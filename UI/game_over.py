import pygame
import pygame.freetype
from pathlib import Path

from .assets import load_font, load_image, load_sound

pygame.init()
pygame.font.init()

class GameOver:
    """Game Over screen"""
    def __init__(self, screen):
        self.screen = screen

        self.dark_surface = pygame.Surface((1200, 800))
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.set_alpha(150)

        self.winning_sound = load_sound("Sound Effect", "Ranking.mp3")
        self.losing_sound = load_sound("Sound Effect", "wrong_answer.mp3")

        self.bg = load_image("Game Assets", "bg.png", size=(1200, 800), label="BG")
        self.frame_player = load_image("Game Assets", "frame_player.png", size=(280, 90), label="")
        self.game_over = load_image("Game Assets", "GAMEOVER.png", size=(480, 90), label="GAME OVER")
        self.trophy = load_image("Game Assets", "trophy.png", size=(80, 80), label="")

        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.back_text = load_image("Game Assets", "Back.png", size=(220, 50), label="BACK")
        self.back_pressed = load_image("Game Assets", "Back_pressed.png", size=(220, 50), label="BACK")
        self.back_rect = self.back_text.get_rect(center = (300, 700))

        self.restart_text = load_image("Game Assets", "RESTART.png", size=(220, 50), label="RESTART")
        self.restart_pressed = load_image("Game Assets", "RESTART_pressed.png", size=(220, 50), label="RESTART")
        self.restart_rect = self.restart_text.get_rect(center = (900, 700))

        self.back_frame = load_image("Game Assets", "back_frame.png", size=(280, 80), label="")
        self.back_frame_pressed = load_image("Game Assets", "back_frame_pressed.png", size=(280, 80), label="")
        self.back_frame_rect = self.back_frame.get_rect(center = (300, 700))
        self.restart_frame_rect = self.back_frame.get_rect(center = (900, 700))

        self.info_font = load_font(34)
        self.record_font = load_font(26)
        self.coin_font = load_font(50)
        self.rankings = []
        self._personal_best: int | None = None
        self._win_streak_record: int | None = None
        self._human_player_score_for_coins: int | None = None

    def make_avatar_surface(self, avatar_ref, player_name: str):
        """Return avatar image"""
        try:
            avatar_path = Path(str(avatar_ref))
            if avatar_path.exists():
                return pygame.image.load(str(avatar_path)).convert_alpha()
        except Exception:
            pass
        surf = pygame.Surface((88, 88), pygame.SRCALPHA)
        pygame.draw.circle(surf, (90, 140, 210), (44, 44), 44)
        label = (player_name[:2] or "?").upper()
        lab_surf, lab_rect = self.info_font.render(label, (255, 255, 255))
        lab_rect.center = (44, 44)
        surf.blit(lab_surf, lab_rect)
        return surf

    def set_personal_records(self, best_score: int, win_streak: int) -> None:
        """show win streak and best score"""
        self._personal_best = int(best_score)
        self._win_streak_record = int(win_streak)

    def set_coins_added_display(self, human_player_score: int) -> None:
        self._human_player_score_for_coins = int(human_player_score)

    def update_result(self, result: list[list[str | int]]):
        self._personal_best = None
        self._win_streak_record = None
        self._human_player_score_for_coins = None
        normalized = []
        for i, entry in enumerate(result):
            avatar_ref = entry[0]
            name = str(entry[1])
            score = int(entry[2])
            correct_clues = int(entry[3]) if len(entry) > 3 else 0
            avatar_surf = (
                self.make_avatar_surface(avatar_ref, name) if i == 0 else None
            )
            normalized.append(
                {
                    "avatar": avatar_surf,
                    "name": name,
                    "score": score,
                    "correct_clues": correct_clues,
                }
            )
        self.rankings = sorted(
            normalized,
            key=lambda x: (x["score"], x["correct_clues"]),
            reverse=True,
        )
        human_name = str(result[0][1])
        human_score = int(result[0][2])
        human_clues = int(result[0][3]) if len(result[0]) > 3 else 0
        top = self.rankings[0]
        human_first = (
            top["name"] == human_name
            and top["score"] == human_score
            and top["correct_clues"] == human_clues
        )
        if human_first:
            self.winning_sound.play()
        else:
            self.losing_sound.play()

    def update(self, events):
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()

        if self.back_frame_rect.collidepoint(mouse_pos):
            self.current_back = self.back_pressed
            self.current_back_frame = self.back_frame_pressed
        else:
            self.current_back = self.back_text
            self.current_back_frame = self.back_frame

        if self.restart_frame_rect.collidepoint(mouse_pos):
            self.current_restart = self.restart_pressed
            self.current_restart_frame = self.back_frame_pressed
        else:
            self.current_restart = self.restart_text
            self.current_restart_frame = self.back_frame
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button_rect.collidepoint(event.pos):
                    return 4
                if self.restart_frame_rect.collidepoint(event.pos):
                    return 3
                if self.back_frame_rect.collidepoint(event.pos):
                    return 2

        return 1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.quit_button, self.quit_button_rect)

        self.screen.blit(self.game_over, (200, 130))

        if self._personal_best is not None and self._win_streak_record is not None:
            rx, ry = 40, 30
            lab1, lab1_r = self.record_font.render("Highest Streak: ", (210, 220, 240))
            v1, v1_r = self.record_font.render(str(self._win_streak_record), (255, 220, 80))
            self.screen.blit(lab1, (rx, ry))
            self.screen.blit(v1, (rx + lab1_r.width + 6, ry))
            ry += 36
            lab2, lab2_r = self.record_font.render("Highest Score: ", (210, 220, 240))
            v2, v2_r = self.record_font.render(str(self._personal_best), (255, 220, 80))
            self.screen.blit(lab2, (rx, ry))
            self.screen.blit(v2, (rx + lab2_r.width + 6, ry))

        if self._human_player_score_for_coins is not None:
            hp = self._human_player_score_for_coins
            coin_msg = "0 coins added!" if hp < 0 else f"{hp} coins added!"
            csurf, _cr = self.coin_font.render(coin_msg, (200, 255, 170))
            self.screen.blit(csurf, (420, 40))

        self.screen.blit(self.frame_player, (440, 320))
        self.screen.blit(self.frame_player, (200, 450))
        self.screen.blit(self.frame_player, (680, 450))
        self.screen.blit(self.trophy, (700, 300))

        # winner -> top frame, second -> left frame, last -> right frame
        frame_centers = [(505, 415), (265, 545), (750, 545)]
        for i, center in enumerate(frame_centers):
            if i >= len(self.rankings):
                continue
            item = self.rankings[i]
            av = item["avatar"]
            if av is not None:
                avatar_rect = av.get_rect(center=(center[0], center[1] - 28))
                self.screen.blit(av, avatar_rect)
            name_surf, name_rect = self.info_font.render(item["name"], (255, 255, 255))
            name_rect.topleft = (center[0] + 73, center[1] - 60)
            self.screen.blit(name_surf, name_rect)
            score_surf, score_rect = self.info_font.render(
                f"{item['score']}", (255, 220, 80)
            )
            score_rect.topleft = (center[0] + 73, center[1] - 25)
            self.screen.blit(score_surf, score_rect)

        self.screen.blit(self.current_back_frame, self.back_frame_rect)
        self.screen.blit(self.current_back, self.back_rect)
        self.screen.blit(self.current_restart_frame, self.restart_frame_rect)
        self.screen.blit(self.current_restart, self.restart_rect)


if __name__ == "__main__":
    pygame.display.set_caption("GameOver (test)")
    screen = pygame.display.set_mode((1200, 800))
    window = GameOver(screen)
    window.update_result(
        [
            [Path(__file__).parent / "Game Assets" / "Characters" / "c1.png", "You", 2500, 10],
            ["", "AI1", 1800, 7],
            ["", "AI2", 1200, 4],
        ]
    )
    window.set_personal_records(7400, 3)
    window.set_coins_added_display(2500)
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        n = window.update(events)
        if n != 1:
            meaning = {2: "back -> HOME", 3: "restart", 4: "quit -> PAUSE"}.get(n, "?")
            print(f"[game_over test] return {n} ({meaning})")
        window.draw()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()