import random
from External.Functions import getStationList,get_shortest_path
import time
class Person():
    def __init__(self,id,station):
        self.name=""
        self.money=100
        self.id=id
        self.tripStartTime=0
        self.tripTime=self.tripStartTime
        self.homeStation=station
        self.currentStation=station
        self.nextStation=station
        self.train={}
        self.stationList=[]
        self.dayOver=False

        self.shortestTime=1000000
        self.numberOfTrips=random.randint(1,5)
        self.traveling=False
        self.log=False


    def getData(self,weighted_graph,off_stop_dict,exception_dict):
        # print("==========\n\n\n\n===============")
        data={
            self.id:{
                    "name":self.name,
                    "number_of_trips":self.numberOfTrips,
                    "trips":[]
                    }
            }

        """
            everything centered around logging the following shematic of data:
            structure of data produced:
        {
            id:{
                name: "full-name"
                trips:{
                        money: "money-left"
                        trip_time: "hours-min-sec"
                        trip_cost: "cost"
                        trip_taken: "loctionA-locationB"
                        transits: [station1,station2,station3]
                        arrival_time: "time"
                        trains_taken: {
                                        train Id:
                                                {
                                                    Time: {
                                                        stop_list:[1,2,3]
                                                        stop_index: index
                                                        }
                                                }
                                        }
                }
        }

        """

        while self.numberOfTrips>=0:
            trip={'money': "money-left",
                        'time': "hours-min-sec",
                        'trip_cost': "cost",
                        'transits': [],
                        'arrival_time': "time",
                        'trains_taken': {}}
            #======GENERATE A ROUTE====
            if self.numberOfTrips==0:
                self.numberOfTrips-=1
                if self.currentStation != self.homeStation:
                    self.generateRoute(weighted_graph, self.currentStation, self.homeStation)


            else:

                stopStation = random.choice(list(weighted_graph))
                while stopStation in exception_dict or stopStation==self.nextStation:
                    stopStation = random.choice(list(weighted_graph))

                self.generateRoute(weighted_graph, self.currentStation, stopStation)
                # print("==============NEW ROUTE================")
                # print(self.currentStation,"==:==",stopStation)
                # print(self.stationList)
                while self.stationList == None:
                    # print(self.currentStation)
                    # print(weighted_graph[self.currentStation])
                    self.homeStation = random.choice(list(weighted_graph))
                    self.currentStation = self.homeStation
                    stopStation = random.choice(list(weighted_graph))
                    while stopStation == self.nextStation:
                        stopStation = random.choice(list(weighted_graph))

                    self.generateRoute(weighted_graph, self.currentStation, stopStation)
                self.numberOfTrips -= 1
            #============FIND TRAINS FOR SAID ROUTE====
            trip['trip_cost']=len(self.stationList)
            self.money-=len(self.stationList)
            trip['money']=self.money
            trip['time']=self.tripTime
            trip['transits']=self.stationList


            while len(self.stationList) >0:
                # print("===========FINDING TRAIN==============")
                check=self.getOnTrain(off_stop_dict,trip)
                if check=='Train Found':
                    continue
                    # self.getOffTrain()
                else:
                    print("No Train Found")
                    break

            properties=data[self.id]
            trips=properties['trips']
            trips.append(trip)
        return data

    def getOnTrain(self,off_stop_dict,trip):
        # print('Trip: ',self.currentStation,self.nextStation)
        """
        structure of dictionary:
        {data
            station_name: {
                        Train Id: {
                                    Time1{
                                        stop_list[n1,n2,n3]
                                        stop_index: ind
                                        }
                                    }


                     },
            station: {

}
        :param off_stop_dict:
        :return:
        """
        # get trains at current station
        valid_train_list=[]
        train_dict=off_stop_dict[self.currentStation]

        chosen_train_dict={}
        self.shortestTime=9000000
        for trainId in train_dict:
            times= train_dict[trainId]

            for time in times:
                chosenStation = ''
                if time>=self.tripTime and time<self.shortestTime:
                    properties=times[time]
                    stop_list=properties['stop_list']
                    stop_index=properties['stop_index']
                    station_names = []
                    for a in range(stop_index, len(stop_list)):
                        stopId = stop_list[a]
                        station_names.append( off_stop_dict[stopId])  # list of stops the arrived train will still go through
                    # compare the station names to the stop list, board the train if any are the same and remove all the previous ones from our station list


                    for localStation in self.stationList:
                        if localStation in station_names:
                            chosenStation = localStation

                if chosenStation!='':
                    # print(time)
                    self.nextStation=chosenStation
                    self.shortestTime=time
                    chosen_train_dict.update({time:(trainId,stop_list,stop_index)})

        if chosen_train_dict=={}:
            for trainId in train_dict:
                times = train_dict[trainId]

                for time in times:
                    chosenStation=''
                    if time >= self.tripTime and time<self.shortestTime:
                        properties = times[time]
                        stop_list = properties['stop_list']
                        # print("++++++++++++++++++++++++++++++++++++++++++++++++")
                        # print(time)
                        # print(stop_list)
                        # stop_index = properties['stop_index']
                        station_names = []
                        for a in range(0, len(stop_list)):

                            stopId = stop_list[a]

                            station_names.append(
                                off_stop_dict[stopId])  # list of stops the arrived train will still go through
                        # compare the station names to the stop list, board the train if any are the same and remove all the previous ones from our station list

                        for localStation in self.stationList:
                            if localStation in station_names:
                                chosenStation = localStation

                    if chosenStation != '':
                        self.nextStation=chosenStation
                        self.shortestTime=time
                        # print(time)
                        chosen_train_dict.update({time: (trainId, stop_list, stop_index)})

        # print("current: ", self.currentStation)
        # print("Next: ", self.nextStation)
        finalTime=100000000
        for time in chosen_train_dict:
            if time<finalTime:
                finalTime=time
        if finalTime==100000000:
            print("ABORTED REASON: NO TRAINS")
            return "No Trains"
        self.tripTime=finalTime
        trip['trains_taken'].update({time:trainId})
        (trainId,stop_list,stop_index)=chosen_train_dict[finalTime]
        self.train=trainId
        index=self.stationList.index(self.nextStation)
        index+=1
        self.stationList = self.stationList[index:]
        # print("new Route: ",self.stationList)
        # print("current: ", self.currentStation)
        # print("Next: ", self.nextStation)
        if len(self.stationList)>0:
            self.currentStation=self.nextStation
            self.nextStation=self.stationList[0]
        # print("current: ", self.currentStation)
        # print("Next: ", self.nextStation)
        #
        # print("TRAIN FOUND AND RECORDED")
        return "Train Found"



    def generateRoute(self,weighted_graph,startName,stopName):
        """
        generate a list of station along which the person has to travel.
        """
        # print('generating Route')
        # print('\ngenerating route from: ',startName,stopName )
        self.stationList=get_shortest_path(weighted_graph,startName,stopName)
        if self.stationList!=None:
            self.currentStation=self.stationList[0]
            self.nextStation=self.stationList[1]
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

