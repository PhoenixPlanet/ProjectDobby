import pygame
import sys

pygame.init()

# 게임 화면 설정
screen = (720, 480)
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dobbys")
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# 캐릭터, 타일 크기 설정
playerSize = (33, 48)
tileSize = (15, 15)

# FPS
clock = pygame.time.Clock()
FPS = 60

# 색깔들
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 플레이어 이동 속도, 애니메이션 프레임
pXVel = 1
animRate = 15
frameForAnim = 0

# y방향 가속도(중력 가속도로 작용)
pYAcc = 0.5

# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
        self.rect = pygame.Rect(self.x, self.y, tileSize[0], 1)

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y


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

    def pos(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        global frameForAnim

        tileCollide = 0
        tileY = 0

        key = pygame.key.get_pressed()
        tile_list = pygame.sprite.spritecollide(self, tile_group, False)

        if len(tile_list) > 0:
            for targetTile in tile_list:
                if targetTile.y + 1 == self.y + playerSize[1]:
                    tileCollide = 1
                    tileY = targetTile.y
                    break
                elif targetTile.y + 1 < self.y + playerSize[1]:
                    tileCollide = 2
                    tileY = targetTile.y
                    break

        # 중력 작용
        if tileCollide == 0:
            self.y += self.dy
            self.dy += pYAcc
        elif tileCollide == 1 or tileCollide == 2:
            if self.dy < 0:
                self.y += 5
                self.dy = 0
                tileCollide = 0
            else:
                self.y = tileY + 1 - playerSize[1]
                self.dy = 0

        # 이동
        if key[pygame.K_RIGHT]:
            if self.direction == 1:
                self.direction = 0
            self.dx = pXVel
            self.move(self.dx, 0, frameForAnim == animRate)

        elif key[pygame.K_LEFT]:
            if self.direction == 0:
                self.direction = 1
            self.dx = -pXVel
            self.move(self.dx, 0, frameForAnim == animRate)

        else:
            self.imageNum = 0
            self.dx = 0
            if self.direction == 1:
                self.image = pygame.transform.flip(self.walk_image[self.imageNum], 1, 0)
            else:
                self.image = self.walk_image[self.imageNum]

        # x 방향 충돌 감지(현재 작동 안함->고칠것!)
        if (tileCollide == 1 or tileCollide == 2) and self.dx != 0 and self.dy != 0:
            self.x += self.dx / pXVel * (-3)

        # 점프
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            if tileCollide == 1 or tileCollide == 2:
                self.dy = -6
                self.y -= 1

        # 화면 밖으로 떨어지면 위치 초기화
        if self.y > screen[1]:
            self.x = 10
            self.y = 280
            self.dy = 0

        # 프레임 수 초기화
        if frameForAnim == animRate:
            frameForAnim = 0

        frameForAnim += 1
        self.rect.x = 3
        self.rect.x, self.rect.y = self.x, self.y


player1 = Player(10, 300)
player_group.add(player1)

for i in range(20):
    a = Tile("./tiles/grassHalfMid.png", 10+i*tileSize[0], 348)
    tile_group.add(a)

for i in range(10):
    a = Tile("./tiles/grassHalfMid.png", 100+i*tileSize[0], 280)
    tile_group.add(a)

for i in range(10):
    a = Tile("./tiles/grassHalfMid.png", 320+i*tileSize[0], 320)
    tile_group.add(a)

def tile(posList):
    a = 0

while True:
    clock.tick_busy_loop(FPS)

    window.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()

        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:'''

    player_group.update()
    player_group.draw(window)

    tile_group.update()
    tile_group.draw(window)

    pygame.display.flip()
