from json import load
from turtle import pos
import pygame
import sys
from sprites import PhysicsEntity, Player, Flower
from utils import load_images, Animation, load_image
from tilemap import Tilemap
import datetime
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
        self.font = pygame.font.Font(None, size = 50)
        self.clock = pygame.time.Clock()
        self.assets = {
            'tea/camomila':load_image('items/tea/camomila.png'),
            "blocks/wood":load_images("blocks/wood"),
            'player/walk': Animation(load_images('player/walk')),
            'player/iddle': Animation(load_images('player/iddle')),
            'player/walk_back': Animation(load_images('player/walk_back')),
            'player/iddle_back': Animation(load_images('player/iddle_back')),
        }
        self.player = Player(self, [114, 97], (18, 18))
        self.tilemap = Tilemap(self, 18)
        self.test_spawners = []
        
        self.load_level()

    def load_level(self):
        self.tilemap.load('map.json')
        for wood in self.tilemap.extract([('wood', 1)], keep = True):
            self.test_spawners.append(pygame.Rect(4 + wood['pos'][0], 4 + wood['pos'][1], 23, 13))
        self.items = []
        for spawner in self.tilemap.extract([('spawner',0), ('spawner',3)]):
            if spawner['variant'] == 3:
                self.player.pos = spawner["pos"]
            if spawner['variant'] == 0:
                
                self.items.append(Flower(self, spawner["pos"], (18,18)))
                
                


    def run(self):
        while self.running:
            timepassed = pygame.time.get_ticks()
            
            clock = datetime.timedelta(seconds=(240 - (timepassed//1000)))
            if ':'.join(str(clock).split(':')[1:4]) == '00:00':
                
                pygame.quit()

            self.display.fill((155, 155, 155))
            self.tilemap.render(self.display, offset=self.scroll)
           

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0] )/ 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1] )/ 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            for i in self.items:
                i.render(self.display, offset=render_scroll)
            timer = self.font.render("timer : " + f"{(':'.join(str(clock).split(':')[1:4]))}", True, (0,0,0))
            

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

               
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    elif event.key == pygame.K_a:
                        self.movement[1] = False

                    elif event.key == pygame.K_w:
                        self.movement[3] = False

                    elif event.key == pygame.K_s:
                        self.movement[2] = False


            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), [0, 0]
            )
            self.screen.blit(timer, (50,30))
            pygame.display.update()
            self.clock.tick(60)
            


g = Game()
while g.running:
    g.run()


pygame.quit()
sys.exit()
