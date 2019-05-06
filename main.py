import pygame
import sys
from etc import etcFuntions
from Characters import players, tiles
import data

pygame.init()

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobby")
background = etcFuntions.image_load("./background/stage1_background1.png", screen)
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# 게임 흐름
gameState = data.gameStateList["normal"]
stageNum = 0
stageBackgroundImageList = ["./background/stage1_background1.png", "./background/stage1_background2.png"]
stageTileImageList = ["./tiles/stage1_main1.png", "./tiles/stage1_main2.png"]
goNext = True

# FPS
clock = pygame.time.Clock()

# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# 실제로 y방향 충돌을 감지하는 스프라이트: 디버깅할 때만 사용하자
dummy_group = pygame.sprite.Group()

t_tile = tiles.Tile("./tiles/stage1_main1.png", 0, 0)
tile_group.add(t_tile)

player1 = players.Player(50, 200, t_tile)
player_group.add(player1)

backgroundPos = [0, 0]
ticksForStageChange = 0

backgroundPreImage = 0
backgroundNewImage = 0
tilePreImage = 0
tileNewImage = 0
backgroundDX = 0
playerDxForChangeStage = 0
playerPosForChangeStage = []


def change_stage(new_background, new_tile, isNext=True):
    global background, backgroundPos, backgroundDX, gameState, playerDxForChangeStage, t_tile, player1, ticksForStageChange

    window.fill(data.SEMI_SKY)

    t = ticksForStageChange

    if isNext:
        a = ((6 * 720) / (data.changeStageSpeed ** 3))
        b = ((6 * 639) / (data.changeStageSpeed ** 3))
    else:
        a = ((-6 * 720) / (data.changeStageSpeed ** 3))
        b = ((-6 * 639) / (data.changeStageSpeed ** 3))

    backgroundDX = a * ((t ** 2) - (data.changeStageSpeed * t))
    backgroundPos[0] += backgroundDX

    if isNext:
        newX = backgroundPos[0] + screen[0]
    else:
        newX = backgroundPos[0] - screen[0]

    window.blit(backgroundPreImage, backgroundPos)
    window.blit(backgroundNewImage, (newX, backgroundPos[1]))
    window.blit(tilePreImage, backgroundPos)
    window.blit(tileNewImage, (newX, backgroundPos[1]))

    playerDxForChangeStage = b * ((t ** 2) - (data.changeStageSpeed * t))
    playerPosForChangeStage[0] += playerDxForChangeStage
    player1.pos(playerPosForChangeStage[0], playerPosForChangeStage[1])
    player_group.draw(window)

    if t == data.changeStageSpeed:
        background = etcFuntions.image_load(new_background, screen)
        gameState = data.gameStateList["normal"]
        t_tile.kill()
        t_tile = tiles.Tile(new_tile, 0, 0)
        player1.t_tile = t_tile
        tile_group.add(t_tile)
        backgroundPos = (0, 0)

    ticksForStageChange += 1


while True:
    clock.tick_busy_loop(data.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:'''

    if gameState == data.gameStateList["normal"]:
        window.fill(data.SEMI_SKY)

        window.blit(background, backgroundPos)

        tile_group.update()
        tile_group.draw(window)

        player_group.update()
        player_group.draw(window)

        if player1.rect.centerx >= 680 and stageNum < len(stageBackgroundImageList) - 1:
            gameState = data.gameStateList["changeStage"]
            ticksForStageChange = 0
            backgroundPos = [0, 0]
            stageNum += 1
            goNext = True
            playerPosForChangeStage = [player1.x, player1.y]
            backgroundPreImage = background
            backgroundNewImage = etcFuntions.image_load(stageBackgroundImageList[stageNum], screen)
            tilePreImage = t_tile.image
            tileNewImage = etcFuntions.image_load(stageTileImageList[stageNum], screen)

        if player1.rect.centerx <= 40 and stageNum > 0:
            gameState = data.gameStateList["changeStage"]
            ticksForStageChange = 0
            backgroundPos = [0, 0]
            stageNum -= 1
            goNext = False
            playerPosForChangeStage = [player1.x, player1.y]
            backgroundPreImage = background
            backgroundNewImage = etcFuntions.image_load(stageBackgroundImageList[stageNum], screen)
            tilePreImage = t_tile.image
            tileNewImage = etcFuntions.image_load(stageTileImageList[stageNum], screen)

    elif gameState == data.gameStateList["changeStage"]:
        change_stage(stageBackgroundImageList[stageNum], stageTileImageList[stageNum], goNext)

    pygame.display.flip()
