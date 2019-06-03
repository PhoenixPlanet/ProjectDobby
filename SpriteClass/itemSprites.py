import pygame
from etc import etcFuntions


class Item(pygame.sprite.Sprite):
    def __init__(self, itemData):
        pygame.sprite.Sprite.__init__(self)

        self.itemData = itemData

        self.type = itemData[0]
        self.x = int(itemData[1])
        self.width = int(itemData[3])
        self.height = int(itemData[4])
        self.y = int(itemData[2]) - self.height
        self.life = int(itemData[5])
        self.returnType = itemData[6]
        self.returnValue = int(itemData[7])

        self.path = "./itemImages/" + self.type + ".png"

        self.size = (self.width, self.height)
        self.image = etcFuntions.image_load(self.path, self.size, True, (0,0,0))
        self.rect = self.image.get_rect()

    def mined(self, damage):
        self.life -= damage

    def return_things(self):
        return self.returnType, self.returnValue

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.image.set_alpha(255 - self.life)
        # print("%d %d %d %d %d" % (self.x, self.y, self.life, self.width, self.height))
