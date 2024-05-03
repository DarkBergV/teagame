import random
import pygame
import sys
from sprites import PhysicsEntity, Player, Flower, Tea, Order
from utils import load_images, Animation, load_image
from tilemap import Tilemap
import datetime
import json
WIN_WIDTH = 640
WIND_HEIGHT = 480
ORDERS = ['camomila', 'mint']


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("cozy spring game")

        #display items
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIND_HEIGHT))
        self.display = pygame.surface.Surface((WIN_WIDTH // 2, WIND_HEIGHT // 2))
        self.running = True
        
        
        self.font = pygame.font.Font(None, size = 50)
        self.clock = pygame.time.Clock()
        self.assets = {
            'order/camomila':load_image('orders/camomila_order.png'),
            'order/mint':load_image('orders/mint_order.png'),
            'order/mix':load_image('orders/mix_order.png'),
            'scenario/carpet':load_images('blocks/scenario'),
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
            'player/side_walk_left':Animation(load_images('player/side_walk_left')),
            'player/side_walk_right':Animation(load_images('player/side_walk_right')),
        }

        #player
        self.player = Player(self, [114, 97], (18, 18))
        self.movement = [0, 0, 0, 0]
        self.scroll = [0, 0]



        self.tilemap = Tilemap(self, 18)

        #order items
        self.test_spawners = []
        self.items = []
        self.tea = []
        self.tea_pos = (0,0)
        self.flavor = ""
        self.make_tea = False
        self.num_orders = 3
        self.orders_made = []
        self.order_flavors = []
        self.tea_flavors = []


        #debugging
        self.pos_item = []
        self.pos_chaleira = []
        #ingrediants list
        self.ingredients = []

        #score items
        self.points = 0
        self.high_score = 0

        #may use it eventually
        self.space = False
        self.load_order()
        self.load_level()
        self.load_high_score()
        
        
    def save_high_score(self, path):
        if self.points>self.high_score:
            f = open(path, 'w')
            json.dump({
                "high_score": self.points 
            },
                f,
            )
            f.close()
        

    def load_high_score(self):
        try:

            f = open("high_score.json", 'r')
            high_score = json.load(f)
            f.close()
            self.high_score =  high_score['high_score']
        except json.decoder.JSONDecodeError:
            print("bruh")

        


    def load_order(self):
       
        for _ in range(self.num_orders):
                x = random.randrange(201, 244)
                y = random.randrange(77, 208)
                
                flavor = random.choice(ORDERS)
                item_x = random.randrange(-5,219 )
                item_y = random.randrange(90, 167 )
                chaleira_x = random.randrange(-5,219 )
                chaleira_y = random.randrange(-54,24 )
                self.items.append(Flower(self,flavor,'flavor',[item_x, item_y],(32,32)))
                self.items.append(Flower(self, 'chaleira','chaleira', [chaleira_x, chaleira_y],(32,32)))
              
                
                self.order_flavors.append(flavor)
            
                self.orders_made.append(Order(self, [x,y], [32,32], flavor))
    
                
                
        

    def load_ingredients(self):
        count = 0
        

        for flavor in self.order_flavors:
                item_x = random.randrange(-5,219 )
                item_y = random.randrange(90, 167 )
                chaleira_x = random.randrange(-5,219 )
                chaleira_y = random.randrange(-54,24 )
                self.items.append(Flower(self,flavor,'flavor',[item_x, item_y],(32,32)))
                self.items.append(Flower(self, 'chaleira','chaleira', [chaleira_x, chaleira_y],(32,32)))
              
                count+=1
           
        self.pos_item.append([item_x, item_y])
        self.pos_chaleira.append([chaleira_x, chaleira_y])

                
      
                

    def load_level(self):
        self.tilemap.load('map.json')
        for wood in self.tilemap.extract([('blocks/wood', 0)], keep = True):
            self.test_spawners.append(pygame.Rect(4 + wood['pos'][0], 4 + wood['pos'][1], 13, 13))
        
        for carpet in self.tilemap.extract([('scenario/carpet',0)], keep = True):
            self.test_spawners.append(pygame.Rect(4 + carpet['pos'][0], 4 + carpet['pos'][1], 20, 20))
        for spawner in self.tilemap.extract([('spawner',0),('spawner',1), ('spawner',2), ('spawner',3)]):
            
            

            if spawner['variant'] == 3:
                self.player.pos = spawner["pos"]

       

                
                


    def run(self):

        while self.running:
           
            
           
            
            #print(len(self.items))
           
            #time logic
          

            timepassed = pygame.time.get_ticks()
            
            clock = datetime.timedelta(seconds=(60 - (timepassed//1000)))
            if ':'.join(str(clock).split(':')[1:4]) == '00:00':
                self.save_high_score('high_score.json')
                pygame.quit()

            timer = self.font.render("timer : " + f"{(':'.join(str(clock).split(':')[1:4]))}", True, (0,0,0))

            #display logic
            self.display.fill((155, 155, 155))
            self.tilemap.render(self.display, offset=self.scroll)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0] )/ 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1] )/ 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #displays ingrediants for making tea
            for i in self.items:
               
                i.render(self.display, offset=(render_scroll))
                make_tea = i.update()
                
        #if it is true it will make tea
                if make_tea:
                    self.make_tea = True
                    
                    
         
            #makes tea
            if self.make_tea:
                tea = Tea(self, 'tea_cup', 'tea',self.tea_pos,(32,32), self.flavor)
                tea.render(self.display, self.scroll)
                self.items.append(tea)
                self.make_tea = False
              

              
                
           
            
            #handles the player movement logic 
            self.player.update(
                self.tilemap, 
                (   
                    self.movement[0] - self.movement[1],
                    self.movement[2] - self.movement[3],
                )
            )
            self.player.render(self.display, offset=render_scroll)
            print('player_position:',self.player.pos)
            #calculates and updates points (todo*** -> save high score in json maybe)
            
            for order in self.orders_made:

                order.render(self.display, offset=render_scroll)
            
                order_points = order.update()
                if order_points:
                    self.points+=1
                    self.orders_made.remove(order)
                
                    
           
            if len(self.orders_made) <=0:
                self.load_order()
              
            points = self.font.render(f'tea served: {self.points}', True, (0,0,0))
            
            #handles movement buttons and logic

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
             

            #scale the game 
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), [0, 0]
            )
            #shows points
            self.screen.blit(points, (50,60))
            #shows timer
            self.screen.blit(timer, (50,30))
            if not self.high_score <= 0:
                player_high_score = self.font.render(f'High score: {self.high_score}',True, (0,0,0))
                self.screen.blit(player_high_score, (300, 30))
        
            pygame.display.update()
            self.clock.tick(60)
            


g = Game()
while g.running:
    g.run()


pygame.quit()
sys.exit()
