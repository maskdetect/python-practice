class Person:
    def __init__(self,name):
        self.name = name
        self.power = 100
        print(f"{self.name}默认体力：100(体力不可以为负值）")
    def eat(self):
        self.power += 20
        print(f"{self.name}吃饭恢复体力20,当前体力值为{self.power}")
    def sleep(self):
        self.power += 50
        print(f"{self.name}睡觉恢复体力50,当前体力值为{self.power}")
    def study(self):
        if self.power >= 30:
            self.power -= 30
            print(f"{self.name}学习消耗体力30,当前体力值为{self.power}")
        else:
            print(f"{self.name}当前体力值为{self.power}，不足30，无法学习")
    def training(self):
        if self.power >= 25:
            self.power -= 25
            print(f"{self.name}练习消耗体力25,当前体力值为{self.power}")
        else:
            print(f"{self.name}当前体力值为{self.power}，不足25，无法练习")

Wang = Person('小王')
Wang.eat()
Wang.study()
Wang.training()
Wang.study()
Wang.study()
Wang.study()
Wang.training()
Wang.sleep()
print()

Li = Person('小李')
Li.sleep()
Li.eat()
Li.training()