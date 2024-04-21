import pygame
import os


IMG_PATH = "img/"


def load_image(path):
    return pygame.image.load(IMG_PATH + path).convert()


def load_images(path):
    images = []

    for image in os.listdir(IMG_PATH + path):
        images.append(load_image(path + "/" + image))

    return images


class Animation:
    def __init__(self, images, img_duration=5, loop=True):
        self.images = images
        self.img_duration = img_duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))

        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)

            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

            else:
                self.frame += 1

    def img(self):
        return self.images[self.frame // self.img_duration]
