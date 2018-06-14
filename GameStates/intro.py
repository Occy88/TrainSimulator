#    mmm   mmmm  mmm     mmmm   mmmm   mmmm
#  m"   " #"   "   #    #    # "   "# m"  "m
#  #      "#mmm    #    "mmmm"   mmm" #  m #
#  #          "#   #    #   "#     "# #    #
#   "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm#

import pygame
from SimpleGUICS2Pygame import simplegui_lib_draw
from Loading.Objects import gameState1, splash,story
import configparser
config = configparser.ConfigParser()
config.read_file(open('Classes/config'))
#LOADING LIBRARIES

def introLoop(canvas):

    left, middle, right = pygame.mouse.get_pressed()

    if left:
        gameState1.introToMain()
    if right:
        gameState1.introToStory()

    canvas.draw_image(splash, (splash.get_width()/2,splash.get_height()/2), (splash.get_width(), splash.get_height()), (int(config['CANVAS']['CANVAS_WIDTH'])/2,int(config['CANVAS']['CANVAS_HEIGHT'])/2), (int(config['CANVAS']['CANVAS_WIDTH']),int(config['CANVAS']['CANVAS_HEIGHT'])), 0)

    canvas.draw_text('Left Click anywhere to start', ((int(config['CANVAS']['CANVAS_WIDTH'])/20,int(config['CANVAS']['CANVAS_HEIGHT'])/10)), 30, "Black")
    canvas.draw_text('Right Click and hold anywhere for story', ((int(config['CANVAS']['CANVAS_WIDTH'])/20,int(config['CANVAS']['CANVAS_HEIGHT'])/6)), 30, "Black")
    #simplegui_lib_draw.draw_rect(canvas, (250,250), (100,100), 1, 'Black', fill_color='Black')

def storyLoop(canvas):
    left, middle, right = pygame.mouse.get_pressed()
    if right:
        gameState1.storyToIntro()
    canvas.draw_image(story, (story.get_width() / 2, story.get_height() / 2),
                      (story.get_width(), story.get_height()),
                      (int(config['CANVAS']['CANVAS_WIDTH']) / 2, int(config['CANVAS']['CANVAS_HEIGHT']) / 2),
                      (int(config['CANVAS']['CANVAS_WIDTH']), int(config['CANVAS']['CANVAS_HEIGHT'])), 0)


def waitingLoop(canvas):
    canvas.draw_text('waiting for player 2', (150, 200), 30, "Magenta")

    simplegui_lib_draw.draw_rect(canvas, (250, 250),
                                 (100, 100), 1, 'Black', fill_color='Black')

