class Person:
    def __init__(self,name):
        self.power = 100
        self.name = name
        print("%s的初始体力值为%d" % (self.name,self.power))

    def eat(self):
        self.power += 20
        print("%s吃饭，体力值增加20，当前体力值为%d" % (self.name,self.power))

    def sleep(self):
        self.power += 50
        print("%s睡觉，体力值增加50，当前体力值为%d" %  (self.name,self.power))

    def study(self):
        if (self.power >= 30):
            self.power -= 30
            print("%s学习，体力值减少30，当前体力值为%d" % (self.name, self.power))
        else:
            print("体力值不足30，体力值不可以为负值,学习失败")
        
    def training(self):
        if (self.power >= 25):
            self.power -= 25
            print("%s训练，体力值减少25，当前体力值为%d" % (self.name,self.power))
        else:
            print("体力值不足25，体力值不可以为负值,训练失败")


lmf = Person("lmf")
hxy = Person("hxy")
fmk = Person("fmk")


fmk.eat()
fmk.study()
fmk.sleep()
fmk.study()
fmk.study()
fmk.training()
fmk.study()
fmk.study()
fmk.training()
print()

lmf.eat()
lmf.training()
lmf.sleep()
lmf.study()
print()

hxy.eat()
hxy.sleep()
print()


