import data
from etc import etcFuntions


def change_stage(window, gameData, spriteGroups, itemgroups):
    window.fill(data.SEMI_SKY)

    t = gameData.ticksForStageChange

    if gameData.goNext:
        a = ((6 * 720) / (data.changeStageSpeed ** 3))
        b = ((6 * 639) / (data.changeStageSpeed ** 3))
    else:
        a = ((-6 * 720) / (data.changeStageSpeed ** 3))
        b = ((-6 * 639) / (data.changeStageSpeed ** 3))

    backgroundDX = a * ((t ** 2) - (data.changeStageSpeed * t))
    gameData.backgroundPos[0] += backgroundDX
    for i in itemgroups.item_group:
        i.x += backgroundDX

    if gameData.goNext:
        newX = gameData.backgroundPos[0] + data.screen[0]
    else:
        newX = gameData.backgroundPos[0] - data.screen[0]

    window.blit(gameData.backgroundPreImage, gameData.backgroundPos)
    window.blit(gameData.backgroundNewImage, (newX, gameData.backgroundPos[1]))
    window.blit(gameData.tilePreImage, gameData.backgroundPos)
    window.blit(gameData.tileNewImage, (newX, gameData.backgroundPos[1]))

    playerDxForChangeStage = b * ((t ** 2) - (data.changeStageSpeed * t))
    gameData.playerPosForChangeStage[0] += playerDxForChangeStage
    spriteGroups.player.pos(gameData.playerPosForChangeStage)
    spriteGroups.player_group.draw(window)

    if t == data.changeStageSpeed:
        new_background, new_tile = gameData.get_recent_stage_images()
        gameData.background = etcFuntions.image_load(new_background, data.screen)
        gameData.gameState = data.gameStateList["normal"]
        spriteGroups.kill_tile()
        spriteGroups.add_tile(new_tile, 0, 0)
        spriteGroups.player.t_tile = spriteGroups.t_tile
        gameData.backgroundPos = (0, 0)

    gameData.ticksForStageChange += 1