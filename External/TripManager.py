from External.Person import Person
from External.Objects import *
import random
import json
import os
cwd=os.getcwd()
people_list=[]


def generatePeople():
    print("GENERATING PEOPLE")
    for a in range(0, 10000):
        print((a*100)/10000)
        stop =random.choice(list(weighted_graph_dict))
        while stop in exception_dict:
            stop = random.choice(list(weighted_graph_dict))

        person = Person(a, stop)
        print(stop)
        people_list.append(person)

def updatePeople():
    print("entered thread")

    with open(cwd+'/Logs','a+') as outfile:
        while True:
            if not(len(list(off_stop_dict))<10):
                if (len(people_list)<1):
                    generatePeople()

                a=0

                for people in people_list:
                    a+=1
                    print(a)
                    data=people.getData(weighted_graph_dict,off_stop_dict,exception_dict)
                    json.dump(data,outfile)
                    outfile.write("\n")
while True:
    updatePeople()