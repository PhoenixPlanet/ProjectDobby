def add(a, b):
    return a + b


class Monster(object):
    def __init__(self, atk=10, defend=10, hp=25):
        self.atk = atk
        self.defend = defend
        self.hp = hp

    def Attack(self, enemy):
        if enemy.defend < self.atk:
            enemy.hp -= self.atk - enemy.defend

        if enemy.hp < 0:
            enemy.hp = 0
            print("Dead!")


class Dragon(Monster):
    def __init__(self, atk, defend, hp, sp):
        super().__init__(atk, defend, hp)
        self.sp = sp

    def FireAttack(self, enemy):
        if self.sp >= 10:
            self.sp -= 10
            enemy.hp -= 10
            if enemy.hp <= 0:
                enemy.hp = 0
                print("Burn...")
        else:
            print("Not enough energy")


monster1 = Monster()
monster2 = Monster()
transparentDragon = Dragon(100, 80, 500, 15)

transparentDragon.FireAttack(monster1)
transparentDragon.FireAttack(monster2)
transparentDragon.Attack(monster2)