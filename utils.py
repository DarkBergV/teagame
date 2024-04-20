import pygame
import os



IMG_PATH = 'img/'


def load_image(path):
    return pygame.image.load(IMG_PATH + path).convert

def load_images(path):
    images = []

    for image in os.listdir(IMG_PATH + path):
        images.append(load_image(path + '/' + image))

    return images
