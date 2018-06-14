#from Classes.Settings import *
from Classes.Functions.Geometry import angleFromCoordinate, getDistance
from Classes.Base.Vector import Vector

from SimpleGUICS2Pygame import simpleguics2pygame

from Classes.Super.Camera import Camera
from Handlers.Mouse import Mouse

from Classes.Middle.SpriteControl.SpriteAnimator import SpriteAnimator
from Classes.Functions import Line as line
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

env_l1_set = set()
env_l2_list=[]
env_l3_list=[]


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

# MOUSE HANDLER (PYGAME)(NO RIGHT/MIDDLE CLICKS ON SIMPLEGUI)
mouse = Mouse()
# CONVERSION OF SIMPLE GUI MOUSE LOCATION TO PYGAME LOCATION
adjustment = Vector(250, 25)

# quick functions for testing to be cleaned up
def getUid():
    return str(uuid.uuid4())



# ------------------ DICTIONARY OF ALL PICTURES LOCATIONS-----------------
print('LOADING ASSETS')
cwd = os.getcwd()
link=cwd + '/img/splash.jpg'
splash = simpleguics2pygame.load_image(link)
link=cwd + '/img/story.jpg'

story = simpleguics2pygame.load_image(link)
print(story.get_height())
print(splash.get_width())
ch1 = SpriteAnimator(cwd + '/img/Character/1.jpg')
ch2 = SpriteAnimator(cwd + '/img/Character/2.jpg')

spriteDictionary = {'ch_1': ch1,
                    'ch_2': ch2,}

# -----------------------MOVING OBJECTS-------------------
print("ASSETS LOADED")
print("LOADING OBJECTS")
# CAMERA
cam = Camera(Vector(0,0), Vector(int(config['CANVAS']['CANVAS_WIDTH'])*4,int(config['CANVAS']['CANVAS_HEIGHT'])*4))

# PLAYER

# -----------------------NON-MOVING OBJECTS------------------
print("OBJECTS LOADED")
print("GENERATING RANDOM ENVIRONMENT")
# randomGrass()
# randomTrees()
print("ENVIRONMENT GENERATED")

#----------------   LOADING DATA FOR NODES----------------------------
file = open(cwd+"/img/Data/data.json",'r')
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
            x=distance*math.sin(math.radians(angle))
            y=distance*math.cos(math.radians(angle))
            element.update({'x': x})
            element.update({'y': -y})
            node_dict.update({element['id']: element})

    elif element['type']=='way':
        way_dict.update({element['id']: element})

    elif element['type']=='relation':
        relation_dict.update({element['id']: element})
    else:
        print(element['type'])


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
    node.update({'maxVel':1000})
    node.update({'delay':0})
all_stops=[]
#now find all the stops and change the delay to say 30 sec (new york minimum) and max vel 0 (assume trains stop at all stops?
for relationId in relation_dict:
    relation=relation_dict[relationId]
    members=relation['members']
    for elements in members:
        dic={}
        if elements['type']=='node':
            if elements['role']=='stop':
                nodeTraffic_dict.update({elements['ref']:dic})
                node=node_dict[elements['ref']]
                node['maxVel']=0
                node['delay']=1

                all_stops.append(node['id'])


#==============load train example=====================
testLine1='Northern Line: Edgware → Charing Cross → Kennington'
testLine2='Northern Line: Kennington → Charing Cross → Edgware'

train=Train(30,2,testLine1,testLine2,relation_dict,line_dict,way_dict,node_dict,0,5,'',spriteDictionary,0.01,getUid(),1,1,1,1,1,1)
train_dict.update({train.idObject:train})
train=Train(30,2,testLine1,testLine2,relation_dict,line_dict,way_dict,node_dict,0,5,'',spriteDictionary,0.01,getUid(),1,1,1,1,1,1)
train_dict.update({train.idObject:train})
for name in line_dict:
    print(name)
#==================ATTEMPT AT FINDING PAIR FROM LINE NAME=============


#add a drawn element into the every way to avoid being drawn twice.
for wayId in way_dict:
    way=way_dict[wayId]

    way.update({'drawn':False})


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
