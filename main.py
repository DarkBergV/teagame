import pygame
import sys 
WIN_WIDTH = 640
WIND_HEIGHT = 480

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('cozy spring game')
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIND_HEIGHT))
        self.display = pygame.surface.Surface((WIN_WIDTH//2, WIND_HEIGHT//2))
        self.running = True


    def run(self):
        while self.running:
            self.display.fill((155,155,155))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),[0,0])




g = Game()
while g.running:
    g.run()


pygame.quit()
sys.exit()