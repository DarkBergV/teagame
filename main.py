from itertools import count
from json import load
from turtle import pos
import pygame
import sys
from sprites import PhysicsEntity, Player, Flower, Tea
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
            'tea/tea_cup/mint':load_image('items/cup/tea_protag_iddle_back1.png'),
            'tea/tea_cup/camomila':load_image('items/cup/tea_cup.png'),
            'tea/chaleira':load_image('items/chaleira/chaleira.png'),
            'tea/camomila':load_image('items/tea/camomila.png'),
            'tea/mint':load_image('items/tea/mint.png'),
            "blocks/wood":load_images("blocks/wood"),
            'player/walk': Animation(load_images('player/walk')),
            'player/iddle': Animation(load_images('player/iddle')),
            'player/walk_back': Animation(load_images('player/walk_back')),
            'player/iddle_back': Animation(load_images('player/iddle_back')),
        }
        self.player = Player(self, [114, 97], (18, 18))
        self.tilemap = Tilemap(self, 18)
        self.test_spawners = []
        self.items = []
        
        self.space = False
        self.tea_pos = (0,0)
        self.flavor = ""
        self.make_tea = False
        self.load_level()

    def load_level(self):
        self.tilemap.load('map.json')
        for wood in self.tilemap.extract([('wood', 1)], keep = True):
            self.test_spawners.append(pygame.Rect(4 + wood['pos'][0], 4 + wood['pos'][1], 23, 13))
        
        for spawner in self.tilemap.extract([('spawner',0),('spawner',1), ('spawner',2), ('spawner',3)]):
            
            if spawner['variant'] == 0:
                
                self.items.append(Flower(self,'camomila', spawner["pos"], (32,32)))
            if spawner['variant'] == 1:
                
                self.items.append(Flower(self,'chaleira', spawner["pos"], (30,32)))
            
            
            if spawner['variant'] == 2:
                self.items.append(Flower(self,'mint', spawner["pos"], (30,32)))

            if spawner['variant'] == 3:
                self.player.pos = spawner["pos"]
                
                


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
                
                i.render(self.display, offset=(render_scroll))
                make_tea = i.update()
                

                if make_tea:
                    self.make_tea = True
                    
                    if len(self.items) == 0:
                        break

            print(len(self.items))

            if self.make_tea:
                tea = Tea(self, 'tea_cup', self.tea_pos,(32,32), self.flavor)
                tea.render(self.display, self.scroll)
                self.items.append(tea)
                self.make_tea = False


              
                
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

                elif keys[pygame.K_SPACE]:
                    self.space = True
                
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    elif event.key == pygame.K_a:
                        self.movement[1] = False

                    elif event.key == pygame.K_w:
                        self.movement[3] = False

                    elif event.key == pygame.K_s:
                        self.movement[2] = False
                    
                    elif event.key == pygame.K_SPACE:
                        self.space = False
                        print(self.space)


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
