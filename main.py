import pygame
import sys
from etc import etcFuntions, gamedata, stageFunctions
from SpriteClass import players, tiles, textSprites, guideSprites
import data
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobby")
background = etcFuntions.image_load("./UserFile/Stage/background1.png", screen)
lobbyBackground = etcFuntions.image_load("./background/lobby.png", screen)
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# 게임 흐름
isClicked = 0
ticksForAll = 0
storyLine = 0

# FPS
clock = pygame.time.Clock()

# 스프라이트 그룹
text_group = pygame.sprite.Group()
guide_group = pygame.sprite.Group()
# 실제로 y방향 충돌을 감지하는 스프라이트: 디버깅할 때만 사용하자
dummy_group = pygame.sprite.Group()

# 스프라이트 그룹들을 모아놓은 클래스
sprite_groups = gamedata.SpriteGroups()
sprite_groups.add_tile("./UserFile/Stage/tile1.png", 0, 0)
sprite_groups.init_player(50, 200)

howToMoveSprite = 0

gameFlowData = gamedata.gameFlowData.get_game_data()
gameFlowData.set_window(window)
gameFlowData.set_sprite_groups()


text_group.add(textSprites.Text(70, 140, (110, 60), "./textImage/play.png", "play"))


etcFuntions.gameInit(gameFlowData)


while True:
    clock.tick_busy_loop(data.FPS)

    if (not pygame.mouse.get_pressed()[0]) and isClicked == 1:
        isClicked = 0

    if not pygame.mouse.get_pressed()[0]:
        gamedata.gameFlowData.get_game_data().isClicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:'''

    if gameFlowData.gameState == data.gameStateList["lobby"]:
        window.fill(data.SEMI_SKY)
        window.blit(lobbyBackground, (0, 0))

        text_group.update()
        text_group.draw(window)
        for t in text_group:
            if t.touched == 1:
                if pygame.mouse.get_pressed()[0] and isClicked == 0:
                    isClicked = 1
                    if t.text == "play":
                        gameFlowData.gameState = data.gameStateList["normal"]
                        ticksForAll = 0

    elif gameFlowData.gameState == data.gameStateList["normal"]:
        window.fill(data.SEMI_SKY)
        window.blit(gameFlowData.background, gameFlowData.backgroundPos)

        gameFlowData.sprite_groups.update_sprites(window)

        if ticksForAll == 100:
            howToMoveSprite = guideSprites.Guide(300, 20, (132, 93), "./guideImage/guide1.png", "howToMove")
            guide_group.add(howToMoveSprite)

        elif 500 >= ticksForAll > 100:
            guide_group.draw(window)

        elif ticksForAll > 500:
            howToMoveSprite.kill()

        if gameFlowData.sprite_groups.player.rect.centerx >= 680 and \
                gameFlowData.stageNum < len(gameFlowData.stageBackgroundImageList) - 1:
            gameFlowData.init_stage(True)

        if gameFlowData.sprite_groups.player.rect.centerx <= 40 and gameFlowData.stageNum > 0:
            gameFlowData.init_stage(False)

    elif gameFlowData.gameState == data.gameStateList["changeStage"]:
        gameFlowData.change_stage()

    etcFuntions.showMousePos(window)

    pygame.display.flip()

    ticksForAll += 1
