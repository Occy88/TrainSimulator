import time, configparser
from Classes.Base.Vector import Vector
from Classes.Middle.Particle import Particle

config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
import json
import random

# ==> json structure: elements --> relation (line, name (way (node) node))



    #here you # can count n number of trains e.t.c.
def draw(canvas,cam,way_dict,node_dict):
    for wayId in way_dict:
        convPoints = []
        way = way_dict[wayId]

        for nodes in way['nodes']:


            node = node_dict[nodes]
            nodeVect = nodeToVector(node)
            nodeVect.transformToCam(cam)
            convPoints.append((nodeVect.getX(), nodeVect.getY()))

        canvas.draw_polyline(convPoints, 1, random.choice(['red','green','blue']))

def nodeToVector(node):
    return Vector(node['x'],node['y'])

def drawNode(canvas,cam,node_dict,nodeId,color):
    node = node_dict[nodeId]
    nodeVect = nodeToVector(node)
    nodeVect.transformToCam(cam)
    radius = 8
    ratio = cam.ratioToCam()
    radius = radius * ratio.getX()
    canvas.draw_circle((nodeVect.getX(), nodeVect.getY()), radius, 10, color)


def drawNodeList(canvas,cam,node_dict,node_list):
    for nodeId in node_list:
        node = node_dict[nodeId]
        nodeVect = nodeToVector(node)
        nodeVect.transformToCam(cam)
        radius=5
        ratio = cam.ratioToCam()
        radius =radius * ratio.getX()
        canvas.draw_circle((nodeVect.getX(), nodeVect.getY()), radius, 10, 'White')

def drawByName(canvas,cam,line_dict,way_dict,node_dict,name,color):
    way_list= line_dict[name]
    for wayId in way_list:
        convPoints = []
        way=way_dict[wayId]

        for nodes in way['nodes']:


            node=node_dict[nodes]
            nodeVect=nodeToVector(node)
            nodeVect.transformToCam(cam)
            convPoints.append((nodeVect.getX(),nodeVect.getY()))

        canvas.draw_polyline(convPoints,1,color)

def getWayListFromLineName(relation_dict,name):
    way_list=[]
    for relationId in relation_dict:
        relation=relation_dict[relationId]
        if 'tags' in relation:
            if 'name' in relation['tags']:
                tags=relation['tags']
                if tags['name']==name:
                    members=relation['members']
                    for element in members:
                        if element['type']=='way' and element['role']=='':
                            way_list.append(element['ref'])
                    return way_list



def getStopListFromLineName(relation_dict,way_dic,name):

    nodeCheck_dic = {}
    wayIds = getWayListFromLineName(relation_dict, name)
    for wayId in wayIds:
        way = way_dic[wayId]
        for nodeId in way['nodes']:
            nodeCheck_dic.update({nodeId:nodeId})

    stop_list = []
    for relationId in relation_dict:
        relation=relation_dict[relationId]
        if 'tags' in relation:
            if 'name' in relation['tags']:
                tags=relation['tags']
                if tags['name']==name:
                    members = relation['members']
                    for element in members:
                        if element['type'] == 'node':
                            if element['ref'] in nodeCheck_dic:
                                stop_list.append(element['ref'])
                    #check stop_list for authenticity/ if all stop nodes are in the way lists

                    return stop_list

