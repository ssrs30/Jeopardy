import pygame
import sys
from login import LoginScreen
from game_logic import Game
from shop import Shop

def main():
    # 1. Run Login Module
    # This calls the run() method from your login.py
    login_app = LoginScreen()
    user_name, avatar_path = login_app.run()

    # 2. Setup Main Game Window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Initialize Game with data from Login
    game = Game(questions_file="questions.json")
    game.player.name = user_name
    # Update player avatar logic here if needed
    
    shop = Shop(screen, game.player)
    
    state = "BOARD" # States: BOARD, QUESTION, SHOP, GAMEOVER
    running = True

    while running:
        screen.fill((0, 0, 0))
        
        # --- LOGIC & DRAWING ---
        if state == "BOARD":
            game.draw_board_screen()
            # Draw a small Shop button on the board
            shop_btn = pygame.Rect(700, 20, 80, 40)
            pygame.draw.rect(screen, (128, 0, 128), shop_btn)
            screen.blit(pygame.font.Font(None, 24).render("SHOP", True, (255,255,255)), (715, 30))
            
        elif state == "QUESTION":
            game.draw_question_screen()
            
        elif state == "SHOP":
            shop.draw()

        # Check for Completion Reward
        if game.board.all_answered() and not game.game_over:
            game.player.coins += 1000 # Reward 1000 coins for clearing
            game.game_over = True
            state = "GAMEOVER"

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "BOARD":
                    if shop_btn.collidepoint(event.pos):
                        state = "SHOP"
                    else:
                        game.handle_click(event.pos)
                        if game.question_screen: state = "QUESTION"
                
                elif state == "SHOP":
                    result = shop.handle_click(event.pos)
                    if result == "exit": state = "BOARD"
                
                elif state == "QUESTION":
                    # Manage your question answering logic here
                    # If answer is checked, set state back to BOARD
                    pass

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()