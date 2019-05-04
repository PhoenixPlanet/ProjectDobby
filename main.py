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

# FPS
clock = pygame.time.Clock()

# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# 실제로 y방향 충돌을 감지하는 스프라이트: 자원을 낭비하므로 디버깅할 때만 사용할 것!
dummy_group = pygame.sprite.Group()

t_tile = tiles.Tile("./tiles/stage1_main7.png", 0, 0)
tile_group.add(t_tile)

player1 = players.Player(10, 200, t_tile)
player_group.add(player1)


while True:
    clock.tick_busy_loop(data.FPS)

    window.fill(data.SEMI_SKY)

    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:'''

    tile_group.update()
    tile_group.draw(window)

    player_group.update()
    player_group.draw(window)

    pygame.display.flip()
