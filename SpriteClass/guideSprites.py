import pygame
from etc import etcFuntions


class Guide(pygame.sprite.Sprite):
    def __init__(self, x, y, size, path, text):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.path = path
        self.image = etcFuntions.image_load(self.path, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.touched = 0
        self.text = text
