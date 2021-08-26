import pygame
class Cannon():
    
    def __init__(self,game):
        self.game = game        
        self.head = pygame.Rect(400,760,40,40)
        
    def update(self):
        if self.game.left:
            self.head.x -= 10
        if self.game.right:
            self.head.x += 10
        
class CannonGame():
    
    def __init__(self):        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((800,800))
        self.running = True
        self.can = Cannon(self)
        self.left, self.right = False,False
        
    def loop(self):
        self.can.update()
        self.display.fill((255,0,0))
        pygame.draw.rect(self.display,(255,255,255),self.can.head)
        
        
    def reset_keys(self):
        self.left, self.right = False,False
    
    def run(self):
        while self.running:
            pygame.init()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.right = True
                    if event.key == pygame.K_LEFT:
                        self.left = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.right = False
                    if event.key == pygame.K_LEFT:
                        self.left = False
            self.loop()
            pygame.display.flip()
            self.clock.tick(60)
        
if __name__ == "__main__":
    game = CannonGame()
    game.run()