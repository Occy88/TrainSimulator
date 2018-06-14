import pygame
from Loading.RandomGen import getRandomArrow,getRandomMagicWeapon,getRandomMagicCast,getRandomShowOff
from Classes.Base.Vector import Vector
from Loading.Objects import mouse,  player_list, cam, \
    adjustment, spriteDictionary,weapon_set,getUid,visual_set

from Classes.Middle.Particle import Particle
import configparser, time

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))


def checkClick():
    left, middle, right = pygame.mouse.get_pressed()

    # LEFT KEY
    if left and mouse.releasedL:
        mouse.pressL()

    elif left:
        pass
    elif not left and not mouse.releasedL:
        mouse.releaseL()

    # RIGHT KEY
    if right and mouse.releasedR:
        mouse.pressR()


    elif right:
        pass

    elif not right and not mouse.releasedR:

        mouse.releaseR()

    # MIDDLE KEY
    if middle and mouse.releasedM:
        mouse.pressM()
    elif middle:
        pass
    elif not middle and not mouse.releasedM:
        mouse.releaseM()
