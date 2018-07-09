import math
from geopy.distance import VincentyDistance, distance,vincenty,geodesic
from Classes.Base.Vector import Vector
def angleFromCoordinate(lat1, lon1, lat2, lon2):
    la1 = math.radians(float(lat1))
    la2 = math.radians(float(lat2))

    y=math.sin(math.radians(lon2)-math.radians(lon1))*math.cos(la2)
    x=math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(math.radians(lon2)-math.radians(lon1))
    angle=math.atan2(y,x)


    return angle
def getDistance(lat1,lon1,lat2,lon2):
    c1 = (lat1, lon1)
    c2 = (lat2, lon2)
    d=geodesic(c1, c2).meters
    return d

def getPointFromBearingDistance(point,bearing,distance):
    bearing=math.degrees(float(bearing))
    c1 = point
    a = geodesic.destination(geodesic(),c1,bearing,distance/1000)
    return (a.latitude,a.longitude)

def getDistanceGeopy(lat1,lon1,lat2,lon2):
    c1=(lat1,lon1)
    c2=(lat2,lon2)
    return vincenty(c1,c2).meters

def getLatLongFromCoordinates(BaseNode,VectorPoint):
    angle=Vector(0,0).angleTo(VectorPoint)
    distance=Vector(0,0).distanceTo(VectorPoint)
    return getPointFromBearingDistance(BaseNode,math.radians(angle),distance)

def getMetersPerPixelGoogleImage(lat,zoom):
    return 156543.03392 * math.cos(lat* math.pi / 180) / math.pow(2, zoom)

def getMetersPerPixelsCam(cam):
    ca=cam.dim.getY()
    cv=cam.dimCanv.getY()
    ans=ca/cv

    return ans
    #dim cam is the pixels per meter of the