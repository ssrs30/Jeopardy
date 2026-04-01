import runpy

import pygame

from login import LoginScreen


def main() -> None:
    # 1) login
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    login = LoginScreen(screen)
    _user_name, _avatar_path = login.run()

    # 2) close login window, then run 1.py as the main program
    pygame.display.quit()
    pygame.quit()

    runpy.run_path("1.py", run_name="__main__")


if __name__ == "__main__":
    main()

