import pygame
import sys
from etc import etcFuntions, gamedata, stageFunctions
from SpriteClass import players, tiles, textSprites, guideSprites
import data
import os

itemNameList = ["grass1", "rock1"]
itemXMargin = [10, 0]
itemYMargin = [15, 15]

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobby")
clock = pygame.time.Clock()
fontObj = pygame.font.Font('./Fonts/NanumGothic.ttf', 11)

stageNumFile = open("./UserFile/Stage/stageNum.txt", "r")
stageNum = int(stageNumFile.readline())
stageNumFile.close()

tileList = []
for i in range(24):
    tileList.append([])
    for j in range(16):
        tileList[i].append(0)
tile_surface = pygame.Surface(data.screen)

itemList = []
for i in range(24):
    itemList.append([])
    for j in range(16):
        itemList[i].append(0)
item_surface = pygame.Surface(data.screen)

background_surface = pygame.Surface(data.screen)
background_surface.fill(data.SEMI_SKY)

menu_list = ['Tiles', 'Items', 'Player', 'Enemies', 'Backgrounds', 'Save']
menu_color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0), (128, 0, 128), (0, 128, 128)]
current_menu = 0
current_sub_menu = -1
menu_state = 0

outer_sub_menu = pygame.Rect(0, 20, 720, 50)
inner_sub_menu_rect = []
for i in range(10):
    inner_sub_menu_rect.append(pygame.Rect(50 * i, 20, 50, 50))

sub_menu_tile_image = []
for i in range(6):
    sub_menu_tile_image.append(
        etcFuntions.image_load("./tiles/tile_base/grassTile" + str(i + 1) + ".png", data.basic_tileSize))
sub_menu_tile_image.append(etcFuntions.image_load("./tiles/tile_base/dummy.png", data.basic_tileSize))
sub_menu_item_image = [etcFuntions.image_load("./itemImages/grass1.png", data.basic_tileSize),
                       etcFuntions.image_load("./itemImages/rock1.png", data.basic_tileSize),
                       etcFuntions.image_load("./tiles/tile_base/dummy.png", data.basic_tileSize)]
sub_menu_player_image = [etcFuntions.image_load("./PlayerImages/alienBlue_walk1.png", data.playerSize)]
sub_menu_item_enemy = [etcFuntions.image_load("./enemyImages/enemyBase/blocker.png", data.basic_tileSize),
                       etcFuntions.image_load("./enemyImages/enemyBase/slime.png", data.basic_tileSize)]
sub_menu = [sub_menu_tile_image, sub_menu_item_image, sub_menu_player_image, sub_menu_item_enemy]

menu_rect = []
for i in range(len(menu_list)):
    menu_rect.append(pygame.Rect(70 * i, 0, 70, 20))

click_available = True


def renderTile():
    global tile_surface
    tile_surface = pygame.Surface(data.screen, pygame.SRCALPHA, 32)
    for i in range(24):
        for j in range(16):
            if tileList[i][j] > 0:
                tile_surface.blit(sub_menu_tile_image[tileList[i][j] - 1], (30 * i, 30 * j))
    window.blit(tile_surface, (0, 0))


def renderItem():
    global item_surface
    item_surface = pygame.Surface(data.screen, pygame.SRCALPHA, 32)
    for i in range(24):
        for j in range(16):
            if itemList[i][j] > 0:
                item_surface.blit(sub_menu_item_image[itemList[i][j] - 1], (30 * i, 30 * j))
    window.blit(item_surface, (0, 0))


def checkMousePosition():
    mousePos = [int(pygame.mouse.get_pos()[0] // 30), int(pygame.mouse.get_pos()[1] // 30)]
    return mousePos


while True:
    window.fill(data.WHITE)

    if not pygame.mouse.get_pressed()[0]:
        click_available = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

    # 가이드 라인
    for i in range(int(720 / 30)):
        pygame.draw.line(window, data.GREY, (30 * i, 0), (30 * i, 480))

    for i in range(int(480 / 30)):
        pygame.draw.line(window, data.GREY, (0, 30 * i), (720, 30 * i))

    renderItem()
    renderTile()

    # 오브젝트 리스트 메뉴
    for i in range(len(menu_list)):
        pygame.draw.rect(window, menu_color[i], menu_rect[i])
        textSurfaceObj = fontObj.render(menu_list[i], True, (0, 0, 0))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.centerx, textRectObj.y = (menu_rect[i].centerx, menu_rect[i].y + 1)
        window.blit(textSurfaceObj, textRectObj)

        # 메뉴 클릭 감지
        if menu_rect[i].collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                and pygame.mouse.get_pressed()[0] and click_available:
            click_available = False
            if i == current_menu:
                if menu_state == 1:
                    menu_state = 0
                else:
                    menu_state = 1
            else:
                if menu_state == 0:
                    menu_state = 1
                current_menu = i
                current_sub_menu = -1

    if menu_state == 1:
        if current_menu == 5:
            stageNumFile = open("./UserFile/Stage/stageNum.txt", "w")
            stageNum += 1
            stageNumFile.write(str(stageNum))
            stageNumFile.close()
            pygame.image.save(tile_surface, "./UserFile/Stage/tile" + str(stageNum) + ".png")
            pygame.image.save(tile_surface, "./UserFile/Stage/background" + str(stageNum) + ".png")
            itemF = open("./UserFile/Stage/item" + str(stageNum) + ".txt", "w")
            for i in range(24):
                for j in range(16):
                    if itemList[i][j] > 0:
                        itemF.write(
                            itemNameList[itemList[i][j] - 1] + " " + str(i * 30) + " " + str(j * 30 + 30) + " 30 30 50 "
                            + itemNameList[itemList[i][j] - 1] + " 3 " + str(itemXMargin[itemList[i][j] - 1])
                            + " " + str(itemYMargin[itemList[i][j] - 1])+"\n")
            itemF.close()
            quit()
            sys.exit()
        pygame.draw.rect(window, data.SEMI_BLACK, outer_sub_menu)
        if current_menu != 4:
            for i in range(len(sub_menu[current_menu])):
                pygame.draw.rect(window, data.BLACK, inner_sub_menu_rect[i], 1)
                if current_menu != 2:
                    window.blit(sub_menu[current_menu][i], (50 * i + 10, 30))
                else:
                    window.blit(sub_menu[current_menu][i], (50 * i + 10, 20))

                if inner_sub_menu_rect[i].collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                        and pygame.mouse.get_pressed()[0] and click_available:
                    click_available = False
                    current_sub_menu = i

            if outer_sub_menu.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                    and pygame.mouse.get_pos()[0] > 50 * len(sub_menu[current_menu]) \
                    and pygame.mouse.get_pressed()[0] and click_available:
                click_available = False
                current_sub_menu = -1

        # 타일 선택했을 때
        if current_menu == 0:
            window.blit(sub_menu_tile_image[current_sub_menu],
                        (30 * checkMousePosition()[0], 30 * checkMousePosition()[1]))
            if pygame.mouse.get_pressed()[0] and click_available:
                i, j = checkMousePosition()
                if j > 1:
                    tileList[i][j] = current_sub_menu + 1

        # 아이템 선택했을 때
        if current_menu == 1:
            window.blit(sub_menu_item_image[current_sub_menu],
                        (30 * checkMousePosition()[0], 30 * checkMousePosition()[1]))
            if pygame.mouse.get_pressed()[0] and click_available:
                i, j = checkMousePosition()
                if j > 1:
                    itemList[i][j] = current_sub_menu + 1

    clock.tick_busy_loop(data.FPS)
    pygame.display.flip()
