import time, configparser
from Classes.Middle.SpriteControl.SpriteSheet import SpriteSheet
from Classes.Base.Vector import Vector
from SimpleGUICS2Pygame import simplegui_lib_draw

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
import json


class Particle:

    def __init__(self, updateSprite, pos, vel, radius, angle, spriteKey, spriteDictionary, fps, removeOnVelocity0,
                 removeOnAnimationLoop, idObject, numRows, numColumns, startRow, startColumn, endRow, endColumn):

        self.idObject = idObject
        self.idClass = 2
        self.pos = pos
        self.vel = vel
        self.angle = angle
        self.updateSprite = updateSprite
        self.spriteKey = spriteKey

        if spriteKey != '':
            print('spriteKey: ',spriteKey)
            self.spriteSheet = SpriteSheet(spriteDictionary.get(self.spriteKey, 'elf_demo'), fps)

            self.spriteSheet.setRow(numRows, numColumns, startRow, startColumn, endRow, endColumn)
            self.dim = self.spriteSheet.animator.dimOriginal.copy().divideVector(
                Vector(self.spriteSheet.numColumns, self.spriteSheet.numRows))

        self.removeOnAnimationLoop = removeOnAnimationLoop
        self.removeOnVelocity0 = removeOnVelocity0

        self.radius = radius

        self.drawn = False
        if radius == 0:
            self.radius = self.dim.size() / 4

        self.currentTime = time.time()

    def draw(self, canvas, cam):

        distance = cam.origin.copy().subtract(self.pos)
        if distance.getX() < 0:
            distance.x *= -1
        if distance.getY() < 0:
            distance.y *= -1
        if self.spriteKey != '':
            distance.subtract(self.spriteSheet.animator.dimCamera.copy().multiply(2))

        if distance.getX() < cam.dim.getX() / 2 and distance.getY() < cam.dim.getY() / 2:
            # --------TESTING PURPOSES----DO NOT REMOVE-------------
            # cam.dim = Vector(2600*2, 1400*2)
            objectPos = self.pos.copy().transformToCam(cam)
            if self.spriteKey != '':
                self.spriteSheet.draw(canvas, cam, objectPos, self.angle)
            # 1cam.dim=Vector(1300,700)

            # DEVELOPER OPTION:

            ratio = cam.ratioToCam()
            radius = self.radius * ratio.getX()
            x, y = objectPos.getX(), objectPos.getY()
            # print(radius)
            if self.spriteKey != '':
                self.spriteSheet.draw(canvas, cam, objectPos, self.angle)
            # 1cam.dim=Vector(1300,700)

            # DEVELOPER OPTION:

            # draw nodes
            canvas.draw_circle((x, y), radius, 2, 'White')

    def updatePos(self):
        self.pos.add( self.vel.copy().multiply((time.time() - self.currentTime)*int(config['DEVELOPER']['SPEED_MULT'])))

    def update(self):
        if self.updateSprite and self.spriteKey != '':
            self.spriteSheet.update()

        self.updatePos()
        self.currentTime = time.time()
