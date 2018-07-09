from urllib import request
from io import BytesIO

import json

import requests


def getStationList(start,end):
    print("GENERATION: ",start,end)
    start=start.replace(' ','%20')
    end= end.replace(' ','%20')
    url= 'https://api.tfl.gov.uk/Journey/JourneyResults/'+start + '%20underground%20station/to/'+end+'%20underground%20station'
    # url = 'https://api.tfl.gov.uk/Journey/JourneyResults/wimbledon%20park%20underground%20station/to/bank%20station%20underground?journeyPreference=LeastWalking&mode=tube&accessibilityPreference=NoRequirements'


    querystring = {"journeyPreference": "LeastWalking", "mode": "tube", "accessibilityPreference": "NoRequirements"}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "afbea7f6-2fb2-4566-a492-9e9598874f10"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    station_list = []
    if (response.status_code != 200):
        raise Exception("The status code was:", response.status_code, "for question:", url)
    di = response.json()
    print("JASON: ",di)
    journey_list = []
    for data in di:
        journeys = di['journeys']
    for data in journeys:
        journey_list.append(data)
    journey = journey_list[0]
    leg_list = []
    print("================JOURNEY==================")
    for data in journey:
        legs = journey['legs']

    for data in legs:
        leg_list.append(data)

    for leg in leg_list:

        print("=====================LEG=====================")
        path = leg['path']
        stopPoints = path['stopPoints']
        for data in stopPoints:
            name = data['name']
            new = name.replace(" Underground Station", "")
            new = new.split(' (')[0]
            station_list.append(new)
    return(station_list)


def get_shortest_path(weighted_graph, start, end):
    """
    Calculate the shortest path for a directed weighted graph.

    Node can be virtually any hashable datatype.

    :param start: starting node
    :param end: ending node
    :param weighted_graph: {"node1": {"node2": "weight", ...}, ...}
    :return: ["START", ... nodes between ..., "END"] or None, if there is no
             path
    """

    # We always need to visit the start
    nodes_to_visit = {start}
    visited_nodes = set()
    # Distance from start to start is 0
    distance_from_start = {start: 0}
    tentative_parents = {}

    while nodes_to_visit:
        # The next node should be the one with the smallest weight
        current = min([(distance_from_start[node], node) for node in nodes_to_visit])[1]

        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = weighted_graph[current]
        unvisited_neighbours = set(edges).difference(visited_nodes)
        for neighbour in unvisited_neighbours:
            neighbour_distance = distance_from_start[current] + \
                                 edges[neighbour]
            if neighbour_distance < distance_from_start.get(neighbour,
                                                            float('inf')):
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)

    return _deconstruct_path(tentative_parents, end)


def _deconstruct_path(tentative_parents, end):
    if end not in tentative_parents:
        return None
    cursor = end
    path = []
    while cursor:
        path.append(cursor)
        cursor = tentative_parents.get(cursor)
    return list(reversed(path))