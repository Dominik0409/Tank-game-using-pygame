import pygame

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((200,200))
        self.running = True
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
g = SnakeGame()
g.run()
        