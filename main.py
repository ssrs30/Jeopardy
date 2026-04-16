import pygame

from login import LoginScreen
from main_screen import MainScreen
from shop import Shop


class ShopPlayer:
    """Shop 所需玩家结构（game_logic 里目前没有 coins/inventory）。"""

    def __init__(self, name: str):
        self.name = name
        self.coins = 2000
        self.inventory = {
            "skips": 0,
            "fifty_fifty": 0,
            "shields": 0,
            "double_chance": 0,
        }


def run_shop(screen: pygame.Surface, player: ShopPlayer) -> str:
    shop = Shop(screen, player)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"

            if event.type == pygame.MOUSEBUTTONDOWN:
                result = shop.handle_click(event.pos)
                if result == "EXIT":
                    return "back"

        shop.draw()
        pygame.display.flip()
        clock.tick(60)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # 1) login
    login = LoginScreen(screen)
    user_name, avatar_path = login.run()
    if user_name is None:
        pygame.quit()
        return

    # 2) main menu
    while True:
        menu = MainScreen(screen, user_name, avatar_path)
        choice = menu.run()

        if choice == "exit":
            pygame.quit()
            return

        if choice == "shop":
            player = ShopPlayer(user_name)
            run_shop(screen, player)
            # shop 退出后回到主菜单
            continue

        if choice == "game":
            # game_logic.py 自己会创建窗口并进入事件循环
            import game_logic

            game = game_logic.Game(questions_file="questions.json")
            game.player.name = user_name
            game.run()
            # game_logic 结束后回到主界面：重新确保菜单窗口可用
            screen = pygame.display.set_mode((800, 600))
            continue


if __name__ == "__main__":
    main()