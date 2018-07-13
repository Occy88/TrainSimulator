print("""\
   mmm   mmmm  mmm     mmmm   mmmm   mmmm
 m"   " #"   "   #    #    # "   "# m"  "m
 #      "#mmm    #    "mmmm"   mmm" #  m #
 #          "#   #    #   "#     "# #    #
  "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm#
""")

import sys, configparser
import time
from SimpleGUICS2Pygame import simplegui_lib_fps
from SimpleGUICS2Pygame import simpleguics2pygame
#LOADING SETTINGS
config = configparser.ConfigParser()
#Open file as writeable
config.read_file(open('Classes/config'))


#Override settings when testing (to make it easier to run multiple instances)
if(len(sys.argv) > 1):
    print("OVERIDING SETTINGS_________________________")
    config['NETWORKING']['CONFIG_TYPE'] = sys.argv[1]

    config.set('NETWORKING', 'CONFIG_TYPE', sys.argv[1])
    with open('Classes/config', "w") as conf:

        config.write(conf)

#reopen
#config.read_file(open('Classes/config'))

# #LOAD INTERNAL CLASSES
# from Transfer.comms import communicate, recieve, ping
from Handlers.KeyHandler import keydown, keyup
from Handlers.ClickHandler import checkClick
from Loading.Objects import send_list
from Loading.Objects import *
from Loading.Objects import simTime
from GameStates.intro import introLoop, waitingLoop,storyLoop
from threading import Thread
#-----START----GAME----CLOCK
fps = simplegui_lib_fps.FPS()
fps.start()
#initiate Ai
# print("HERE")
# updateP=Thread(target=updatePeople)
# print("then here")
# updateP.start()

print("NOW Here ")

print("MONSTERS LOADED AND SPAWNED")
cwd=os.getcwd()


#--------------GAME-----LOOP-------------------


startTime=time.time()
currentTime=time.time()

def draw(canvas):

#========== GAME LOOPS NON MAIN =====================

        # x,y=train.nextNode['lon'],train.nextNode['lat']
        # pos=Vector(x,y).transformToCam(cam)
        # canvas.draw_circle((pos.getX(),pos.getY()), 20, 2, 'Yellow')

    if gameState1.main and  gameState2.main:
        # line.drawByName(canvas, cam, line_dict, way_dict, node_dict, 'Waterloo & City: Waterloo → Bank',
        #                 'blue')
        autoCam.update(cam,train_dict)
        # mapLoader.update((baseNode['lat'], baseNode['lon']), cam, spriteDictionary)
        # mapLoader.draw(canvas, cam)
        trainLoader.load(train_dict,spriteDictionary,relation_dict,line_dict,way_dict,node_dict,nodeTraffic_dict,variables['simulation_speed'])
        global simTime,currentTime
        simTime += (time.time() - currentTime) * variables['simulation_speed']
        currentTime=time.time()

        timeString="("+str(round(((simTime/60)/60)))+" : "+str(round((simTime/60)%60))+" : "+str(round(simTime%60,1))+")"
        timeLable.set_text(timeString)
        for trainId in train_dict:
            train=train_dict[trainId]
            train.update(nodeTraffic_dict,relation_dict,line_dict,way_dict,node_dict,variables['simulation_speed'])
            # line.drawNodeList(canvas,cam,node_dict,all_stops)
            # train.draw(canvas,cam,node_dict)
            if train.send:
                train.send=False
                stopId=train.currentStop
                stop=all_stops_dict[stopId]
                stop['train']=train.encode()

                stop['time']=simTime
                send_list.append(stop)
            # if train.remove:
            #     train.remove=False
            #     stopId = train.currentStop
            #     stop = all_stops_dict[stopId]
            #     stop['train'] = {}
            #     send_list.append(stop)
        if len(send_list)>0:
            with open(cwd + '/Loading/TrainLog', 'a+') as outfile:
                for stop in send_list:

                    json.dump(stop,outfile)
                    outfile.write("\n")
            send_list.clear()


        numTrains.set_text('Number of Trains: '+str(len(train_dict)))

#========================  ===========================================

#================ CLICK HANDLER =================================

        checkClick()

#================ CLICK HANDLER END =================================

#===================================================================

#================ DRAW AND UPDATES =================================

    #  -------UPDATE-AND-DRAW---OBJECTS---BY---LAYER---PRIORITY



        # x,y=train.nextNode['lon'],train.nextNode['lat']
        # pos=Vector(x,y).transformToCam(cam)
        # canvas.draw_circle((pos.getX(),pos.getY()), 20, 2, 'Yellow')

    # --------------- CONSTRUCT AND DRAW LINES FROM THE WAYS -------

 # ========================================================================================

#  ======================== CAMERA UPDATE ===============================================================
        cam.move()
        cam.zoom()

        fps.draw_fct(canvas)
# ========================== CAMERA UPDATE END==============================================================

# ========================================================================================

# ========================== STATS DISPLAY ==============================================================

        #DISPLAY STATS:

        # life.set_text('CamX: ' + str(train.particle.pos))

##
## Init
##
frame = simpleguics2pygame.create_frame('Game', int(config['CANVAS']['CANVAS_WIDTH']), int(config['CANVAS']['CANVAS_HEIGHT']))
frame.set_canvas_background('Black')
#Labels
numTrains = frame.add_label('Number of Trains: '+str(len(train_dict)))
timeLable = frame.add_label('Time: ')
rng = frame.add_label('Ranfe: ')
arrows = frame.add_label('Arrows: ')
spells = frame.add_label('Spells: ')

remote = frame.add_label('Remote Addr: ' + config['NETWORKING']['client_ip'])

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()