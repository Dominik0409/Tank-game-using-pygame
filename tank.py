import pygame
import math as m
class Ball():
    def __init__(self,game):
        self.game = game
        self.ball = pygame.Rect(10,400,40,40)
        self.xv0 = 2
        self.yv0 = 10
        self.g = 9.8
        self.t = 0 
    def draw(self):
        self.update()
        pygame.draw.circle(self.game.display,(30,40,40),(self.ball.centerx,self.ball.centery),20)
    def update(self):
        if self.ball.right > 800: self.xv0 *= -1
        if self.ball.left < 0: self.xv0 *= -1
        if self.ball.bottom > 720:
            self.t = 0
        self.ball.x += self.xv0
        self.yv = self.yv0 -self.g*self.t
        self.t += 1/60
        print(self.yv)
        self.ball.y -= self.yv
        
class Bullets():
    def __init__(self,game):
        self.game = game
        self.bullets_list = []
        self.bullet_png = pygame.image.load("resources/bullet.png").convert_alpha()
        self.cooldown = 1
    def fire(self,x,y):
        if self.game.space:
            if self.cooldown == 1:
                self.bullets_list.append(pygame.Rect(x,y,10,10))
                self.cooldown = 5
            else: self.cooldown -= 1
    def animate_bullets(self):
        i = 0
        while i < len(self.bullets_list):
            self.bullets_list[i].y -= 10
            self.game.display.blit(self.bullet_png,(self.bullets_list[i].x,self.bullets_list[i].y))
            if self.bullets_list[i].y < 0 or self.bullets_list[i].colliderect(self.game.ball.ball):
                self.bullets_list.pop(i)         
            i += 1
            
        
class Cannon():
    
    def __init__(self,game):
        self.game = game        
        self.tank = pygame.Rect(400,644,80,80)
        self.tank_png = pygame.image.load("resources/tank.png").convert_alpha()
        self.tank_png = pygame.transform.scale(self.tank_png,(80,80))
        
    def update(self):
        if self.game.left:
            self.tank.x -= 10
        if self.game.right:
            self.tank.x += 10
        if self.tank.right > 800:
            self.tank.right = 800
        if self.tank.left < 0:
            self.tank.left = 0
class CannonGame():
    
    def __init__(self):        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((800,800))
        self.running = True
        self.pause = False
        self.can = Cannon(self)
        self.bul = Bullets(self)
        self.ball = Ball(self)
        self.grass1_png = pygame.image.load("resources/grass1.png").convert_alpha()
        self.grass1_png = pygame.transform.scale(self.grass1_png,(80,80))
        self.font = pygame.font.Font("resources/Font1.ttf",30)
        self.left, self.right, self.space = False,False,False
        
        
    def loop(self):
        self.can.update()
        self.bul.fire(self.can.tank.centerx-4,self.can.tank.y)
        self.display.fill((184,234,242))
        self.ball.draw()
        for i in range(10):
            self.display.blit(self.grass1_png, (i*80,720))
            
        self.bul.animate_bullets()
        self.display.blit(self.can.tank_png, (self.can.tank.x,self.can.tank.y))
        self.collision()
    
    def collision(self):
        if self.ball.ball.colliderect(self.can.tank):
            self.gameover()
    
    def gameover(self):
        self.pause = True
        self.display.fill((184,234,242))
        text = self.font.render("Game Over",True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.topleft = (400,400)
        self.display.blit(text,text_rect)
        
        
        
    def reset_keys(self):
        self.left, self.right = False,False
    
    def run(self):
        while self.running:
            while not self.pause:               
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.right = True
                        if event.key == pygame.K_LEFT:
                            self.left = True
                        if event.key == pygame.K_SPACE:
                            self.space = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            self.right = False
                        if event.key == pygame.K_LEFT:
                            self.left = False
                        if event.key == pygame.K_SPACE:
                            self.space = False
                self.loop()
                pygame.display.flip()
                self.clock.tick(60)
        
if __name__ == "__main__":
    game = CannonGame()
    game.run()