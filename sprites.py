from shutil import move
import pygame


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, e_type, pos, size, ):
        self.game = game
        self.pos = pos
        self.size = size
        self.type = e_type
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}
        self.flip = False
        print(self.size)
        self.display = pygame.surface.Surface(self.size)
        self.display.fill((198, 55, 32))
        self.action = ''
        self.set_action('walk')
        self.back = False
        
        self.anim_offset = (-3,-3)

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

        entity_rect = self.rect()
        
        self.pos[0] += frame_movement[0]
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0]>0:
                    entity_rect.right = rect.left
                    self.collision['right'] = True

                if frame_movement[0]<0:
                    entity_rect.left = rect.right
                    self.collision['left'] = True

                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]

        for rect in tilemap.physics_rect_around(self.pos):
            print('ashdoiasdoj')
            if entity_rect.colliderect(rect):
                
                if frame_movement[1]>0:
                    entity_rect.bottom = rect.top
                    self.collision['down'] = True

                if frame_movement[1]<0:
                    entity_rect.top = rect.bottom
                    self.collision['up'] = True

                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = True

        if movement[0] < 0:
            self.flip = False

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1]+self.anim_offset[1]))



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


        super().update(tilemap, movement=movement)