import pygame
import random
class Destruction():
    def __init__(self,game):
        self.game = game
        self.sheet = pygame.image.load('resources/destroy.png').convert_alpha()
        self.explosions = []
    def explosion_spawn(self,x,y):
        self.explosions.append([1,x,y])
    def draw(self):
        i = 0
        while i < len(self.explosions):
            if self.explosions[i][0] < 15:
                self.game.display.blit(self.sheet,(self.explosions[i][1]-45,self.explosions[i][2]-45),(0,self.explosions[i][0]*150,150,150))
                self.explosions[i][0] += 1
            else: self.explosions.pop(i)
            i += 1
        
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
            if self.bonus_shield[i][0].bottom < self.game.H-108:
                self.bonus_shield[i][0].y += (self.bonus_shield[i][1] + 9.8*self.bonus_shield[i][2])
            else:
                self.bonus_shield[i][0].bottom = self.game.H-108
                
        
    def spawn(self,x,y):
        self.bonus_shield.append([pygame.Rect(x,y,40,40),5,0])
        
class Mine_bonus():
    def __init__(self,game):
        self.game = game
        self.crateL_png = pygame.image.load("resources/crateL.png").convert_alpha()
        self.crateL_png = pygame.transform.scale(self.crateL_png,(40,40))
        self.bonus_mine = []
    def draw(self):
        self.update()
        for i in self.bonus_mine:
            self.game.display.blit(self.crateL_png,(i[0].x,i[0].y))
            
    def update(self):
        for i in range(len(self.bonus_mine)):
            self.bonus_mine[i][2] += 1/60
            if self.bonus_mine[i][0].bottom < self.game.H-108:
                self.bonus_mine[i][0].y += (self.bonus_mine[i][1] + 9.8*self.bonus_mine[i][2])
            else:
                self.bonus_mine[i][0].bottom = self.game.H-108
                
        
    def spawn(self,x,y):
        self.bonus_mine.append([pygame.Rect(x,y,40,40),5,0])
        
        
class Laser():
    def __init__(self,game):
        self.game = game
        self.laser_png = pygame.image.load("resources/mine.png").convert_alpha()
        self.laser_png = pygame.transform.scale(self.laser_png,(60,60))
        self.laser_beam = pygame.image.load("resources/laser.png").convert_alpha()
        self.laser_beam = pygame.transform.scale(self.laser_beam,(60,900))
        self.laser = []
        self.cooldown = 0 
        self.frame = 0
        
    def draw(self):
        self.update()
        for i in self.laser:
            for j in range(17):
                if self.frame < 15:
                    self.game.display.blit(self.laser_beam,(i[0].x,i[0].y-j*60),(0,0+self.frame*60,60,60))
            self.game.display.blit(self.laser_png,(i[0].x,i[0].y))
        self.frame += 1
        if self.frame == 15: self.frame = 0
    
    def update(self):
        self.spawn(self.game.can.tank.x,self.game.can.tank.y)
        if self.cooldown > 0: self.cooldown -= 1
        i = 0
        while i < len(self.laser):
            self.laser[i][1] -= 1/60
            if self.laser[i][1] <= 0:
                self.laser.pop(i)
            i += 1
        
    def spawn(self,x,y):
        if self.game.m == True and self.game.mines_left > 0 and self.cooldown == 0:
            self.cooldown = 60
            self.game.mines_left -= 1
            self.laser.append([pygame.Rect(x,y+48,60,60),5,pygame.Rect(x+20,0,20,self.game.H)])
        
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
            r = i[4]*15
            g = i[4]*15
            b = i[4]*15
            pygame.draw.circle(self.game.display,'black',(i[0].centerx,i[0].centery),30)
            pygame.draw.circle(self.game.display,(160-r,160-g,160-b),(i[0].centerx,i[0].centery),28)
            self.game.drawtext(25,self.game.font,str(i[4]),'white',i[0].centerx,i[0].centery)
    def update(self):
        for i in range(len(self.ball)):
            if self.ball[i][0].right > self.game.W-312: self.ball[i][2] *= -1
            if self.ball[i][0].left < 312: self.ball[i][2] *= -1
            if self.ball[i][0].bottom > self.game.H-108:
                self.ball[i][1] = 0
            self.ball[i][0].x += self.ball[i][2]
            yv = self.ball[i][3] -self.g*self.ball[i][1]
            self.ball[i][1] += 1/60
            self.ball[i][0].y -= yv
        i = 0
        while i < len(self.ball):
            for j in self.game.laser.laser:
                if self.ball[i][0].colliderect(j[2]):
                    self.ball[i][4] -= 1
                    if self.ball[i][4] == 0:
                        self.destroy(i)
                        break
            i += 1
    def spawn(self,probability):
        if random.randint(0,probability) == 1 and self.game.balls_left > 0:
            self.ball.append([pygame.Rect(random.randint(420,self.game.W-520),400,60,60),0,2,10,random.randint(3,10)])
            self.game.balls_left -= 1
            
    def destroy(self,i):
        if random.randint(0,15) == 1:
            self.game.bonus_s.spawn(self.game.ball.ball[i][0].x, self.game.ball.ball[i][0].y)
        if random.randint(0,15) == 2:
            self.game.bonus_m.spawn(self.game.ball.ball[i][0].x, self.game.ball.ball[i][0].y)
        x = self.ball[i][0].x
        y = self.ball[i][0].y
        self.game.des.explosion_spawn(x, y)
        self.ball.pop(i)
        self.game.score += 1
        self.game.sound('pop')
        
class Bullets():
    def __init__(self,game):
        self.game = game
        self.bullets_list = []
        self.bullet_png = pygame.image.load("resources/bullet.png").convert_alpha()
        self.cooldown = 1
    def fire(self,x,y):
        if self.game.space:
            if self.cooldown == 1:
                self.bullets_list.append(pygame.Rect(x-4,y,10,10))
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
                    self.game.points += 1
                    if self.game.ball.ball[j][4] != 1: self.game.ball.ball[j][4] -= 1
                    elif self.game.ball.ball[j][4] == 1:
                        self.game.ball.destroy(j)
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
        self.tank = pygame.Rect(self.game.W/2,-60,108,108)
        self.shield_rect = pygame.Rect(self.game.W/2,-60,216,216)
        self.tank_hitbox = pygame.Rect(self.game.W/2,-60,60,60)
        self.shield = False
        self.tank_png1 = pygame.image.load("resources/tank-1.png").convert_alpha()
        self.tank_png1 = pygame.transform.scale(self.tank_png1,(108,108))
        self.tank_png2 = pygame.image.load("resources/tank-2.png").convert_alpha()
        self.tank_png2 = pygame.transform.scale(self.tank_png2,(108,108))
        self.tank_png3 = pygame.image.load("resources/tank-3.png").convert_alpha()
        self.tank_png3 = pygame.transform.scale(self.tank_png3,(108,108))
        self.tank_png = [self.tank_png1,self.tank_png2,self.tank_png3]
        self.frame = 1
        self.move_left_1 = pygame.image.load("resources/move1.png").convert_alpha()
        self.move_left_1 = pygame.transform.scale(self.move_left_1,(216,108))
        self.move_left_2 = pygame.image.load("resources/move2.png").convert_alpha()
        self.move_left_2 = pygame.transform.scale(self.move_left_2,(216,108))
        self.move_left_3 = pygame.image.load("resources/move3.png").convert_alpha()
        self.move_left_3 = pygame.transform.scale(self.move_left_3,(216,108))
        self.move_left_4 = pygame.image.load("resources/move4.png").convert_alpha()
        self.move_left_4 = pygame.transform.scale(self.move_left_4,(216,108))
        self.move_left_5 = pygame.image.load("resources/move5.png").convert_alpha()
        self.move_left_5 = pygame.transform.scale(self.move_left_5,(216,108))
        self.move_left_6 = pygame.image.load("resources/move6.png").convert_alpha()
        self.move_left_6 = pygame.transform.scale(self.move_left_6,(216,108))
        self.move_left = [self.move_left_1,self.move_left_2,self.move_left_3,self.move_left_4,self.move_left_5,self.move_left_6]
        self.frame_move_left = 0
        self.frame_move_right = 0
        self.shield_png = pygame.image.load("resources/shield.png").convert_alpha()
        self.shield_png = pygame.transform.scale(self.shield_png,(216,216))
        self.shield_time = 0
        
    def update(self):
        if self.game.left:
            self.tank.x -= 10
        if self.game.right:
            self.tank.x += 10
        if self.tank.right > self.game.W-312:
            self.tank.right = self.game.W-312
        if self.tank.left < 312:
            self.tank.left = 312
        self.shield_rect.midbottom = self.tank.midbottom
        self.tank_hitbox.midbottom = self.tank.midbottom
            
    def animation(self):
        if self.game.space:
            self.game.display.blit(self.tank_png[self.frame], (self.tank.x,self.tank.y))
            self.frame += 1
            if self.frame == 3: self.frame = 0
        else:
            self.game.display.blit(self.tank_png[0], (self.tank.x,self.tank.y))
        if self.shield:
            self.game.display.blit(self.shield_png, (self.shield_rect.x,self.shield_rect.y))
            
    def animation_move_left(self):
        if self.game.left:
            self.game.display.blit(self.move_left[int(self.frame_move_left/2)], (self.tank.x,self.tank.y+6))
            self.frame_move_left += 0.5
            if self.frame_move_left == 11: self.frame_move_left = 0
            
    def animation_move_right(self):
        if self.game.right:
            self.game.display.blit(pygame.transform.flip(self.move_left[int(self.frame_move_right/2)],True,False), (self.tank.x-108,self.tank.y+6))
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
        self.W, self.H = 1920,1080
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.W,self.H))
        self.running = True
        self.pause = True
        self.startup = True
        self.can = Cannon(self)
        self.bul = Bullets(self)
        self.ball = Ball(self)
        self.bonus_s = Shield_bonus(self)
        self.bonus_m = Mine_bonus(self)
        self.laser = Laser(self)
        self.des = Destruction(self)
        self.score = 0
        self.score_max = 30
        self.points = 0
        self.mines_left = 2
        self.level = 1
        self.balls_left = 35
        self.current_state = 'Press Enter to play'
        self.grass1_png = pygame.image.load("resources/grass1.png").convert_alpha()
        self.grass1_png = pygame.transform.scale(self.grass1_png,(108,108))
        self.cloud_1_png = pygame.image.load("resources/cloud1.png").convert_alpha()
        self.cloud_1_png = pygame.transform.scale(self.cloud_1_png,(216,108))
        self.cloud_2_png = pygame.image.load("resources/cloud2.png").convert_alpha()
        self.cloud_2_png = pygame.transform.scale(self.cloud_2_png,(216,108))
        self.bg_png = pygame.image.load("resources/bg.png").convert_alpha()
        self.bg_png = pygame.transform.scale(self.bg_png,(self.W-2*312,self.H))
        self.tank_exp = pygame.image.load("resources/tank_exp.png").convert_alpha()
        self.tank_exp = pygame.transform.scale(self.tank_exp,(324,3240))
        self.tank_frame = 15
        self.cloudx = -100
        self.font = "resources/Font1.ttf"
        self.shot = pygame.mixer.Sound("resources/shot.mp3")
        self.engine = pygame.mixer.Sound("resources/engine.mp3")
        self.pop = pygame.mixer.Sound("resources/pop.mp3")
        self.engine_channel = pygame.mixer.Channel(1)
        self.left, self.right, self.space, self.m = False,False,False,False
        
        
    def loop(self):
        if pygame.time.get_ticks() - self.can.shield_time > 5000 and self.can.shield_time != 0:
            self.can.shield = False
            self.shield_time = 0
        self.can.update()
        self.bul.fire(self.can.tank.centerx,self.can.tank.y)
        self.bg()
        self.draw_clouds()
        self.bonus_s.draw()
        self.bonus_m.draw()
        self.ball.draw()
        self.laser.draw()
        self.draw_grass()
        self.bul.animate_bullets()
        self.can.animation()
        self.can.animation_move_left()
        self.can.animation_move_right()
        self.can.engine_sound()
        self.des.draw()
        self.draw_bars()
        self.ball.spawn(100-self.level*7)
        self.collision()
        self.isover()
    
    def loop_dead(self):
        self.bg()
        self.draw_clouds()
        self.ball.draw()
        self.draw_grass()
        self.tank_des(self.can.tank.x-108, self.can.tank.y-108)
        self.drawtext(30,self.font,self.current_state,'white',self.W/2,self.H/2)
        self.draw_bars()
        
    def start_animation(self):
        t = 0
        while self.can.tank.bottom < self.H-108:
            self.bg()
            self.draw_clouds()
            self.can.update()
            self.can.animation()
            self.bonus_s.draw()
            self.bonus_m.draw()
            self.ball.draw()
            self.laser.draw()
            self.draw_grass()
            self.collision()
            self.can.tank.y += 15*t
            self.draw_bars()
            t += 1/60
            pygame.display.flip()
            self.clock.tick(60)
        self.can.tank.bottom = self.H-108
        self.startup = False
            
    
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
        self.display.blit(self.cloud_1_png,(int(self.cloudx)+1200,50))
        self.display.blit(self.cloud_2_png,(int(self.cloudx)+1300,60))
        if self.cloudx == 1000: self.cloudx = -100
        
    def draw_grass(self):
        for i in range(12):
            self.display.blit(self.grass1_png, (312+i*108,self.H-108))
            
    def draw_bars(self):
        pygame.draw.rect(self.display,'black',(0,0,312,1080))
        pygame.draw.rect(self.display,'black',(1608,0,312,1080))
        self.drawtext(20,self.font,f'Level: {self.level}','white',80,self.H-40)
        self.drawtext(20,self.font,f'Score: {self.points}','white',80,self.H-70)
        self.drawtext(20,self.font,f'Balls left: {self.balls_left}','white',80,self.H-100)
        
    def sound(self, sound):
        if sound == 'shot':
            self.shot.play()
        if sound == 'pop':
            self.pop.play()
    
    def bg(self):
        self.display.fill((184,234,242))
        self.display.blit(self.bg_png,(312,150))
        
    def tank_des(self,x,y):
        if self.tank_frame < 14:
            self.display.blit(self.tank_exp,(x,y),(0,0+self.tank_frame*216,324,216))
            self.tank_frame += 1
        if self.tank_frame == 14:
            self.display.blit(self.tank_exp,(x,y),(0,0+self.tank_frame*216,324,216))
            
    def collision(self):
        for i in range(len(self.ball.ball)):
            if self.ball.ball[i][0].colliderect(self.can.tank_hitbox):
                self.gameover()
        if self.can.shield:
            for i in range(len(self.ball.ball)):
                if self.ball.ball[i][0].colliderect(self.can.shield_rect):
                    self.ball.destroy(i)
                    break
        for i in range(len(self.bonus_s.bonus_shield)):
            if self.bonus_s.bonus_shield[i][0].colliderect(self.can.tank):
                self.can.shield = True
                self.can.shield_time = pygame.time.get_ticks()
                self.bonus_s.bonus_shield.pop(i)
                break
            
        for i in range(len(self.bonus_m.bonus_mine)):
            if self.bonus_m.bonus_mine[i][0].colliderect(self.can.tank):
                self.mines_left += 1
                self.bonus_m.bonus_mine.pop(i)
                break
                
    def isover(self):
        if self.score == self.score_max and self.level == 10:
            self.gameover()
        elif self.balls_left == 0 and len(self.ball.ball) == 0:
            self.nextlevel()
            
    
    def gameover(self):
        self.pause = True
        self.current_state = 'Game Over'
        self.level = 1
        self.startup = True
        self.reset()
        
    def nextlevel(self):
        self.pause = True
        self.current_state = 'Press Enter for the next level'
        self.level += 1
        self.startup = True
        self.reset()
        
    def reset(self):
        self.bul = Bullets(self)
        self.bonus_s = Shield_bonus(self)
        self.bonus_m = Mine_bonus(self)
        self.laser = Laser(self)
        self.balls_left = 30 + 5*self.level
        self.left, self.right, self.space, self.m = False,False,False,False
        self.score = 0
        self.tank_frame = 0
    
    def drawtext(self,size,font,text,color,x,y):
        fontwsize = pygame.font.Font(font,size)
        text = fontwsize.render(text,True,color)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text,text_rect)
        
        
        
        
    def reset_keys(self):
        self.left, self.right, self.space, self.m = False,False,False,False
    
    def run(self):
        while self.running:
            while not self.pause:
                if self.startup:
                    self.start_animation()
                else:
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
                            if event.key == pygame.K_m:
                                self.m = True
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT:
                                self.right = False
                            if event.key == pygame.K_LEFT:
                                self.left = False
                            if event.key == pygame.K_SPACE:
                                self.space = False
                            if event.key == pygame.K_m:
                                self.m = False
                    self.loop()
                    pygame.display.flip()
                    self.clock.tick(60)
            while self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.pause = False
                            self.ball = Ball(self)
                            self.can = Cannon(self)
                self.loop_dead()
                pygame.display.flip()
                self.clock.tick(60)
        
if __name__ == "__main__":
    game = CannonGame()
    game.run()