from External.Objects import *

def recieveStops(stop):

    if not stop['id']in stop_dict:
        stop_dict.update({stop['id']:stop})
    else:
        if not stop == stop_dict[stop['id']]:
            stop_dict['id']=stop

def recieveWeightedGraph(graph):
    weighted_graph_dict.update(graph)
