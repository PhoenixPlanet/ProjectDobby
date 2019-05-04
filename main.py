import pygame
import sys

pygame.init()

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = (720, 480)
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobby")
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# 캐릭터, 타일 크기 설정
playerSize = (33, 48)
dummyMargin = int(playerSize[0] / 4.7)
dummyPlayerSize = (playerSize[0] - dummyMargin*2, playerSize[1])
tileSize = screen

# FPS
clock = pygame.time.Clock()
FPS = 60

# 색깔들
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SEMI_SKY = (214, 255, 255)

# 플레이어 이동 속도, 애니메이션 프레임
pXVel = 2
animRate = 12
frameForAnim = 0

# y방향 가속도(중력 가속도로 작용)
pYAcc = 0.5  # (0.5px * 60^2 / s^2)

# 점프 세기
jumpF = -8

# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# 실제로 y방향 충돌을 감지하는 스프라이트: 자원을 낭비하므로 디버깅할 때만 사용할 것!
dummy_group = pygame.sprite.Group()


def image_load(path, size):
    image = pygame.transform.scale(pygame.image.load(path), size)

    return image


# 스프라이트 클래스들
# 타일 클래스
class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_load(image_path, tileSize)
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, 0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y


t_tile = Tile("./tiles/stage1_main7.png", 0, 0)
tile_group.add(t_tile)


class dummyPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.dy = 0
        self.dx = 0
        self.image = image_load("./Player1/walking_dummy2.png", (w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x, self.rect.y = self.x, self.y

    def get_info(self):
        return self.x, self.y


# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.dy = 0
        self.dx = 0

        self.walk_image = [image_load("./Player1/alienBlue_walk1.png", playerSize),
                           image_load("./Player1/alienBlue_walk2.png", playerSize)]
        self.rect = self.walk_image[0].get_rect()
        self.imageNum = 0
        self.image = self.walk_image[self.imageNum]
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.jumpState = 0

    def move(self, dx, dy, image=False):
        self.x += dx
        self.y += dy

        if image:
            if self.imageNum == 1:
                self.imageNum = 0
            else:
                self.imageNum = 1

        if self.direction == 1:
            self.image = pygame.transform.flip(self.walk_image[self.imageNum], 1, 0)
        else:
            self.image = self.walk_image[self.imageNum]

        self.mask = pygame.mask.from_surface(self.image)

    def pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x, self.rect.y = self.x, self.y

    # x 방향으로 움직이는 것이 가능한 지 확인할 것!
    def x_check_move(self, dx):
        dummy = dummyPlayer(self.x + dummyMargin, self.y, dummyPlayerSize[0], dummyPlayerSize[1])
        dummy.move(dx, 0)
        # dummy_group.add(dummy)

        i = 0
        while True:
            if (not (pygame.sprite.collide_mask(dummy, t_tile))) or i > 7:
                break
            dummy.move(0, -1)
            i += 1

        if i > 7:
            is_ok = 0
        else:
            is_ok = 1

        if is_ok == 1:
            if i != 0:
                self.y = dummy.y
                self.rect.y = self.y
            self.dx = dx
            self.move(self.dx, 0, frameForAnim == animRate)
            if pygame.sprite.collide_mask(dummy, t_tile):
                while pygame.sprite.collide_mask(dummy,t_tile):
                    if self.dx > 0:
                        self.x -= 0.1
                        self.rect.x = self.x
                    else:
                        self.x -= 0.1
                        self.rect.x = self.x

        # dummy_group.draw(window)

    # 중력 구현
    def check_ground(self):
        dummy = dummyPlayer(self.x+dummyMargin, self.y, dummyPlayerSize[0], dummyPlayerSize[1])

        if pygame.sprite.collide_mask(dummy, t_tile):
            if self.dy < 0:
                while pygame.sprite.collide_mask(dummy, t_tile):
                    dummy.move(0, 1)

                print(self.y)
                self.y = dummy.y
                print(self.y)
                self.dy = 0

            else:
                while pygame.sprite.collide_mask(dummy, t_tile):
                    dummy.move(0, -1)

                self.dy = 0
                self.y = dummy.y
                self.jumpState = 1

            self.rect.y = self.y

        # 디버깅 테스트용
        # dummy_group.add(dummy)
        # dummy_group.draw(window)

    def update(self):
        global frameForAnim

        key = pygame.key.get_pressed()

        self.dy += pYAcc

        # 점프
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            if self.jumpState:
                self.y -= 1
                self.rect.y = self.y

                self.dy = jumpF
                self.jumpState = 0

        self.y += self.dy

        # 좌우 이동
        if key[pygame.K_RIGHT]:
            if self.direction == 1:
                self.direction = 0
            self.dx = pXVel
            self.x_check_move(self.dx)

        elif key[pygame.K_LEFT]:
            if self.direction == 0:
                self.direction = 1
            self.dx = -pXVel
            self.x_check_move(self.dx)

        else:
            self.imageNum = 0
            self.dx = 0
            if self.direction == 1:
                self.image = pygame.transform.flip(self.walk_image[self.imageNum], 1, 0)
            else:
                self.image = self.walk_image[self.imageNum]

        # 화면 밖으로 떨어지면 위치 초기화
        if self.y > screen[1]:
            self.x = 10
            self.y = 10
            self.dy = 0

        # 프레임 수 초기화
        if frameForAnim == animRate:
            frameForAnim = 0

        frameForAnim += 1

        # 위치 지정 및 땅 감지
        self.rect.x, self.rect.y = self.x, self.y
        self.check_ground()


player1 = Player(10, 200)
player_group.add(player1)


while True:
    clock.tick_busy_loop(FPS)

    window.fill(SEMI_SKY)
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
