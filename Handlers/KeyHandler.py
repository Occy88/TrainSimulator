from SimpleGUICS2Pygame import simpleguics2pygame
from Loading.Objects import gameState1

from Loading.Objects import cam,variables,autoCam

def keyup(key):
    if key == simpleguics2pygame.KEY_MAP['r']:
        cam.zoomOut = False
    elif key == simpleguics2pygame.KEY_MAP['e']:
        cam.zoomIn = False
    elif key == simpleguics2pygame.KEY_MAP['right']:
        cam.moveRight = False
    elif key == simpleguics2pygame.KEY_MAP['left']:
        cam.moveLeft = False
    elif key == simpleguics2pygame.KEY_MAP['up']:
        cam.moveUp = False
    elif key == simpleguics2pygame.KEY_MAP['down']:
        cam.moveDown = False
    elif key == simpleguics2pygame.KEY_MAP['a']:
        if autoCam.active:
            autoCam.active=False
        else:
            autoCam.active=True


def keydown(key):

    if key == simpleguics2pygame.KEY_MAP['r']:
        cam.zoomOut = True
    elif key == simpleguics2pygame.KEY_MAP['e']:
        cam.zoomIn = True

    elif key == simpleguics2pygame.KEY_MAP['right'] :
        cam.moveRight = True
    elif key == simpleguics2pygame.KEY_MAP['left']:
        cam.moveLeft = True
    elif key == simpleguics2pygame.KEY_MAP['up']:
        cam.moveUp = True
    elif key == simpleguics2pygame.KEY_MAP['down']:
        cam.moveDown = True
    elif key == simpleguics2pygame.KEY_MAP['1']:
        variables['simulation_speed']=1
    elif key == simpleguics2pygame.KEY_MAP['2']:
        variables['simulation_speed']=2
    elif key == simpleguics2pygame.KEY_MAP['3']:
        variables['simulation_speed']=4
    elif key == simpleguics2pygame.KEY_MAP['4']:
        variables['simulation_speed']=6
    elif key == simpleguics2pygame.KEY_MAP['5']:
        variables['simulation_speed']=8
    elif key == simpleguics2pygame.KEY_MAP['6']:
        variables['simulation_speed']=10
    elif key == simpleguics2pygame.KEY_MAP['7']:
        variables['simulation_speed']=20
    elif key == simpleguics2pygame.KEY_MAP['8']:
        variables['simulation_speed']=30
    elif key == simpleguics2pygame.KEY_MAP['9']:
        variables['simulation_speed']=40


