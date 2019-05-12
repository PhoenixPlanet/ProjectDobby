import pygame
from etc import etcFuntions
from . import guideSprites


class Text(guideSprites.Guide):
    def __init__(self, x, y, size, path, text):
        guideSprites.Guide.__init__(self, x, y, size, path, text)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = etcFuntions.image_load(self.path, tuple(map(etcFuntions.sizeUp, self.size)))
            self.touched = 1

        else:
            self.image = etcFuntions.image_load(self.path, self.size)
            self.touched = 0

