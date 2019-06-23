from . import etcFuntions
import data
import pygame
from SpriteClass import tiles, players, itemSprites, guideSprites


class GameData:
    def __init__(self):
        # 게임 흐름
        self.gameState = data.gameStateList["lobby"]
        self.stageNum = 0

        self.stageTileImageList = []
        self.stageBackgroundImageList = []
        f = open("./UserFile/Stage/stageNum.txt", "r")
        self.maxStageNum = int(f.readline())
        f.close()
        for i in range(self.maxStageNum):
            self.stageTileImageList.append("./UserFile/Stage/tile" + str(i + 1) + ".png")
            self.stageBackgroundImageList.append("./UserFile/Stage/background" + str(i + 1) + ".png")
        self.goNext = True
        self.isClicked = 0
        # self.ticksForAll = 0
        self.storyLine = 0

        self.backgroundPos = [0, 0]
        self.ticksForStageChange = 0
        self.backgroundPreImage = 0
        self.backgroundNewImage = 0
        self.tilePreImage = 0
        self.tileNewImage = 0
        self.backgroundDX = 0
        self.playerDxForChangeStage = 0
        self.playerPosForChangeStage = []
        self.background = etcFuntions.image_load(self.stageBackgroundImageList[0], data.screen)

    def init_item(self, window):
        item_file = open("./UserFile/Stage/item" + str(self.stageNum + 1) + ".txt", "r")
        item_list = item_file.read().split("\n")
        self.item_groups = ItemGroups(item_list, window)
        item_file.close()

    def init_sprite_groups(self, sprite_groups):
        self.sprite_groups = sprite_groups

    def init_stage(self, sprite_groups, goNext, window):
        self.gameState = data.gameStateList["changeStage"]

        self.ticksForStageChange = 0
        self.backgroundPos = [0, 0]
        self.goNext = goNext
        if goNext:
            self.stageNum += 1
        else:
            self.stageNum -= 1

        item_file = open("./UserFile/Stage/item" + str(self.stageNum + 1) + ".txt", "r")
        item_list = item_file.read().split("\n")
        print(item_list)
        self.item_groups = ItemGroups(item_list, window)
        item_file.close()

        self.playerPosForChangeStage = [sprite_groups.player.x, sprite_groups.player.y]
        self.backgroundPreImage = self.background
        self.backgroundNewImage = etcFuntions.image_load(self.stageBackgroundImageList[self.stageNum], data.screen)
        self.tilePreImage = sprite_groups.t_tile.image
        self.tileNewImage = etcFuntions.image_load(self.stageTileImageList[self.stageNum], data.screen)

    def get_recent_stage_images(self):
        return self.stageBackgroundImageList[self.stageNum], self.stageTileImageList[self.stageNum]

    def get_game_data(self):
        return self


gameFlowData = GameData()


class SpriteGroups:
    t_tile: tiles.Tile
    player: players.Player

    def __init__(self):
        self.tile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.Group()
        self.guide_group = pygame.sprite.Group()

        self.player = 0
        self.t_tile = 0

    def add_tile(self, path, x, y):
        self.t_tile = tiles.Tile(path, x, y)
        self.tile_group.add(self.t_tile)

    def kill_tile(self):
        self.t_tile.kill()

    def init_player(self, x, y):
        self.player_group.empty()
        self.player = players.Player(x, y, self.t_tile)
        self.player_group.add(self.player)

    def init_enemy(self, enemyData):
        self.enemy_group.empty()
        #for e in enemyData:


    def update_sprites(self, window):
        self.tile_group.update()
        self.tile_group.draw(window)
        #window.blit(self.t_tile.image, (self.t_tile.x, self.t_tile.y))

        self.player_group.update()
        self.player_group.draw(window)

        self.enemy_group.update()
        self.enemy_group.draw(window)


class ItemGroups:
    def __init__(self, itemList, window):
        self.item_group = pygame.sprite.Group()
        self.window = window

        self.itemList = itemList
        for i in itemList:
            if not i == "":
                self.item_group.add(itemSprites.Item(i.split(), self.window))

    def update_item(self):
        self.item_group.update()
        self.item_group.draw(self.window)

