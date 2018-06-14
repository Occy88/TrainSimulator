from Classes.Base.Vector import Vector
import math


def doCirclesIntersect(pos1,radius1, pos2,radius2):
    distance_points = (pos1.copy().subtract(pos2)).length()
    distance_radius = radius1 + radius2
    return (distance_points <= distance_radius)

def isCircleInRect(posC,radius,posR,dim):
    distX=posC.getX()-posR.getX()
    if distX<0:
        distX*=-1
    distY = posC.getY() - posR.getY()
    if distY < 0:
        distY*= -1
    if distY < radius + dim.getY() and distX<radius+dim.getX():
        return True
    return False

def isPointInRect(point,rectOrigin,rectDim):
    x=rectDim.copy().divide(2).getX()
    y = rectDim.copy().divide(2).getY()
    xIn=point.getX()>rectOrigin.getX()-x and point.getX()<rectOrigin.getX()+x
    yIn=point.getY()>rectOrigin.getY()-y and point.getY()<rectOrigin.getY()+y

    return xIn and yIn







        
