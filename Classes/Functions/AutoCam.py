import math
import random
import time
from Classes.Base.Vector import Vector


class AutoCam():
    def __init__(self):
        self.active=True
        self.currentTime=time.time()
        self.delay=0
        self.train=Vector(0,0)
    def update(self,cam,train_dict):

        if self.active and len(train_dict)>0:

            if self.delay!=0:
                if self.delay<0:
                    self.delay=0
                if self.delay>0:

                    self.delay-=time.time()-self.currentTime
            else:
                self.getRandomTrainPosVector(train_dict)
                self.delay = 20
            cam.origin = self.train.particle.pos.copy()
            self.currentTime=time.time()
    def getRandomTrainPosVector(self,train_dict):
        if len(train_dict)>0:
            randKey=random.choice(list(train_dict))
            randTrain=train_dict[randKey]
            self.train=randTrain
