import pygame
import data


def image_load(path, size, isAlpha=False, color_key=(255, 255, 255)):
    image = pygame.transform.scale(pygame.image.load(path), size)

    if isAlpha:
        image = image.convert()
        image.set_colorkey(color_key)
        image.set_colorkey((255, 255, 255))
    return image


def sizeUp(target):
    return int(target * 1.2)


def showMousePos(window):
    # fontObj = pygame.font.Font('./Fonts/caviar_dreams/CaviarDreams.ttf', 16)
    fontObj = pygame.font.Font('./Fonts/NanumGothic.ttf', 16)
    textSurfaceObj = fontObj.render("x: %d, y: %d" % (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), True,
                                    (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (360, 10)
    window.blit(textSurfaceObj, textRectObj)


def gameInit(gameFlowData):
    gameFlowData.gameState = data.gameStateList["lobby"]
    gameFlowData.stageNum = 0