import pygame


def image_load(path, size, isAlpha=False, color_key=(255, 255, 255)):
    image = pygame.transform.scale(pygame.image.load(path), size)

    if isAlpha:
        image = image.convert()
        image.set_colorkey(color_key)
        image.set_colorkey((255, 255, 255))
    return image


def sizeUp(target):
    return int(target * 1.2)