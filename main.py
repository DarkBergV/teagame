import pygame
import sys
from sprites import PhysicsEntity
from utils import load_images, load_image, Animation
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
        self.player = PhysicsEntity(self, [0, 0], (32, 32))
        self.clock = pygame.time.Clock()
        self.assets = {
            'player/walk': Animation(load_images('player/walk')),
        }

    def run(self):
        while self.running:
            self.display.fill((155, 155, 155))

            self.player.update(
                (
                    self.movement[0] - self.movement[1],
                    self.movement[2] - self.movement[3],
                )
            )
            self.player.render(self.display, offset=(0, 0))

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

            print(self.movement)
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
