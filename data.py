# 게임 화면 설정(확인해본 결과 (1440, 960), (1280, 1080) 정도 되면 연산속도가 눈에 띌 정도로 느려짐)
screen = (720, 480)
mapEditorScreen = (720, 550)

# 캐릭터, 타일 크기 설정
playerSize = (30, 50)
basic_tileSize = (30, 30)

lifeBarSize = (20, 3)

dummyMargin = int(playerSize[0] / 4.7)
dummyPlayerSize = (playerSize[0] - dummyMargin*2, playerSize[1])
tileSize = screen

# FPS
FPS = 60

# 색깔들
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SEMI_SKY = (214, 255, 255)
GREY = (189, 189, 189)
SEMI_BLACK = (93, 93, 93)

# 플레이어 이동 속도, 애니메이션 프레임
pXVel = 2
animRate = 3
frameForAnim = 0

# y방향 가속도(중력 가속도로 작용)
pYAcc = 0.5  # (0.5px * 60^2 / s^2)

# 점프 세기
jumpF = -8

# 게임 흐름 상태 목록
gameStateList = {"lobby": 0, "normal": 1, "changeStage": 2}

# 스테이지 변경 속도 (단위: 프레임)
changeStageSpeed = 90


def loadGameData(stageNum):
    itemFile = open("./ItemContentLists/stage"+str(stageNum)+".txt", 'r')
    loadList = itemFile.read().split("\n")
    result = []
    for i in loadList:
        result.append(i.split())

