import pygame


WHITE = (245, 247, 250)
BLACK = (20, 20, 20)
BLUE = (58, 123, 213)
DARK_BLUE = (39, 88, 173)
GRAY = (210, 214, 220)
RED = (200, 70, 70)


class MainScreen:
    def __init__(self, screen: pygame.Surface, username: str, avatar_path: str | None = None):
        self.screen = screen
        self.username = username
        self.avatar_path = avatar_path

        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Main Menu")

        self.title_font = pygame.font.Font(None, 64)
        self.text_font = pygame.font.Font(None, 34)
        self.button_font = pygame.font.Font(None, 32)

        self.avatar_image = None
        if avatar_path:
            try:
                img = pygame.image.load(avatar_path).convert_alpha()
                self.avatar_image = pygame.transform.smoothscale(img, (120, 120))
            except Exception:
                self.avatar_image = None

    def _draw_button(self, rect: pygame.Rect, label: str, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=12)
        txt = self.button_font.render(label, True, WHITE)
        self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        self.width, self.height = self.screen.get_size()
        self.screen.fill(WHITE)

        card_rect = pygame.Rect(self.width // 2 - 260, 140, 520, 260)
        pygame.draw.rect(self.screen, GRAY, card_rect, border_radius=18)
        pygame.draw.rect(self.screen, BLACK, card_rect, 2, border_radius=18)

        if self.avatar_image:
            self.screen.blit(self.avatar_image, self.avatar_image.get_rect(center=(self.width // 2, 265)))
        else:
            placeholder = pygame.Rect(self.width // 2 - 60, 205, 120, 120)
            pygame.draw.ellipse(self.screen, BLUE, placeholder)
            letter = self.title_font.render(self.username[:1].upper(), True, WHITE)
            self.screen.blit(letter, letter.get_rect(center=placeholder.center))

        hello = self.text_font.render(f"Hello, {self.username}!", True, BLACK)
        self.screen.blit(hello, hello.get_rect(center=(self.width // 2, 340)))

        game_btn = pygame.Rect(self.width // 2 - 220, 480, 200, 55)
        shop_btn = pygame.Rect(self.width // 2 + 20, 480, 200, 55)
        exit_btn = pygame.Rect(self.width // 2 - 50, 560, 100, 40)

        self._draw_button(game_btn, "START GAME", BLUE)
        self._draw_button(shop_btn, "SHOP", DARK_BLUE)
        self._draw_button(exit_btn, "EXIT", RED)

        hint = self.text_font.render("ESC to exit", True, BLACK)
        self.screen.blit(hint, hint.get_rect(center=(self.width // 2, 610)))

        pygame.display.flip()
        return game_btn, shop_btn, exit_btn

    def run(self) -> str:
        clock = pygame.time.Clock()

        while True:
            game_btn, shop_btn, exit_btn = self._draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "exit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_btn.collidepoint(event.pos):
                        return "game"
                    if shop_btn.collidepoint(event.pos):
                        return "shop"
                    if exit_btn.collidepoint(event.pos):
                        return "exit"

            clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    page = MainScreen(screen, "Player", None)
    page.run()
    pygame.quit()

