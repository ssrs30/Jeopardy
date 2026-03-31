import pygame
import sys
import os
import json
import threading
import LLM

pygame.init()

# ================== 基础设置 ==================
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeopardy Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GRAY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

FONT_L = pygame.font.Font(None, 48)
FONT_M = pygame.font.Font(None, 36)
FONT_S = pygame.font.Font(None, 24)

# ================== 登录界面 ==================
class LoginScreen:
    def __init__(self):
        self.username = ""
        self.input_active = False
        self.selected_path = None
        self.avatar_folder = "avatar"
        self.avatars = []
        os.makedirs(self.avatar_folder, exist_ok=True)
        self.load_avatars()

    def load_avatars(self):
        for f in os.listdir(self.avatar_folder):
            if f.endswith((".png",".jpg",".jpeg")):
                path = os.path.join(self.avatar_folder, f)
                img = pygame.image.load(path)
                img = pygame.transform.scale(img,(80,80))
                self.avatars.append((img,path))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            screen.fill(WHITE)

            title = FONT_L.render("LOGIN", True, BLACK)
            screen.blit(title,(WIDTH//2-80,50))

            input_rect = pygame.Rect(300,150,400,50)
            pygame.draw.rect(screen, BLACK, input_rect,2)

            txt = FONT_M.render(self.username, True, BLACK)
            screen.blit(txt,(input_rect.x+10,input_rect.y+10))

            avatar_rects=[]
            for i,(img,path) in enumerate(self.avatars):
                x = 200 + (i%5)*100
                y = 250 + (i//5)*100
                rect = pygame.Rect(x,y,80,80)
                screen.blit(img,(x,y))
                avatar_rects.append((rect,path))
                if self.selected_path == path:
                    pygame.draw.rect(screen,YELLOW,rect,3)

            btn = pygame.Rect(400,650,200,60)
            pygame.draw.rect(screen,BLUE,btn)
            screen.blit(FONT_M.render("START",True,WHITE),(440,665))

            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit();sys.exit()

                if e.type==pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(e.pos):
                        self.input_active=True
                    else:
                        self.input_active=False

                    for r,p in avatar_rects:
                        if r.collidepoint(e.pos):
                            self.selected_path=p

                    if btn.collidepoint(e.pos):
                        if self.username and self.selected_path:
                            return self.username,self.selected_path

                if e.type==pygame.KEYDOWN and self.input_active:
                    if e.key==pygame.K_BACKSPACE:
                        self.username=self.username[:-1]
                    else:
                        self.username+=e.unicode

            pygame.display.flip()
            clock.tick(60)

# ================== 商店 ==================
class Shop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 36)

        self.items = [
            {"name":"Skip","price":200},
            {"name":"Shield","price":300}
        ]

        self.exit_btn = pygame.Rect(400,700,200,50)

    def draw(self):
        self.screen.fill((30,30,60))

        coin = self.font.render(f"Coins: {self.player.coins}",True,WHITE)
        self.screen.blit(coin,(50,50))

        for i,item in enumerate(self.items):
            rect = pygame.Rect(200,150+i*120,600,80)
            pygame.draw.rect(self.screen,BLUE,rect)
            txt = self.font.render(f"{item['name']} - {item['price']}",True,WHITE)
            self.screen.blit(txt,(rect.x+20,rect.y+20))
            item["rect"]=rect

        pygame.draw.rect(self.screen,(128,0,128),self.exit_btn)
        self.screen.blit(self.font.render("EXIT",True,WHITE),(450,710))

    def handle(self,pos):
        if self.exit_btn.collidepoint(pos):
            return "EXIT"

        for item in self.items:
            if item["rect"].collidepoint(pos):
                if self.player.coins>=item["price"]:
                    self.player.coins-=item["price"]

# ================== 玩家 ==================
class Player:
    def __init__(self,name,avatar):
        self.name=name
        self.avatar=avatar
        self.score=0
        self.coins=1000
        self.inventory={}

# ================== 游戏 ==================
class Game:
    def __init__(self, player):
        self.player=player
        self.shop = Shop(screen,player)
        self.in_shop=False

    def run(self):
        clock = pygame.time.Clock()

        while True:
            screen.fill(BLACK)

            # UI
            name = FONT_M.render(f"Player: {self.player.name}",True,YELLOW)
            screen.blit(name,(20,20))

            score = FONT_M.render(f"Score: {self.player.score}",True,YELLOW)
            screen.blit(score,(20,60))

            hint = FONT_S.render("Press S to open Shop",True,WHITE)
            screen.blit(hint,(20,100))

            if self.in_shop:
                self.shop.draw()

            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit();sys.exit()

                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_s:
                        self.in_shop = not self.in_shop

                if e.type==pygame.MOUSEBUTTONDOWN:
                    if self.in_shop:
                        res=self.shop.handle(e.pos)
                        if res=="EXIT":
                            self.in_shop=False

            pygame.display.flip()
            clock.tick(60)

# ================== 主程序 ==================
if __name__ == "__main__":
    login = LoginScreen()
    username, avatar = login.run()

    player = Player(username, avatar)

    game = Game(player)
    game.run()