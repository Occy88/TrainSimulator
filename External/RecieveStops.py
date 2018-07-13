from External.Objects import *
import json
def recieveStops(stop):

    if not stop['id']in stop_dict:
        stop_dict.update({stop['id']:stop})
    else:
        if not stop == stop_dict[stop['id']]:
            stop_dict['id']=stop

def recieveWeightedGraph(graph):
    with open(cwd+'/External/WeightedGraph','w')as f:
        json.dump(graph,f)
