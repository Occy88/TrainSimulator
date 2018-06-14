class Mouse:
    def __init__(self):
        self.releasedL = True
        self.releasedR = True
        self.releasedM = True

    def pressL(self):
        self.releasedL = False

    def pressR(self):
        self.releasedR = False

    def pressM(self):
        self.releasedM = False

    def releaseL(self):
        self.releasedL = True

    def releaseR(self):
        self.releasedR = True

    def releaseM(self):
        self.releasedM = True
