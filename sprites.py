import pygame


class PhysicsEntity:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = pos
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}
        self.flip = False
        self.display = pygame.surface.Surface(self.size)
        self.display.fill((198, 55, 32))

    def rec(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).copy()

    def update(self, movement=(0, 0)):
        frame_movement = [
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        ]

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        if movement[0] > 0:
            self.flip = True

        if movement[0] < 0:
            self.flip = False

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.display, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
