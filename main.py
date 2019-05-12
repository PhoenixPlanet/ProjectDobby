import pygame
import sys
from etc import etcFuntions
from SpriteClass import players, tiles, textSprites, guideSprites
import data

pygame.init()

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobby")
background = etcFuntions.image_load("./background/stage1_background1.png", screen)
lobbyBackground = etcFuntions.image_load("./background/lobby.png", screen)
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# 게임 흐름
gameState = data.gameStateList["lobby"]
stageNum = 0
stageBackgroundImageList = ["./background/stage1_background1.png", "./background/stage1_background2.png"]
stageTileImageList = ["./tiles/stage1_main1.png", "./tiles/stage1_main2.png"]
goNext = True
isClicked = 0
ticksForAll = 0
storyLine = 0

# FPS
clock = pygame.time.Clock()

# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()
guide_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
# 실제로 y방향 충돌을 감지하는 스프라이트: 디버깅할 때만 사용하자
dummy_group = pygame.sprite.Group()

# 스프라이트
t_tile = tiles.Tile("./tiles/stage1_main1.png", 0, 0)
tile_group.add(t_tile)

player1 = players.Player(50, 200, t_tile)
player_group.add(player1)

howToMoveSprite = 0

# 스테이지 관련 변수들
backgroundPos = [0, 0]
ticksForStageChange = 0

backgroundPreImage = 0
backgroundNewImage = 0
tilePreImage = 0
tileNewImage = 0
backgroundDX = 0
playerDxForChangeStage = 0
playerPosForChangeStage = []


# def set_stage(stageNumber):


def change_stage(new_background, new_tile, isNext=True):
    global background, backgroundPos, backgroundDX, gameState,\
        playerDxForChangeStage, t_tile, player1, ticksForStageChange

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


def initialize():
    global gameState, stageNum

    text_group.add(textSprites.Text(70, 140, (110, 60), "./textImage/play.png", "play"))
    gameState = data.gameStateList["lobby"]
    stageNum = 0


initialize()

while True:
    clock.tick_busy_loop(data.FPS)
    if (not pygame.mouse.get_pressed()[0]) and isClicked == 1:
        isClicked = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:'''

    if gameState == data.gameStateList["lobby"]:
        window.fill(data.SEMI_SKY)
        window.blit(lobbyBackground, (0, 0))

        text_group.update()
        text_group.draw(window)
        for t in text_group:
            if t.touched == 1:
                if pygame.mouse.get_pressed()[0] and isClicked == 0:
                    isClicked = 1
                    if t.text == "play":
                        gameState = data.gameStateList["normal"]
                        ticksForAll = 0

    elif gameState == data.gameStateList["normal"]:
        window.fill(data.SEMI_SKY)
        window.blit(background, backgroundPos)

        tile_group.update()
        tile_group.draw(window)

        player_group.update()
        player_group.draw(window)

        dummy_player_rect = pygame.Rect((player1.x - 5, player1.y), (data.playerSize[0] + 10, data.playerSize[1]))

        for item in item_group:
            if dummy_player_rect.colliderect(item.rect):
                item.detectPlayer = True
            else:
                item.detectPlayer = False

        if ticksForAll == 100:
            howToMoveSprite = guideSprites.Guide(0, 20, (132, 93), "./guideImage/guide1.png", "howToMove")
            howToMoveSprite.rect.centerx = 360
            guide_group.add(howToMoveSprite)

        elif 500 >= ticksForAll > 100:
            guide_group.draw(window)

        elif ticksForAll > 500:
            howToMoveSprite.kill()

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

    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    textSurfaceObj = fontObj.render("x: %d, y: %d" % (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), True, (0, 0, 0), (255, 255, 255))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (360, 10)
    window.blit(textSurfaceObj, textRectObj)

    pygame.display.flip()

    ticksForAll += 1
