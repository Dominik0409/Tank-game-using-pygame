import pygame
import random
class Shield_bonus():
    def __init__(self,game):
        self.game = game
        self.crate_png = pygame.image.load("resources/crate.png").convert_alpha()
        self.crate_png = pygame.transform.scale(self.crate_png,(40,40))
        self.bonus_shield = []
    def draw(self):
        self.update()
        for i in self.bonus_shield:
            self.game.display.blit(self.crate_png,(i[0].x,i[0].y))
            
    def update(self):
        for i in range(len(self.bonus_shield)):
            self.bonus_shield[i][2] += 1/60
            if self.bonus_shield[i][0].bottom < 700:
                self.bonus_shield[i][0].y += (self.bonus_shield[i][1] + 9.8*self.bonus_shield[i][2])
            else:
                self.bonus_shield[i][0].bottom = 700
                
        
    def spawn(self,x,y):
        self.bonus_shield.append([pygame.Rect(x,y,20,20),5,0])
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
            self.game.drawtext(20,self.game.font,str(i[4]),'white',i[0].centerx,i[0].centery)
    def update(self):
        for i in range(len(self.ball)):
            if self.ball[i][0].right > 800: self.ball[i][2] *= -1
            if self.ball[i][0].left < 0: self.ball[i][2] *= -1
            if self.ball[i][0].bottom > 720:
                self.ball[i][1] = 0
            self.ball[i][0].x += self.ball[i][2]
            yv = self.ball[i][3] -self.g*self.ball[i][1]
            self.ball[i][1] += 1/60
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
                self.game.sound('shot')
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
                        if random.randint(0,10) == 1:
                            self.game.bonus_s.spawn(self.game.ball.ball[j][0].x, self.game.ball.ball[j][0].y)
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
        self.shield_rect = self.tank.copy()
        self.shield_rect.inflate_ip(100,100)
        self.shield = False
        self.tank_png1 = pygame.image.load("resources/tank-1.png").convert_alpha()
        self.tank_png1 = pygame.transform.scale(self.tank_png1,(80,80))
        self.tank_png2 = pygame.image.load("resources/tank-2.png").convert_alpha()
        self.tank_png2 = pygame.transform.scale(self.tank_png2,(80,80))
        self.tank_png3 = pygame.image.load("resources/tank-3.png").convert_alpha()
        self.tank_png3 = pygame.transform.scale(self.tank_png3,(80,80))
        self.tank_png = [self.tank_png1,self.tank_png2,self.tank_png3]
        self.frame = 1
        self.move_left_1 = pygame.image.load("resources/move1.png").convert_alpha()
        self.move_left_1 = pygame.transform.scale(self.move_left_1,(160,80))
        self.move_left_2 = pygame.image.load("resources/move2.png").convert_alpha()
        self.move_left_2 = pygame.transform.scale(self.move_left_2,(160,80))
        self.move_left_3 = pygame.image.load("resources/move3.png").convert_alpha()
        self.move_left_3 = pygame.transform.scale(self.move_left_3,(160,80))
        self.move_left_4 = pygame.image.load("resources/move4.png").convert_alpha()
        self.move_left_4 = pygame.transform.scale(self.move_left_4,(160,80))
        self.move_left_5 = pygame.image.load("resources/move5.png").convert_alpha()
        self.move_left_5 = pygame.transform.scale(self.move_left_5,(160,80))
        self.move_left_6 = pygame.image.load("resources/move6.png").convert_alpha()
        self.move_left_6 = pygame.transform.scale(self.move_left_6,(160,80))
        self.move_left = [self.move_left_1,self.move_left_2,self.move_left_3,self.move_left_4,self.move_left_5,self.move_left_6]
        self.frame_move_left = 0
        self.frame_move_right = 0
        self.shield_png = pygame.image.load("resources/shield.png").convert_alpha()
        self.shield_png = pygame.transform.scale(self.shield_png,(160,160))
        self.shield_time = 0
        
    def update(self):
        if self.game.left:
            self.tank.x -= 10
        if self.game.right:
            self.tank.x += 10
        if self.tank.right > 800:
            self.tank.right = 800
        if self.tank.left < 0:
            self.tank.left = 0
        self.shield_rect.midbottom = self.tank.midbottom
            
    def animation(self):
        if self.game.space:
            self.game.display.blit(self.tank_png[self.frame], (self.tank.x,self.tank.y-16))
            self.frame += 1
            if self.frame == 3: self.frame = 0
        else:
            self.game.display.blit(self.tank_png[0], (self.tank.x,self.tank.y-16))
        if self.shield:
            self.game.display.blit(self.shield_png, (self.tank.x-40,self.tank.y-96))
            
    def animation_move_left(self):
        if self.game.left:
            self.game.display.blit(self.move_left[int(self.frame_move_left/2)], (self.tank.x,self.tank.y-16))
            self.frame_move_left += 0.5
            if self.frame_move_left == 11: self.frame_move_left = 0
            
    def animation_move_right(self):
        if self.game.right:
            self.game.display.blit(pygame.transform.flip(self.move_left[int(self.frame_move_right/2)],True,False), (self.tank.x-80,self.tank.y-16))
            self.frame_move_right += 0.5
            if self.frame_move_right == 11: self.frame_move_right = 0
            
    def engine_sound(self):
        if self.game.right or self.game.left:
            if not self.game.engine_channel.get_busy(): self.game.engine_channel.play(self.game.engine)
        else: self.game.engine_channel.stop()
            
        
            
class CannonGame():
    
    def __init__(self):        
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((800,800))
        self.running = True
        self.pause = True
        self.can = Cannon(self)
        self.bul = Bullets(self)
        self.ball = Ball(self)
        self.bonus_s = Shield_bonus(self)
        self.score = 0
        self.grass1_png = pygame.image.load("resources/grass1.png").convert_alpha()
        self.grass1_png = pygame.transform.scale(self.grass1_png,(80,80))
        self.cloud_1_png = pygame.image.load("resources/cloud1.png").convert_alpha()
        self.cloud_1_png = pygame.transform.scale(self.cloud_1_png,(160,80))
        self.cloud_2_png = pygame.image.load("resources/cloud2.png").convert_alpha()
        self.cloud_2_png = pygame.transform.scale(self.cloud_2_png,(160,80))
        self.cloudx = -100
        self.font = "resources/Font1.ttf"
        self.shot = pygame.mixer.Sound("resources/shot.mp3")
        self.engine = pygame.mixer.Sound("resources/engine.mp3")
        self.engine_channel = pygame.mixer.Channel(1)
        self.shot_channel = pygame.mixer.Channel(2)
        self.left, self.right, self.space = False,False,False
        
        
    def loop(self):
        if pygame.time.get_ticks() - self.can.shield_time > 5000 and self.can.shield_time != 0:
            self.can.shield = False
            self.shield_time = 0
        self.can.update()
        self.bul.fire(self.can.tank.centerx+5,self.can.tank.y)
        self.display.fill((184,234,242))
        self.draw_clouds()
        pygame.draw.rect(self.display,'red',pygame.Rect(0,0,800*(self.score/100),20))
        self.bonus_s.draw()
        self.ball.draw()
        for i in range(10):
            self.display.blit(self.grass1_png, (i*80,720))
            
        self.bul.animate_bullets()
        self.can.animation()
        self.can.animation_move_left()
        self.can.animation_move_right()
        self.can.engine_sound()
        self.ball.spawn()
        self.collision()
        self.isover()
    
    def draw_clouds(self):
        self.cloudx += 0.5
        self.display.blit(self.cloud_1_png,(int(self.cloudx)-400,50))
        self.display.blit(self.cloud_2_png,(int(self.cloudx)-300,60))
        self.display.blit(self.cloud_1_png,(int(self.cloudx),50))
        self.display.blit(self.cloud_2_png,(int(self.cloudx)+100,60))
        self.display.blit(self.cloud_1_png,(int(self.cloudx)+400,50))
        self.display.blit(self.cloud_2_png,(int(self.cloudx)+500,60))
        self.display.blit(self.cloud_1_png,(int(self.cloudx)+800,50))
        self.display.blit(self.cloud_2_png,(int(self.cloudx)+900,60))
        if self.cloudx == 300: self.cloudx = -100
        
    def idle_screen(self):
        self.display.fill((184,234,242))
        self.drawtext(30,self.font,'Press Enter to play','white',400,400)
        pygame.display.flip()
    
    def sound(self, sound):
        if sound == 'shot':
            self.shot_channel.play(self.shot)
    
    def collision(self):
        for i in range(len(self.ball.ball)):
            if self.ball.ball[i][0].colliderect(self.can.tank):
                self.gameover()
        if self.can.shield:
            for i in range(len(self.ball.ball)):
                if self.ball.ball[i][0].colliderect(self.can.shield_rect):
                    self.ball.ball.pop(i)
                    break
        for i in range(len(self.bonus_s.bonus_shield)):
            if self.bonus_s.bonus_shield[i][0].colliderect(self.can.tank):
                self.can.shield = True
                self.can.shield_time = pygame.time.get_ticks()
                self.bonus_s.bonus_shield.pop(i)
                break
                
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
        text_rect.center = (x,y)
        self.display.blit(text,text_rect)
        
        
        
        
    def reset_keys(self):
        self.left, self.right = False,False
    
    def run(self):
        self.idle_screen()
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