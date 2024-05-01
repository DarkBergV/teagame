from os import remove
from pkgutil import iter_modules
import pygame


ITEM_MAKER = ['camomila', 'chaleira', 'mint']

TEA_FLAVORS = ['camomila', 'mint']

ITEM_LIST = ['flavor', 'chaleira']

class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, e_type, pos, size, ):
        self.game = game
        self.pos = pos
        self.size = size
        self.type = e_type
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}
        self.flip = False
        self.display = pygame.surface.Surface(self.size)
        self.display.fill((198, 55, 32))
        self.action = ''
        self.set_action('walk')
        self.back = False
      
        
        self.anim_offset = (-3,-3)
        self.mov= [0,0]
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type +"/"+self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).copy()

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = [
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        ]

        self.mov[0] =  frame_movement[0]
        self.mov[1] =  frame_movement[1]

        entity_rect = self.rect()
        
        self.pos[0] += frame_movement[0]
        for rect in tilemap.physics_rect_around(self.pos):
            
            if entity_rect.colliderect(rect):
                if frame_movement[0] < 0:
                    #self.pos[0] = entity_rect.x
                    #self.pos[1] = self.pos[1]
                    
                    entity_rect.left = rect.right - entity_rect.width
               
                if frame_movement[0]>0:
                    
                    entity_rect.right = rect.left 
             

            self.pos[0] = entity_rect.x


                
        entity_rect_y = self.rect()
        self.pos[1] += frame_movement[1]
        

        for rect in tilemap.physics_rect_around(self.pos):
            
            if entity_rect_y.colliderect(rect):
                
                
                if frame_movement[1]>0:
                    entity_rect_y.bottom = rect.top

                if frame_movement[1]<0:
                    entity_rect_y.top = rect.bottom

            self.pos[1] = entity_rect_y.y
                    
                    
                    

                

        if movement[0] > 0:
            self.flip = True

        if movement[0] < 0:
            self.flip = False

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1]+self.anim_offset[1]))




class MovableObject(pygame.sprite.Sprite):
    def __init__(self, game, e_type, item_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = pos
        self.size = size
        self.item_type = item_type
        


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).copy()
    

    def render(self, surf, offset=(0,0)):
        rect = self.rect().center
        self.img = self.game.assets["tea/" + self.e_type].copy()
        rect = self.pos
        surf.blit(self.img, (rect[0] - offset[0], rect[1] - offset[1]) )

    def update(self):
        pass


class Player(PhysicsEntity):

    def __init__(self, game, pos, size,):
        super().__init__(game, 'player', pos, size,)

    def update(self, tilemap, movement = (0,0)):
        
        


        if movement[1] < 0:
            self.set_action('walk_back')
            self.back = True

        elif movement[1] > 0:
            self.set_action('walk')
            self.back = False
    
        
        elif movement[1] == 0 and not self.back:
            self.set_action('iddle')

        elif movement[1] == 0 and self.back:
            self.set_action('iddle_back')

        tea_rects = [tea for tea in self.game.items]
        for tea in tea_rects:
            rect = tea.rect()
            if self.rect().colliderect(rect):
                if self.mov[0] > 0:
                    self.pos[0] = rect.left - self.rect().width
                    tea.pos[0] +=0.5

                elif self.mov[0] < 0:
                    self.pos[0] = rect.right
                    tea.pos[0] -=0.5   
                    
                if self.mov[1] > 0:
                    self.pos[1] = rect.top - self.rect().height  
                    tea.pos[1] +=0.5  
                elif self.mov[1] < 0:
                    self.pos[1] = rect.bottom
                    tea.pos[1] -=0.5


                
                
        
        super().update(tilemap, movement=movement)
    
    def collect_items(self):
        tea_rects = [tea for tea in self.game.items]
        for item in tea_rects:
            item.move_item()
            




class Flower(MovableObject):
    def __init__(self,game,e_type,item_type, pos, size):
        super().__init__(game,e_type,item_type, pos, size)
    def move_item(self):
        print(self.game.player.rect())
        
        self.pos[0] += 1

    def update(self):
        items = [item for item in self.game.items]
        
        for item in items:
            
            if self.rect().colliderect(item.rect()) and self.e_type != item.e_type and self.e_type in ITEM_MAKER and self.e_type in ITEM_MAKER and self.item_type != item.item_type and self.item_type in ITEM_LIST and item.item_type in ITEM_LIST:
                
                self.game.items.remove(item)
                for j in self.game.items:
                    if j.pos == self.pos:
                        self.game.items.remove(j)
                if self.e_type in TEA_FLAVORS:
                
                    self.game.flavor = self.e_type
                if item.e_type in TEA_FLAVORS:
                    self.game.flavor = item.e_type

                self.game.tea_pos = item.pos
                return True

        super().update()
    


        
       


class Tea(MovableObject):
    def __init__(self, game, e_type,item_type, pos, size, flavor):
        super().__init__(game, e_type,item_type, pos, size)
        self.flavor = flavor

      

    
    
    def render(self, surf, offset=(0,0)):
        rect = self.rect().center
        
        self.img = self.game.assets["tea/" + self.e_type + "/" + self.flavor].copy()
        rect = self.pos
        surf.blit(self.img, (rect[0] - offset[0], rect[1] - offset[1]))



class Order(pygame.sprite.Sprite):
    def __init__(self,game,pos, size, flavor):
        self.game = game
        self.pos = pos
        self.size = size
        self.flavor = flavor

    def rect(self):
        
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).copy()
    
    def update(self):
        items = [item for item in self.game.items]
        
        for item in items:
            
            if self.rect().colliderect(item.rect()) and  item.item_type == 'tea' and item.flavor == self.flavor:
                print("amongus")
                self.game.items.remove(item)
                for j in self.game.items:
                    if j.pos == self.pos:
                        self.game.items.remove(j)

                self.game.tea_pos = item.pos
                return True
                

    def render(self, surf, offset = (0,0)):
        self.img = self.game.assets['order/' + self.flavor].copy()
        rect = self.rect()
        surf.blit(self.img, (rect[0]-offset[0], rect[1] - offset[1]))

    


        