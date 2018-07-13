#from Classes.Settings import *
from Classes.Functions.Geometry import *
from Classes.Base.Vector import Vector

from SimpleGUICS2Pygame import simpleguics2pygame

from Classes.Super.Camera import Camera
from Handlers.Mouse import Mouse

from Classes.Middle.SpriteControl.SpriteAnimator import SpriteAnimator
from Classes.Functions import Line as line
from Classes.Functions.MapLoader import MapLoader
from GameStates.GameStates import GameState
import configparser
from Classes.Super.Train import Train
config = configparser.ConfigParser()
# Open file as writeable
config.read_file(open('Classes/config'))
import json
import os
import uuid
import math
import re

#// TO DO
#temp browers, website scraping

# ------------GAME STATES----------------
if('True' == config['CANVAS']['game_state']):
     gameState1 = GameState(True, False)
     gameState2 = GameState(True, False)
else:
     gameState1 = GameState(True, True)
     gameState2 = GameState(True, True)

# ---------------------ANY SETS/LISTS-----------------------
player_list = []



visual_set = set()
visual_set_external=set()
weapon_set = set()
weapon_set_external = set()
image_set=set()
env_l1_set = set()
env_l2_list=[]
env_l3_list=[]
send_list=[]
weighted_graph_dict={}
node_dict={}
way_dict={}
relation_dict={}
line_dict={} #line_name : node_list
train_dict={}
nodeTraffic_dict={}

node_draw_list=[]
relationPoint_list=[]

monster_set = set()
monster_set_external = set()

variables={'simulation_speed':1}

simTime=0
# MOUSE HANDLER (PYGAME)(NO RIGHT/MIDDLE CLICKS ON SIMPLEGUI)
mouse = Mouse()
# CONVERSION OF SIMPLE GUI MOUSE LOCATION TO PYGAME LOCATION
adjustment = Vector(250, 25)

# quick functions for testing to be cleaned up
def getUid():
    return str(uuid.uuid4())



# ------------------ DICTIONARY OF ALL PICTURES LOCATIONS-----------------
cwd = os.getcwd()
link=cwd + '/img/splash.jpg'
splash = simpleguics2pygame.load_image(link)
link=cwd + '/img/story.jpg'

story = simpleguics2pygame.load_image(link)

spriteDictionary = {}

# -----------------------MOVING OBJECTS-------------------
# CAMERA
cam = Camera(Vector(0,0), Vector(int(config['CANVAS']['CANVAS_WIDTH'])*4,int(config['CANVAS']['CANVAS_HEIGHT'])*4))

# PLAYERWrotham Heath Golf Club, Seven Mile Ln, Borough Green, Wrotham Heath, Sevenoaks TN15 8QZ

# -----------------------NON-MOVING OBJECTS------------------
# randomGrass()
# randomTrees()

#----------------   LOADING DATA FOR NODES----------------------------
file = open(cwd+"/img/Data/data.txt",'r', encoding='utf-8')
text=file.read()
data=json.loads(text)

foundBase=False

const= math.pi*6371000/180
for element in data['elements']:
    if element['type']=='node':
        if not foundBase:
            baseNode=element

            element.update({'x':0})
            element.update({'y':0})
            node_dict.update({element['id']:element})

            foundBase=True
        else:

            angle=angleFromCoordinate(baseNode['lat'],baseNode['lon'],element['lat'],element['lon'])

            distance=getDistance(baseNode['lat'],baseNode['lon'],element['lat'],element['lon'])
            x=distance*math.sin(angle)
            y=distance*math.cos(angle)
            element.update({'x': x})
            element.update({'y': -y})


            node_dict.update({element['id']: element})

    elif element['type']=='way':
        way_dict.update({element['id']: element})

    elif element['type']=='relation':
        relation_dict.update({element['id']: element})


#update with station names



#   ================= GENERATE A DICTIONARY CONTAINING ALL LINES/PATHS ===========

for elements in relation_dict:
    relation=relation_dict[elements]
    tags=relation['tags']
    if 'name' in tags:

        line_dict.update({tags['name']:line.getWayListFromLineName(relation_dict,tags['name'])})

#now that we have ll the lines by name, update their corresponding nodes with the relevant data
#first update all nodes with a specific maxVel and delay of 0 as there is a lack of data
for nodeId in node_dict:
    node= node_dict[nodeId]
    node.update({'maxVel':20})
    node.update({'delay':0})
all_stops_dict={}
#now find all the stops and change the delay to say 30 sec (new york minimum) and max vel 0 (assume trains stop at all stops?
for relationId in relation_dict:
    relation=relation_dict[relationId]
    members=relation['members']
    for elements in members:
        dic={}
        if elements['type']=='node':

            nodeTraffic_dict.update({elements['ref']:dic})
            node=node_dict[elements['ref']]
            node['maxVel']=20
            node['delay']=10
            if not elements['ref'] in all_stops_dict:
                all_stops_dict.update({elements['ref']:node_dict[elements['ref']]})

for stopId in all_stops_dict:
    stop=node_dict[stopId]
    shortestDistance=1000000
    stationName='defaultName'
    for element in data['elements']:

        if 'tags' in element:
            if 'station' in element['tags']: #this is the serch for station nodes
                if element['type']== 'node':
                    distance=Vector(element['x'],element['y']).distanceTo(Vector(stop['x'],stop['y']))
                    if distance<shortestDistance:
                        shortestDistance=distance
                        tags=element['tags']
                        stationName=tags['name']
                        stationName = stationName.split(' (')[0]
                elif element['type']=='way':
                    nodes= element['nodes']
                    nodeId=nodes[0]
                    node=node_dict[nodeId]
                    distance = Vector(node['x'], node['y']).distanceTo(Vector(stop['x'], stop['y']))
                    if distance < shortestDistance:
                        shortestDistance = distance
                        tags = element['tags']
                        stationName = tags['name']
                        stationName = stationName.split(' (')[0]
                elif element['type']=='relation':

                    tags=element['tags']
                    if 'name' in tags and 'railway' in tags:
                        if tags['railway']== 'station':

                            members=element['members']
                            wayTags=members[0]
                            way=way_dict[wayTags['ref']]
                            nodes=way['nodes']
                            nodeId = nodes[0]
                            node = node_dict[nodeId]
                            distance = Vector(node['x'], node['y']).distanceTo(Vector(stop['x'], stop['y']))
                            if distance < shortestDistance:
                                shortestDistance = distance
                                stationName = tags['name']
                                stationName=stationName.split(' (')[0]

    stop.update({'name':stationName})

for stopId in all_stops_dict:
    stop=all_stops_dict[stopId]
    stop.update({'train':{}})
    send_list.append(stop)




#==================ATTEMPT AT FINDING PAIR FROM LINE NAME=============
#node_corrections:
node=node_dict[5473272644]
node['name']='Bank'
node=node_dict[5473272645]
node['name']='Bank'

#===============constructing wighted graph ================
for stationId in all_stops_dict:
    station=all_stops_dict[stationId]
    if not station['name'] in weighted_graph_dict:
        weighted_graph_dict.update({station['name']:{}})
from Classes.Functions.Line import getStopListFromLineName
line_dict_names={}
for lineId in line_dict:
    stations=getStopListFromLineName(relation_dict,way_dict,lineId)
    name_dict={}
    for id in stations:
        station=all_stops_dict[id]
        name_dict.update({station['name']:(station['x'],station['y'])})
    line_dict_names.update({lineId:name_dict})

for name in weighted_graph_dict:
    for listId in line_dict_names:
        dict=line_dict_names[listId]
        if name in dict:
            for stopName in dict:
                pos1=dict[name]
                pos2=dict[stopName]
                pos1=Vector(pos1[0],pos1[1])
                pos2 = Vector(pos2[0], pos2[1])
                weight=pos1.distanceTo(pos2)
                wgStops=weighted_graph_dict[name]
                if not stopName in wgStops:
                    wgStops.update({stopName:weight})



none_connected_stop_list=[]
for stopName in weighted_graph_dict:
    if len((weighted_graph_dict[stopName]))<1:
        none_connected_stop_list.append(stopName)
for name in none_connected_stop_list:
    weighted_graph_dict.pop(name)
#add a drawn element into the every way to avoid being drawn twice.
for wayId in way_dict:
    way=way_dict[wayId]

    way.update({'drawn':False})

mapLoader=MapLoader(14)
from Classes.Functions.TrainLoader import TrainLoader
from Classes.Functions.AutoCam import AutoCam
trainLoader=TrainLoader()
autoCam=AutoCam()
#-------------  LOADING DATA FOR WAYS ------------------------------

# tree = Particle(True, Vector(2500, 2500), Vector(0, 0), 0, Vector(2500, 2500), 200, 0, 0, 0, 'en_l1_tr', spriteDictionary,
#                 1, False, False, getUid(), 4, 15, 1, 1, 4, 15)
#

# # -----------------------SOUNDS------------------
# sound_bg_1 = simpleguics2pygame._load_local_sou24491112nd(cwd + '/sound/bg1.wav')
# sound_bg_1.set_volume(0.1)
# sound_bg_2 = simpleguics2pygame._load_local_sound(cwd + '/sound/bg2.wav')
# sound_bg_2.set_volume(0.1)
# sound_bg_3 = simpleguics2pygame._load_local_sound(cwd + '/sound/bg3.wav')
# sound_bg_3.set_volume(0.1)
# sound_bg_4 = simpleguics2pygame._load_local_sound(cwd + '/sound/bg4.wav')
# sound_bg_4.set_volume(0.1)
#
# sound_dict = {
#      "bg_1":sound_bg_1,
#      "bg_2":sound_bg_2,
#      "bg_3":sound_bg_3,
#      "bg_4":sound_bg_4}
#
# sound_manager = SoundManager(sound_dict)
