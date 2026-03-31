import pygame
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Login - Avatar Selection")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
BLUE = (0, 120, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)
FONT_L = pygame.font.Font(None, 50)
FONT_S = pygame.font.Font(None, 30)

class LoginScreen:
    def __init__(self):
        self.username = ""
        self.input_active = False
        self.error_msg = ""
        
        # Avatar
        self.avatar_folder = "avatar"
        self.selected_path = None      
        self.avatars = []              
        if not os.path.exists(self.avatar_folder):
            os.makedirs(self.avatar_folder)
        
        self.load_avatars()

    def load_avatars(self):
        """Scan the folder and pre-load images as thumbnails"""
        self.avatars = []
        valid_exts = ('.png', '.jpg', '.jpeg', '.bmp')
        
        if not os.path.exists(self.avatar_folder):
            return

        files = [f for f in os.listdir(self.avatar_folder) if f.lower().endswith(valid_exts)]
        
        for f in files:
            path = os.path.join(self.avatar_folder, f)
            try:
                img = pygame.image.load(path).convert_alpha()
                display_img = pygame.transform.smoothscale(img, (80, 80))
                self.avatars.append({"path": path, "img": display_img})
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def run(self):
        clock = pygame.time.Clock()

        while True:
            screen.fill(WHITE)
            
            #Title
            title_surf = FONT_L.render("USER LOGIN", True, BLACK)
            screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 40))

            # Username Input Box
            input_rect = pygame.Rect(250, 140, 300, 50)
            border_color = BLUE if self.input_active else DARK_GRAY
            pygame.draw.rect(screen, border_color, input_rect, 2)
            
            name_surf = FONT_S.render(self.username + ("|" if self.input_active else ""), True, BLACK)
            screen.blit(name_surf, (input_rect.x + 10, input_rect.y + 15))
            
            label_name = FONT_S.render("Username:", True, BLACK)
            screen.blit(label_name, (input_rect.x, input_rect.y - 30))

            grid_label = FONT_S.render("Select your Avatar:", True, BLACK)
            screen.blit(grid_label, (100, 230))
            
            grid_x, grid_y = 100, 260
            avatar_rects = [] 
            
            if not self.avatars:
                warn_surf = FONT_S.render("No images found in /avatar folder!", True, RED)
                screen.blit(warn_surf, (grid_x, grid_y))
            
            for i, data in enumerate(self.avatars):
                col = i % 6
                row = i // 6
                x = grid_x + col * (80 + 20)
                y = grid_y + row * (80 + 20)
                
                rect = pygame.Rect(x, y, 80, 80)
                avatar_rects.append((rect, data['path']))
                
                if self.selected_path == data['path']:
                    pygame.draw.rect(screen, GOLD, rect.inflate(10, 10), 4)
                
                screen.blit(data['img'], (x, y))

            btn_login = pygame.Rect(300, 500, 200, 55)
            pygame.draw.rect(screen, BLUE, btn_login, border_radius=10)
            btn_text = FONT_S.render("LOGIN", True, WHITE)
            screen.blit(btn_text, (btn_login.centerx - btn_text.get_width()//2, btn_login.centery - btn_text.get_height()//2))

            if self.error_msg:
                error_surf = FONT_S.render(self.error_msg, True, RED)
                screen.blit(error_surf, (WIDTH//2 - error_surf.get_width()//2, 460))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click input box
                    if input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                    
                    # Click avatar
                    for rect, path in avatar_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_path = path
                    
                    # Click login button
                    if btn_login.collidepoint(event.pos):
                        if not self.username.strip():
                            self.error_msg = "Please enter a username!"
                        elif not self.selected_path:
                            self.error_msg = "Please select an avatar!"
                        else:
                            return self.username, self.selected_path

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.input_active = False
                    else:
                        if len(self.username) < 12:
                            self.username += event.unicode

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    login = LoginScreen()
    user_name, avatar_file = login.run()
    
    print("-" * 30)
    print(f"Login Successful!")
    print(f"User: {user_name}")
    print(f"File: {avatar_file}")
    print("-" * 30)
    
    # After login,start game
    pygame.quit()
