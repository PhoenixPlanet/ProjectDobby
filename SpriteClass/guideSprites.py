import pygame
from etc import etcFuntions
import data


class LifeBar:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.innerXSize = data.lifeBarSize[0] - 0.4
        self.innerYSize = data.lifeBarSize[1] - 0.2
        self.outer = pygame.Rect((self.x, self.y), data.lifeBarSize)
        self.inner = pygame.Rect((self.x + 0.2, self.y + 0.1), (self.innerXSize, self.innerYSize))

    def draw(self, window, x, y, life, max_life):
        self.x, self.y = x, y
        self.outer.x, self.outer.y = self.x, self.y
        self.inner.x = self.outer.x + 0.2
        self.inner.y = self.outer.y + 0.1
        self.inner.width = (float(life) / max_life) * self.innerXSize
        pygame.draw.rect(window, (0, 0, 0), self.outer, 1)
        pygame.draw.rect(window, (255, 0, 0), self.inner)


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


class MouseGuide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.image = etcFuntions.image_load("./PlayerImages/walking_dummy2.png", (1, 1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.rect.x, self.rect.y = self.x, self.y


class ItemGuide(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos[0] - size[0], pos[1] - size[1]
        self.text = text.split("\n")
        self.image = pygame.transform.flip(etcFuntions.image_load("./guideImage/glassPanel_cornerBL.png", size), 1, 0)

        t = 0
        y = 10
        for i in self.text:
            if t % 2 == 0:
                fontObj = pygame.font.Font('./Fonts/NanumGothic.ttf', 10)
                fontObj.set_bold(True)
                if t != 0:
                    y += 16
            else:
                fontObj = pygame.font.Font('./Fonts/NanumGothic.ttf', 14)
                y += 12
            textSurfaceObj = fontObj.render(i, True, (0, 93, 180))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.x, textRectObj.y = (10, y)
            self.image.blit(textSurfaceObj, textRectObj)
            t += 1

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
