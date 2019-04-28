import pygame
import sys

pygame.init()

# 게임 화면 설정
screen = (720, 480)
window = pygame.display.set_mode(screen)
pygame.display.set_caption("Project Dumbledore")
# 게임 아이콘: 나중에 변경할 것
# pygame.display.set_icon()

# FPS
clock = pygame.time.Clock()
FPS = 60

# 색깔들
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def image_load(path):
    image = pygame.image.load(path)
    rect = image.get_rect()

    return image, rect


# 스프라이트 클래스
class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__(self)
        self.image, self.rect = image_load(image_path)
        self.pos = self.rect.move(x, y)
        self.x, self.y = x, y

    def set_pos(self, x, y):
        self.pos = self.pos.move(x, y)
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.set_pos(self.x + dx, self.y + dy)


# 스프라이트 그룹
tile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

print(sys.version)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()