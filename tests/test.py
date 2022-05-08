class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def getA(self):
        return self.a

    def getB(self):
        return self.b


o1 = Test(1,2)

print(o1.getA)