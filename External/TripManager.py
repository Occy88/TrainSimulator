from External.Person import Person
from External.Objects import *
import random
import json
import os
cwd=os.getcwd()
people_list=[]

def generatePeople():
    print("GENERATING PEOPLE")
    for a in range(0, 1000):
        print((a*100)/500000)
        stop =random.choice(list(weighted_graph_dict))
        person = Person(a, stop)
        print(stop)
        people_list.append(person)

def updatePeople():
    print("entered thread")

    with open(cwd+'/External/Logs','w') as outfile:
        while True:
            if not(len(list(stop_dict))<10):
                if (len(people_list)<1):
                    generatePeople()
                print("travelling")

                for people in people_list:
                    if people.log:
                        people.log=False
                        json.dump(people.encode(),outfile)
                        outfile.write("\n")
                    people.update(stop_dict,weighted_graph_dict)