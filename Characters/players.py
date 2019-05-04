import pygame
from etc import etcFuntions
import data

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
frameForAnim = 0


class dummyPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.dy = 0
        self.dx = 0
        self.image = etcFuntions.image_load("./Player1/walking_dummy2.png", (w, h))
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
    def __init__(self, x, y, t_tile):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.t_tile = t_tile
        self.dy = 0
        self.dx = 0

        self.walk_image = []
        for i in range(1, 10):
            self.walk_image.append(
                etcFuntions.image_load("./Player1/alien_mint/p1_walk0" + str(i) + ".png", data.playerSize))
        self.walk_image.append(etcFuntions.image_load("./Player1/alien_mint/p1_walk10.png", data.playerSize))
        self.walk_image.append(etcFuntions.image_load("./Player1/alien_mint/p1_walk11.png", data.playerSize))

        self.rect = self.walk_image[0].get_rect()
        self.imageNum = 0
        self.image = self.walk_image[self.imageNum]
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.jumpState = 0

    def set_target_tile(self, t_tile):
        self.t_tile = t_tile

    def move(self, dx, dy, image=False):
        self.x += dx
        self.y += dy

        if image:
            if self.imageNum < 10:
                self.imageNum += 1
            else:
                self.imageNum = 0

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
        dummy = dummyPlayer(self.x + data.dummyMargin, self.y, data.dummyPlayerSize[0], data.dummyPlayerSize[1])
        dummy.move(dx, 0)
        # dummy_group.add(dummy)

        i = 0
        while True:
            if (not (pygame.sprite.collide_mask(dummy, self.t_tile))) or i > 7:
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
            self.move(self.dx, 0, frameForAnim == data.animRate)
            if pygame.sprite.collide_mask(dummy, self.t_tile):
                while pygame.sprite.collide_mask(dummy, self.t_tile):
                    if self.dx > 0:
                        self.x -= 0.1
                        self.rect.x = self.x
                    else:
                        self.x -= 0.1
                        self.rect.x = self.x

        # dummy_group.draw(window)

    # 중력 구현
    def check_ground(self):
        dummy = dummyPlayer(self.x+data.dummyMargin, self.y, data.dummyPlayerSize[0], data.dummyPlayerSize[1])

        if pygame.sprite.collide_mask(dummy, self.t_tile):
            if self.dy < 0:
                while pygame.sprite.collide_mask(dummy, self.t_tile):
                    dummy.move(0, 1)

                print(self.y)
                self.y = dummy.y
                print(self.y)
                self.dy = 0

            else:
                while pygame.sprite.collide_mask(dummy, self.t_tile):
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

        self.dy += data.pYAcc

        # 점프
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            if self.jumpState:
                self.y -= 1
                self.rect.y = self.y

                self.dy = data.jumpF
                self.jumpState = 0

        self.y += self.dy

        # 좌우 이동
        if key[pygame.K_RIGHT]:
            if self.direction == 1:
                self.direction = 0
            self.dx = data.pXVel
            self.x_check_move(self.dx)

        elif key[pygame.K_LEFT]:
            if self.direction == 0:
                self.direction = 1
            self.dx = -data.pXVel
            self.x_check_move(self.dx)

        else:
            self.imageNum = 8
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
        if frameForAnim == data.animRate:
            frameForAnim = 0

        frameForAnim += 1

        # 위치 지정 및 땅 감지
        self.rect.x, self.rect.y = self.x, self.y
        self.check_ground()