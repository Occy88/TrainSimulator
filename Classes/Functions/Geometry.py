import math
def angleFromCoordinate(lat1, lon1, lat2, lon2):
    la1 = math.radians(lat1)
    la2 = math.radians(lat2)

    y=math.sin(math.radians(lon2)-math.radians(lon1))*math.cos(la2)
    x=math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(math.radians(lon2)-math.radians(lon1))
    angle=math.atan2(y,x)
    angle=math.degrees(angle)

    return angle
def getDistance(lat1,lon1,lat2,lon2):
    R = 6371000
    la1 = math.radians(lat1)
    la2 = math.radians(lat2)
    dla = math.radians(lat2 - lat1)
    dlo = math.radians(lon2 - lon1)
    a = math.sin(dla / 2) * math.sin(dla / 2) + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    return d