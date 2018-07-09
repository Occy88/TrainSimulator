from io import BytesIO
from PIL import Image
from urllib import request
import os
from pathlib import Path
import time
import threading
from SimpleGUICS2Pygame import simpleguics2pygame
from Classes.Middle.SpriteControl.SpriteAnimator import SpriteAnimator
from Classes.Base.Vector import Vector
from Classes.Super.MapTile import MapTile
from SimpleGUICS2Pygame import simpleguics2pygame
from Classes.Functions.Geometry import getMetersPerPixelGoogleImage,getMetersPerPixelsCam,getLatLongFromCoordinates
import matplotlib.pyplot as plt # this is if you want to plot the map using pyplot
import math

class MapLoader():
    def __init__(self,zoom):
        self.zoom=zoom
        self.delay=2
        self.currentTime=time.time()
        self.tile_dict={}
        self.cwd=os.getcwd()
        self.loadingKeys={}

    def updateTime(self):
        self.delay-=time.time()-self.currentTime

    def update(self,baseNode,cam,sprite_dict):

        if self.delay<=0:
            self.generatePoints(cam,sprite_dict,baseNode)

            self.delay=2


        else:
            self.updateTime()
        self.currentTime=time.time()
    def generatePoints(self,cam,sprite_dict,baseNode):
        self.updateZoomDistance(cam,baseNode)
        mpp=512 #size of image

        scaleFactor=self.getImageScaleFactor(self.zoom, getLatLongFromCoordinates(baseNode,cam.origin)[0])
        mpp*=scaleFactor
        key_dict={}
        remove_dict={}
        for x in range(int((cam.origin.getX()-cam.dim.getX())//mpp),int(((cam.origin.getX()+cam.dim.getX())//mpp)+1)):
            for y in range(int((cam.origin.getY()-cam.dim.getY())//mpp),int(((cam.origin.getY()+cam.dim.getY())//mpp)+1)):
                key=self.constructKey(x,y,self.zoom)
                directory=self.cwd+'/img/Map/'+key+'.png'
                if not key in sprite_dict:
                    point = getLatLongFromCoordinates(baseNode, Vector(x * mpp, y * mpp))
                    url = self.getUrl(point[0], point[1], self.zoom)
                    path=Path(directory)
                    image=0
                    if path.is_file():

                        image=simpleguics2pygame._load_local_image(directory)


                    elif not key in self.loadingKeys:
                        imgThread=threading.Thread(target=self.loadImage,args=(url,directory))
                        imgThread.start()
                        self.loadingKeys.update({key:key})


                    # if image in file load from file else load from simpleguics2 as bellow
                    # else load image from url and save to directory

                    if image != 0:
                        tile = SpriteAnimator(image, scaleFactor)
                        radius=256*scaleFactor
                        sprite_dict.update({key: tile})

                        mapTile = MapTile(Vector(x*mpp,y*mpp),self.zoom,key,sprite_dict,radius)
                        self.tile_dict.update({key: mapTile})

                elif key not in self.tile_dict:
                    radius = 256 * scaleFactor
                    mapTile = MapTile(Vector(x * mpp, y * mpp), self.zoom, key, sprite_dict,radius)
                    self.tile_dict.update({key:mapTile})
                key_dict.update({key:key})

        for key in self.tile_dict:
            if key not in key_dict:
                remove_dict.update({key:key})
        for key in remove_dict:
            self.tile_dict.pop(key)


    def loadImage(self,url,directory):
        with request.urlopen(url) as uRL:
            f = BytesIO(uRL.read())
        img = Image.open(f)
        img.save(directory)


    def draw(self,canvas,cam):
        a=0
        for key in self.tile_dict:
            a+=1
            tile=self.tile_dict[key]
            tile.draw(canvas,cam)
    def updateZoomDistance(self,cam,baseNode):
        zoom=20
        for i in range(0,19):
            j=20-i
            if getMetersPerPixelGoogleImage(getLatLongFromCoordinates(baseNode,cam.origin)[0],j)>getMetersPerPixelsCam(cam):
                break
            else:
                zoom=j
        self.zoom=zoom-1

    def constructKey(self,lat,long,zoom):
        lat=str(lat)
        long=str(long)
        zoom=str(zoom)
        key=lat+long+zoom
        return key

    def getUrl(self,lat,long,zoom):
        lat=round(lat,6)
        long=round(long,6)
        lat=str(lat)
        long=str(long)
        zoom=str(zoom)
        p1='http://maps.googleapis.com/maps/api/staticmap?center='
        p1= p1+lat+','+long+'&size=512x512&zoom='+zoom+'&format=png&maptype=roadmap&style=element:geometry%7Ccolor:0xebe3cd&style=element:labels.text.fill%7Ccolor:0x523735&style=element:labels.text.stroke%7Ccolor:0xf5f1e6&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0xc9b2a6&style=feature:administrative.land_parcel%7Celement:geometry.stroke%7Ccolor:0xdcd2be&style=feature:administrative.land_parcel%7Celement:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Celement:labels.text.fill%7Ccolor:0xae9e90&style=feature:landscape.natural%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:poi%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:poi%7Celement:labels%7Cvisibility:off&style=feature:poi%7Celement:labels.text%7Ccolor:0x6b4e00%7Cvisibility:on&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x93817c%7Cvisibility:off&style=feature:poi.park%7Celement:geometry.fill%7Ccolor:0xa5b076&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x447530&style=feature:road%7Celement:geometry%7Ccolor:0xf5f1e6&style=feature:road.arterial%7Cvisibility:off&style=feature:road.arterial%7Celement:geometry%7Ccolor:0xfdfcf8&style=feature:road.highway%7Celement:geometry%7Ccolor:0xf8c967&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0xe9bc62&style=feature:road.highway%7Celement:labels%7Cvisibility:off&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0xe98d58&style=feature:road.highway.controlled_access%7Celement:geometry.stroke%7Ccolor:0xdb8555&style=feature:road.local%7Cvisibility:off&style=feature:road.local%7Celement:labels%7Cvisibility:off&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x806b63&style=feature:transit.line%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:transit.line%7Celement:geometry.fill%7Ccolor:0x000000%7Csaturation:-100%7Clightness:-100%7Cweight:0.5&style=feature:transit.line%7Celement:labels.text%7Cvisibility:on&style=feature:transit.line%7Celement:labels.text.fill%7Ccolor:0x8f7d77&style=feature:transit.line%7Celement:labels.text.stroke%7Ccolor:0xebe3cd&style=feature:transit.station%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:transit.station.rail%7Celement:geometry.fill%7Csaturation:-100&style=feature:water%7Celement:geometry.fill%7Ccolor:0xb9d3c2&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x92998d&'+'sensor=false'
        p1=p1+'&key=AIzaSyCPw8pNEVEb7g3jQPj2w4EeaTidz-4qJ-E'
        return p1
    def getImageScaleFactor(self,zoom,lat):

        m2=getMetersPerPixelGoogleImage(lat,zoom)

        return m2

