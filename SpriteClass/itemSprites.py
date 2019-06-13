import pygame
from etc import etcFuntions
from. import guideSprites


class Item(pygame.sprite.Sprite):
    def __init__(self, itemData, window):
        pygame.sprite.Sprite.__init__(self)

        self.itemData = itemData
        self.window = window

        self.type = itemData[0]
        self.x = int(itemData[1])
        self.width = int(itemData[3])
        self.height = int(itemData[4])
        self.y = int(itemData[2]) - self.height
        self.life = int(itemData[5])
        self.returnType = itemData[6]
        self.returnValue = int(itemData[7])
        self.xMargin = int(itemData[8])
        self.yMargin = int(itemData[9])

        self.dummyRect = pygame.Rect(self.x + self.xMargin, self.y + self.yMargin,
                                     self.width - (self.xMargin * 2), self.height - self.yMargin)

        self.path = "./itemImages/" + self.type + ".png"

        self.size = (self.width, self.height)
        self.image = etcFuntions.image_load(self.path, self.size, True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)

        self.guide = pygame.sprite.Group()
        self.guide.add(guideSprites.ItemGuide((self.dummyRect.x, self.dummyRect.y), (100, 100), "Type\n"
                                                                             "%s\n"
                                                                             "Return\n"
                                                                             "%s\n"
                                                                             "Return Value\n"
                                                                             "%d"
                                              % (self.type, self.returnType, self.returnValue), (0, 0)))

    def mined(self, damage):
        self.life -= damage

    def return_things(self):
        return self.returnType, self.returnValue

    def update(self):
        self.image.set_alpha(255 - self.life)

        if self.dummyRect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.guide.update()
            self.guide.draw(self.window)

