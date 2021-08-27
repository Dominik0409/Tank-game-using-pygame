import pygame
import random
class Ball():
    def __init__(self,game):
        self.game = game
        self.ball = []
        self.xv0 = 2
        self.yv0 = 10
        self.g = 9.8
        self.t = 0 
    def draw(self):
        self.update()
        for i in self.ball:
            pygame.draw.circle(self.game.display,(30,40,40),(i[0].centerx,i[0].centery),20)
            self.game.drawtext(20,self.game.font,str(i[4]),'white',i[0].x+13,i[0].y+5)
    def update(self):
        for i in range(len(self.ball)):
            if self.ball[i][0].right > 800: self.ball[i][2] *= -1
            if self.ball[i][0].left < 0: self.ball[i][2] *= -1
            if self.ball[i][0].bottom > 720:
                self.ball[i][1] = 0
            self.ball[i][0].x += self.ball[i][2]
            yv = self.ball[i][3] -self.g*self.ball[i][1]
            self.ball[i][1] += 1/60
            print(yv)
            self.ball[i][0].y -= yv
    def spawn(self):
        if random.randint(0,100) == 1:
            self.ball.append([pygame.Rect(random.randint(100,700),400,40,40),0,2,10,5])
        
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
                self.cooldown = 6
            else: self.cooldown -= 1
    def animate_bullets(self):
        i = 0
        while i < len(self.bullets_list):
            self.bullets_list[i].y -= 10
            self.game.display.blit(self.bullet_png,(self.bullets_list[i].x,self.bullets_list[i].y))
            for j in range(len(self.game.ball.ball)):
                if self.bullets_list[i].colliderect(self.game.ball.ball[j][0]):
                    self.bullets_list.pop(i)
                    if self.game.ball.ball[j][4] != 1: self.game.ball.ball[j][4] -= 1
                    elif self.game.ball.ball[j][4] == 1:
                        self.game.ball.ball.pop(j) 
                        self.game.score += 1
                    break
            i += 1
        i = 0
        while i < len(self.bullets_list):
            if self.bullets_list[i].y < 0:
                self.bullets_list.pop(i)
                break
            i += 1
            
        
class Cannon():
    
    def __init__(self,game):
        self.game = game        
        self.tank = pygame.Rect(400,660,60,60)
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
        self.score = 0
        self.grass1_png = pygame.image.load("resources/grass1.png").convert_alpha()
        self.grass1_png = pygame.transform.scale(self.grass1_png,(80,80))
        self.font = "resources/Font1.ttf"
        self.left, self.right, self.space = False,False,False
        
        
    def loop(self):
        self.can.update()
        self.bul.fire(self.can.tank.centerx+5,self.can.tank.y)
        self.display.fill((184,234,242))
        pygame.draw.rect(self.display,'red',pygame.Rect(0,0,800*(self.score/100),20))
        self.ball.draw()
        for i in range(10):
            self.display.blit(self.grass1_png, (i*80,720))
            
        self.bul.animate_bullets()
        self.display.blit(self.can.tank_png, (self.can.tank.x,self.can.tank.y-16))
        self.ball.spawn()
        self.collision()
        self.isover()
    
    def collision(self):
        for i in range(len(self.ball.ball)):
            if self.ball.ball[i][0].colliderect(self.can.tank):
                self.gameover()
    def isover(self):
        if self.score == 100:
            self.gameover()
    
    def gameover(self):
        self.pause = True
        self.display.fill((184,234,242))
        self.drawtext(30,self.font,'Game Over','white',400,400)
        
    def reset(self):
        self.can = Cannon(self)
        self.bul = Bullets(self)
        self.ball = Ball(self)
        self.left, self.right, self.space = False,False,False
        self.pause = False
    
    def drawtext(self,size,font,text,color,x,y):
        fontwsize = pygame.font.Font(font,size)
        text = fontwsize.render(text,True,color)
        text_rect = text.get_rect()
        text_rect.topleft = (x,y)
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset()
        
if __name__ == "__main__":
    game = CannonGame()
    game.run()