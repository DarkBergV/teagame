import pygame
import sys
from sprites import PhysicsEntity, Player
from utils import load_images, Animation
from tilemap import Tilemap
WIN_WIDTH = 640
WIND_HEIGHT = 480


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("cozy spring game")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIND_HEIGHT))
        self.display = pygame.surface.Surface((WIN_WIDTH // 2, WIND_HEIGHT // 2))
        self.running = True
        self.movement = [0, 0, 0, 0]
        self.scroll = [0, 0]
        
        self.clock = pygame.time.Clock()
        self.assets = {
            "blocks/wood":load_images("blocks/wood"),
            'player/walk': Animation(load_images('player/walk')),
            'player/iddle': Animation(load_images('player/iddle')),
            'player/walk_back': Animation(load_images('player/walk_back')),
            'player/iddle_back': Animation(load_images('player/iddle_back')),
        }
        self.player = Player(self, [114, 97], (18, 18))
        self.tilemap = Tilemap(self, 18)
        self.test_spawners = []

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

    def load_level(self):
        self.tilemap.load('map.json')
        for wood in self.tilemap.extract([('wood', 1)], keep = True):
            self.test_spawners.append(pygame.Rect(4+wood['pos'][0], 4 + wood['pos'][1], 23, 13))

        


    def run(self):
        while self.running:
            self.display.fill((155, 155, 155))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0] )/ 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1] )/ 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=self.scroll)

            self.player.update(
                self.tilemap, 
                (   
                    self.movement[0] - self.movement[1],
                    self.movement[2] - self.movement[3],
                )
            )
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    self.movement[0] = True
                elif keys[pygame.K_a]:
                    self.movement[1] = True

                elif keys[pygame.K_w]:
                    self.movement[3] = True

                elif keys[pygame.K_s]:
                    self.movement[2] = True

                else:
                    self.movement[0] = False
                    self.movement[1] = False
                    self.movement[2] = False
                    self.movement[3] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), [0, 0]
            )
            pygame.display.update()
            self.clock.tick(60)


g = Game()
while g.running:
    g.run()


pygame.quit()
sys.exit()
