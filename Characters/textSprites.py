import pygame
from etc import etcFuntions
import data


class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, size, path):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.path = path
        self.image = etcFuntions.image_load(self.path, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = etcFuntions.image_load(self.path, list(map(etcFuntions.sizeUp, self.size, 1.2)))

