import random
from External.Functions import getStationList,get_shortest_path
import time
class Person():
    def __init__(self,id,station):
        self.id=id
        self.homeStation=station
        self.currentStation=station
        self.nextStation=station
        self.train={}
        self.stationList=[]
        self.dayOver=False
        self.numberOfTrips=random.randint(0,5)
        self.traveling=False
        self.log=False
    def update(self,stop_dict,weighted_graph):
        # print("==========================")
        # print(self.currentStation)
        # print(self.stationList)
        # print("=========================")
        # sequence of events:
        #we have a home station
        if not self.dayOver:
            if len(self.stationList)==0 and not self.traveling:
                if self.numberOfTrips>0:
                    # print(stop_dict)
                    if len(list(stop_dict))>0:
                        stopStation=random.choice(list(weighted_graph))

                        self.generateRoute(weighted_graph,self.currentStation,stopStation)

                        while self.stationList==None:
                            # print(self.currentStation)
                            # print(weighted_graph[self.currentStation])
                            self.homeStation=random.choice(list(weighted_graph))
                            self.currentStation=self.homeStation
                            stopStation = random.choice(list(weighted_graph))
                            self.generateRoute(weighted_graph, self.currentStation, stopStation)

                        self.numberOfTrips-=1
                else:
                    if self.currentStation!=self.homeStation:
                        self.generateRoute(weighted_graph,self.currentStation,self.homeStation)
                    else:
                        self.dayOver=True
            if not self.traveling:
                self.checkBoarding(stop_dict)
            else:
                self.checkArrival(stop_dict)
        #if we dont have a route and we have the permission to generate one, then do so
        #if we have a route then we have a list of nodes we have to get through
        #if we are not on a train, then listen for trains on our comming to our station
        #for the train that has arrived check what furthest node it will get us to so we can get off to switch trains
        #if we have arrived to the last node complete the trip
        # if the trip is complete check if we have any more trips to do,
        # if we do repeat the above
        # otherwise complete the day by returning home unless we are already home.
        pass

    def checkArrival(self,stop_dict):
        station_list=[]
        for stationId in stop_dict:
            station=stop_dict[stationId]
            if station['name']==self.nextStation:
                station_list.append(station)
        for station in station_list:
            if len(station['train'])!=0:
                train=station['train']
                if 'id' in self.train:
                    if train['id']==self.train['id']:
                        self.disembark()
                        # print("ARRIVED AT DESTINATION:", self.nextStation)
                        self.traveling=False
                        self.currentStation=self.nextStation


        """ 
        check if the nodes associated with the next arrival contain the train with our current train id
        if one does, make the next stop the current stop and remove all previouse stops from the stop list
        check travelling is false
        set train id to none.
        """

    def checkBoarding(self,stop_dict):
        for stopId in stop_dict:
            stop=stop_dict[stopId]
            if stop['name']==self.currentStation:
                if len(stop['train'])!=0:

                    train=stop['train']
                    stop_list=train['stop_list']
                    station_names=[]
                    for a in range(train['stop_index'],len(stop_list)-1):
                        stopId=stop_list[a]
                        trainStop=stop_dict[stopId]
                        station_names.append(trainStop['name'])#list of stops the arrived train will still go through
                    #compare the station names to the stop list, board the train if any are the same and remove all the previous ones from our station list
                    chosenStation=''

                    for localStation in self.stationList:
                        if localStation in station_names:
                            chosenStation=localStation
                    location=0
                    if chosenStation!='':
                        location=self.stationList.index(chosenStation)
                        location+=1


                    if chosenStation != '':
                        self.board(train)
                        # print("BOARDED TRAIN DeSTINATION: ", chosenStation)
                        # print(self.stationList)
                        # print(location,len(self.stationList))
                        self.stationList=self.stationList[location:]
                        # print(self.stationList)
                        self.traveling=True
                        self.nextStation=chosenStation







        """
        check if there is a train in any of the nodes related to the current station name
        if there is a train check if it follows the names that are in our list
        find the last name that it follows that is in the list
        make that name the next station
        check travelling
        save current train id

        """

    def generateRoute(self,weighted_graph,startName,stopName):
        """
        generate a list of station along which the person has to travel.
        """
        # print('generating Route')

        self.stationList=get_shortest_path(weighted_graph,startName,stopName)
        self.log=True
        # print("route generated")
        # print("from: ",startName," To: ",stopName)
        # print(self.stationList)
    def encode(self):
        dict={"id: ":self.id,
              "Trip: ":self.stationList,
              "Number of Trips Left: ":self.numberOfTrips
              }
        return dict

    def board(self, train):
        self.train=train

    def disembark(self):

        self.train={}

