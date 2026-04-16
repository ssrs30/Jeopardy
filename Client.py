import pygame
import home
import pause
import char

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

homepage = home.Homepage(screen)
Pause = pause.pause_window(screen)
character = char.Character(screen)

windows = ["Quit", "Home", "Paused", "Char", "Game"]
# num = [0, 1, 2, 3, 4]

running = True
num = 1
pre_num = 1
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    if num == 0:
        running = False
    elif num == 1:
        num = homepage.update(events)
        homepage.draw()
        pre_num = 1
    elif num == 2:
        if pre_num == 1:
            homepage.draw()
        elif pre_num == 3:
            character.draw()

        num = Pause.update(events, pre_num)
        Pause.draw()
    elif num == 3:
        num = character.update(events)
        character.draw()
        pre_num = 3
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()