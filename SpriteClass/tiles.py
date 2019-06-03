import pygame
from etc import etcFuntions
import data

# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = data.screen
tileSize = screen


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = etcFuntions.image_load(image_path, tileSize)
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
