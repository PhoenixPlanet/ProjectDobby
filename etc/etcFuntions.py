import pygame


def image_load(path, size):
    image = pygame.transform.scale(pygame.image.load(path), size)

    return image


def sizeUp(target, xsize):
    return target * xsize