import time, configparser
from Classes.Functions import Line as line
from Classes.Functions.Collisions.Collisions import doCirclesIntersect
from Classes.Middle.Particle import Particle
from Classes.Base.Vector import Vector

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))


class MapTile:
    def __init__(self, pos, zoom, sprite_key, sprite_dictionary, radius):
        self.zoom = zoom
        self.particle = Particle(False, pos, Vector(0, 0), radius, 0, sprite_key, sprite_dictionary, 0.01, False, False,
                                 1, 1, 1, 1, 1, 1, 1)

    def draw(self, canvas, cam):
        self.particle.draw(canvas, cam)
