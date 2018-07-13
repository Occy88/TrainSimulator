import os
import json
cwd=os.getcwd()
weighted_graph_dict={}
stop_dict = {}
off_stop_dict={}
with open(cwd+'/WeightedGraph','r')as f:
    line = True
    while line:
        line = f.readline()

        if line:
            data = json.loads(line)
            weighted_graph_dict = data
exception_dict={}

with open(cwd+'/RouteData','r')as f:
    line=True
    while line:
        line=f.readline()
        print(line)
        if line:
            data=json.loads(line)
        print(data)
with open(cwd+'/TrainLog','r')as f:
    line=True
    while line:
        line=f.readline()
        if line:
            data=json.loads(line)
        if not data['id'] in off_stop_dict:
            off_stop_dict.update({data['id']:data['name']})
        if not data['name'] in off_stop_dict:
            train=data['train']
            off_stop_dict.update({data['name']:{}})
        elif len(data['train'])>0:
            train=data['train']
            if not train['id'] in off_stop_dict[data['name']]:
                off_stop_dict[data['name']].update({train['id']:{}})
            else:
                stop=off_stop_dict[data['name']]
                loc_train=stop[train['id']]
                loc_train.update({data['time']:{'stop_list':train['stop_list'],'stop_index':train['stop_index']}})
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    # with open(cwd + '/External/test', 'w')as f1:
    #     json.dump(off_stop_dict,f1)
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
print(off_stop_dict['Bank'])
for stuff in off_stop_dict:

    if off_stop_dict[stuff]=='Waterloo':
        print(stuff)

"""
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
"""
structure of dictionary:
{data
    stopId:"stationName",
    stopId2:"stationName2",
    
    station_name: {  
                Train Id: {
                            Time1{
                                stop_list[n1,n2,n3]
                                stop_index: ind
                                }
                            }
                            
                
             },
    station_name2: {
                Train Id: {
                            Time1{
                                stop_list[n1,n2,n3]
                                stop_index: ind
                                }
                            }
                            
                
             },
    
}
"""
