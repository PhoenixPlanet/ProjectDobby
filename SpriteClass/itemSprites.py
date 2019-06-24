import pygame
from etc import etcFuntions, gamedata
from . import guideSprites
import data
import math


class Item(pygame.sprite.Sprite):
    def __init__(self, itemData, window):
        pygame.sprite.Sprite.__init__(self)

        self.window = window

        self.itemData = itemData

        self.type = itemData[0]
        self.x = int(itemData[1])
        self.width = int(itemData[3])
        self.height = int(itemData[4])
        self.y = int(itemData[2]) - self.height
        self.max_life = int(itemData[5])
        self.life = self.max_life
        self.returnType = itemData[6]
        self.returnValue = int(itemData[7])
        self.marginX = int(itemData[8])
        self.marginY = int(itemData[9])

        self.path = "./itemImages/" + self.type + ".png"

        self.size = (self.width, self.height)
        self.image = etcFuntions.image_load(self.path, self.size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.mouse_sprite = guideSprites.MouseGuide()
        self.guide = pygame.sprite.Group()
        self.lifebar = guideSprites.LifeBar()
        self.guide.add(guideSprites.ItemGuide((self.x + self.marginX, self.y + self.marginY), (100, 100),
                                              "Type\n"
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
        self.mouse_sprite.update()
        self.rect.x, self.rect.y = self.x, self.y
        if self.life != self.max_life:
            self.lifebar.draw(self.window,
                              self.rect.x + (self.width / 2 - data.lifeBarSize[0] / 2),
                              self.y + self.marginY - 4,
                              self.life,
                              self.max_life)

        if pygame.sprite.collide_mask(self, self.mouse_sprite):
            if pygame.mouse.get_pressed()[0] and not gamedata.gameFlowData.get_game_data().isClicked:
                gamedata.gameFlowData.get_game_data().isClicked = True
                playerX = gamedata.gameFlowData.get_game_data().sprite_groups.player.x
                playerY = gamedata.gameFlowData.get_game_data().sprite_groups.player.y
                math.sqrt((playerX - self.x)**2 + (playerY - self.y)**2)

            self.guide.update()
            self.guide.draw(self.window)

