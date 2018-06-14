import time, configparser
from Classes.Functions import Line as line
from Classes.Functions.Collisions.Collisions import doCirclesIntersect
from Classes.Middle.Particle import Particle
from Classes.Base.Vector import Vector
config = configparser.ConfigParser()
config.read_file(open('Classes/config'))


class Train:
    def __init__(self, maxVel,maxAcceleration,lineName1,lineName2,relation_dict,line_dict,way_dict,node_dict, angle, radius, spriteKey, spriteDictionary, spriteFps,
                 idObject, numRows, numColumns, startRow, startColumn, endRow, endColumn):

        self.line1=lineName1
        self.line2=lineName2
        self.line1Bool=True

        self.way_list=line_dict[self.line1]#make sure this is a list of ways by id's
        wayId=self.way_list[0]
        way=way_dict[wayId]
        self.node_list=way['nodes']

        self.stop_list=line.getStopListFromLineName(relation_dict,way_dict,self.line1)

        self.traverseForward=True

        self.reachedEnd=False
        self.wayIndex=0
        self.nodeIndex=1
        self.stopIndex=0

        self.currentWay = self.way_list[self.wayIndex]
        self.currentStop=self.stop_list[self.stopIndex]
        self.nextStop=self.stop_list[self.stopIndex]
        self.currentNode=self.node_list[self.nodeIndex-1]
        self.nextNode=self.node_list[self.nodeIndex]
        nodeCurrent=node_dict[self.currentNode]
        nodeNext=node_dict[self.nextNode]
        self.acceleration=0
        self.maxVel=maxVel
        self.maxAcceleration = maxAcceleration

        vel = Vector(nodeNext['x'], nodeNext['y']).subtract(Vector(nodeCurrent['x'],nodeCurrent['y']))
        if vel.length() != 0:
            vel.normalize()

        self.directionVect=vel
        self.cooldown = nodeCurrent['delay']
        if self.maxVel == 50:
            self.cooldown=10

        self.currentTime=time.time()
        self.idObject=idObject
        self.particle = Particle(True,Vector(nodeCurrent['x'],nodeCurrent['y']), Vector(0,0), radius, angle,spriteKey,
                                 spriteDictionary, spriteFps,
                                 False, False, self.idObject, numRows, numColumns, startRow, startColumn, endRow,
                                 endColumn)

    def update(self,nodeTraffic_dict,train_dict,relation_dict,line_dict,way_dict,node_dict):
        if not self.reachedEnd:
            if self.cooldown>0:#wait for cooldown
                self.cooldown-= ((time.time()-self.currentTime)*int(config['DEVELOPER']['SPEED_MULT']))

            elif self.cooldown<0:
                self.cooldown=0
            else:
                self.updateVelocity(nodeTraffic_dict,train_dict,relation_dict,line_dict,way_dict,node_dict)
        else:
            self.particle.vel.multiply(0)

        self.particle.update()
        self.currentTime = time.time()

    def draw(self, canvas, cam,node_dict):

        self.particle.draw(canvas, cam)

    def incrementIndexes(self,way_dict):
        self.currentNode=self.nextNode
        if (self.nodeIndex<len(self.node_list)-1 and self.traverseForward) or (self.nodeIndex>0 and not self.traverseForward):#next node
            if self.traverseForward:
                self.nodeIndex+=1
            else:
                self.nodeIndex-=1
            self.nextNode=self.node_list[self.nodeIndex]
        elif (self.nodeIndex>=len(self.node_list)-1 and self.traverseForward) or (self.nodeIndex<=0 and not self.traverseForward):
            if self.wayIndex>=len(self.way_list)-1: #reached end
                self.reachedEnd=True
                self.nodeIndex=1
                self.wayIndex=0
            else:                       #next way
                self.wayIndex+=1
                self.nodeIndex=0
                self.currentWay=self.way_list[self.wayIndex]
                way=way_dict[self.currentWay]
                self.node_list=way['nodes']
                self.nextNode=self.node_list[self.nodeIndex]
                if self.currentNode==self.nextNode:
                    self.traverseForward=True
                else:
                    self.traverseForward=False
                    self.nodeIndex=len(self.node_list)-1
                    self.nextNode=self.node_list[self.nodeIndex]
    def getNodeFromId(self,node_dict,nodeId):
        return node_dict[nodeId]
    def getPosVectorFromNode(self, node_dict,nodeId):
        node=node_dict[nodeId]
        return Vector(node['x'],node['y'])

    def checkIfReachedNode(self,way_dict,node_dict):
        if self.particle.vel.getX() != 0 or self.particle.vel.getY() != 0:
            if self.particle.vel.copy().dot(self.getPosVectorFromNode(node_dict,self.nextNode).subtract( self.particle.pos)) < 0 :
                # if traveling away from node and close to it (reached it)

                # if doCirclesIntersect(self.particle.pos,2,self.getPosVectorFromNode(node_dict,self.nextNode),2):
                self.incrementIndexes(way_dict)

                self.cooldown=node_dict[self.currentNode]['delay']

                vel=self.getPosVectorFromNode(node_dict,self.nextNode).subtract(self.getPosVectorFromNode(node_dict,self.currentNode))
                if vel.length()!=0:
                    vel.normalize()
                    self.directionVect=vel.copy()
                    vel.multiply(self.particle.vel.length())


                    self.particle.vel=vel.copy()
                    self.particle.pos=self.getPosVectorFromNode(node_dict,self.currentNode)
        elif self.particle.pos == self.getPosVectorFromNode(node_dict,self.nextNode):
            self.incrementIndexes(way_dict)

            self.cooldown = node_dict[self.currentNode]['delay']

            vel = self.getPosVectorFromNode(node_dict, self.nextNode).subtract(
                self.getPosVectorFromNode(node_dict, self.currentNode))
            if vel.length() != 0:
                vel.normalize()
                self.directionVect = vel.copy()
                vel.multiply(self.particle.vel.length())

                self.particle.vel = vel.copy()
                self.particle.pos = self.getPosVectorFromNode(node_dict, self.currentNode)

    def checkDecelForStop(self,node_dict):
        nextStop = node_dict[self.nextStop]
        distanceToStop = self.particle.pos.copy().distanceTo(Vector(nextStop['x'], nextStop['y']))
        distanceToDecel = self.particle.vel.copy().multiply(
            (self.particle.vel.length() / self.maxAcceleration)).length()

        if distanceToStop < distanceToDecel:
            self.acceleration = -self.maxAcceleration

    def updateVelocity(self,nodeTraffic_dict,train_dict,relation_dict,line_dict,way_dict,node_dict):
        # check for condition of index incrementation
        self.checkIfReachedNode(way_dict,node_dict)

        currentVel=self.particle.vel.copy().length()
        nextNode = node_dict[self.nextNode]
        nextStop = node_dict[self.nextStop]

        if currentVel<nextNode['maxVel'] or nextNode==nextStop:
            self.acceleration=self.maxAcceleration

        elif currentVel>nextNode['maxVel'] and nextNode!=nextStop:
            self.acceleration=-self.maxAcceleration

        else:
            self.acceleration=0

        self.checkDecelForStop(node_dict)


        #second distance check with trains in the same stop location of the dictionary:
        stop=nodeTraffic_dict[self.nextStop]
        for id in stop:
            if id!=self.idObject:
                particle=stop[id]
                distanceToStop = self.particle.pos.copy().distanceTo(particle.pos)
                distanceToDecel = self.particle.vel.copy().multiply(
                    (self.particle.vel.length() / self.maxAcceleration)).length()

                if distanceToStop-10     < distanceToDecel and  self.particle.vel.copy().dot(particle.pos.copy().subtract( self.particle.pos)) > 0:
                    self.acceleration = -self.maxAcceleration
                    if self.particle.vel.length()<1:
                        self.acceleration=0
                        self.particle.vel.multiply(0)


        #update velocity in relation to acceleration
        if self.currentNode==self.nextNode:
            self.incrementIndexes(way_dict)
        if self.directionVect.length()!=0 and self.acceleration!=0:
            velToAdd= self.directionVect.copy().multiply(self.acceleration)
            velToAdd.multiply((time.time() - self.currentTime)*int(config['DEVELOPER']['SPEED_MULT']))
            self.particle.vel.add(velToAdd)


        #check if reached stop
        self.checkIfReachedStop(nodeTraffic_dict,relation_dict,line_dict,way_dict,node_dict)

    def checkIfReachedStop(self,nodeTraffic_dict,relation_dict,line_dict,way_dict,node_dict):
        if self.currentNode == self.nextStop :
            self.stopIndex+=1
            self.currentStop=self.nextStop
            # if in current remove, add yourself to

            stop=nodeTraffic_dict[self.currentStop]
            if self.idObject in stop:
                stop.pop(self.idObject)




            if self.stopIndex<len(self.stop_list):
                self.nextStop=self.stop_list[self.stopIndex]
                nextStopDic = nodeTraffic_dict[self.nextStop]
                nextStopDic.update({self.idObject: self.particle})
            else:
                self.reachedEnd=True
                if self.line1Bool:
                    self.setLine(relation_dict,line_dict,way_dict,node_dict,self.line2)
                    self.line1Bool=False
                else:
                    self.setLine(relation_dict, line_dict, way_dict, node_dict, self.line1)
                    self.line1Bool = True
            self.particle.vel.multiply(0)
    def setLine(self,relation_dict,line_dict,way_dict,node_dict,line_name):
        self.way_list = line_dict[line_name]  # make sure this is a list of ways by id's
        wayId = self.way_list[0]
        way = way_dict[wayId]
        self.node_list = way['nodes']

        self.stop_list = line.getStopListFromLineName(relation_dict,way_dict, line_name)

        self.reachedEnd = False

        self.wayIndex = 0
        self.nodeIndex = 1
        self.stopIndex = 0

        self.currentWay = self.way_list[self.wayIndex]
        self.currentStop = self.stop_list[self.stopIndex]
        self.nextStop = self.stop_list[self.stopIndex]
        self.currentNode = self.node_list[self.nodeIndex - 1]
        self.nextNode = self.node_list[self.nodeIndex]
        nodeCurrent = node_dict[self.currentNode]
        nodeNext = node_dict[self.nextNode]
        self.acceleration = 0

        vel = Vector(nodeNext['x'], nodeNext['y']).subtract(Vector(nodeCurrent['x'], nodeCurrent['y']))
        if vel.length() != 0:
            vel.normalize()
        self.directionVect = vel
        self.cooldown = nodeCurrent['delay']
        self.currentTime = time.time()



    def checkVel(self):
        pass

