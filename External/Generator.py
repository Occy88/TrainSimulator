from External.Person import Person
from External.Objects import *
from External.Functions import get_shortest_path
import random
import json
import os
cwd=os.getcwd()
people_list=[]


def generatePeople():
    print("GENERATING PEOPLE")

    with open(cwd + '/PeopleData', 'a+')as f:
        y = 0
        for name in weighted_graph_dict:

            y+=1
            print(y)
            for a in range(0,10000):
                dict={a:name}
                json.dump(dict,f)


def generateRoutes():
    y=0
    with open(cwd+'/RouteData','a+')as f:

        for stop in weighted_graph_dict:
            y+=1
            print(y)
            dic={stop:[]}
            for a in range(0,100):
                arrival=random.choice(list(weighted_graph_dict))
                stationList = get_shortest_path(weighted_graph_dict, stop, arrival)
                x=0
                while stationList==None:
                    x+=1
                    arrival = random.choice(list(weighted_graph_dict))
                    stationList = get_shortest_path(weighted_graph_dict, stop, arrival)
                    if x>=20:
                        print('NO STAIONS')
                        print(a)
                        break

                dic[stop].append(stationList)
            json.dump(dic,f)

# print("people")
# generatePeople()
print("ROUTES")
generateRoutes()