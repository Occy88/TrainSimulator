print("""\
   mmm   mmmm  mmm     mmmm   mmmm   mmmm
 m"   " #"   "   #    #    # "   "# m"  "m
 #      "#mmm    #    "mmmm"   mmm" #  m #
 #          "#   #    #   "#     "# #    #
  "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm#
""")

import sys, configparser
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
from Loading.Objects import *
from GameStates.intro import introLoop, waitingLoop,storyLoop

#-----START----GAME----CLOCK
fps = simplegui_lib_fps.FPS()
fps.start()
#initiate Ai

print("MONSTERS LOADED AND SPAWNED")



#--------------GAME-----LOOP-------------------
def draw(canvas):
    

#========== GAME LOOPS NON MAIN =====================

    if gameState1.main and  gameState2.main:
        line.drawByName(canvas, cam, line_dict, way_dict, node_dict, testLine1,
                        'blue')
        line.drawByName(canvas, cam, line_dict, way_dict, node_dict,testLine2,'red')

        for trainId in train_dict:
            train=train_dict[trainId]
            train.update(nodeTraffic_dict,train_dict,relation_dict,line_dict,way_dict,node_dict)
            line.drawNodeList(canvas,cam,node_dict,all_stops)
            train.draw(canvas,cam,node_dict)

#===================================================================

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
life = frame.add_label('Life: ')
magic = frame.add_label('Magic: ')
rng = frame.add_label('Ranfe: ')
arrows = frame.add_label('Arrows: ')
spells = frame.add_label('Spells: ')

remote = frame.add_label('Remote Addr: ' + config['NETWORKING']['client_ip'])

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()