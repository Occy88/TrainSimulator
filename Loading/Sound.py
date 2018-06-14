import sched
import time
import copy

class SoundManager:
    def __init__(self, sound_dict):
        self.sound_dict = sound_dict

        self.sound_sched = sched.scheduler(time.time, time.sleep)

        self.active_sound_dict = {}
        self.active_bg_index = None

        self.sound_bg_name_list = []
        self.sound_bg_index = 0

    def updateSoundDict(self, sound_dict):
        self.sound_dict.update(sound_dict)

    def update(self):
        self.sound_sched.run(False)

    def __removeSound(self, sound_id):
        if sound_id == self.active_bg_index:
            self.active_bg_index = None
        
        del self.active_sound_dict[sound_id]

    def playSound(self, sound_name):
        self.__playSound(sound_name, False)

    def __playSound(self, sound_name, is_bg):
        if sound_name in self.sound_dict:
            time_delay = self.sound_dict[sound_name]._get_length()
            if time_delay > 0:
                i = 0
                while (i in self.active_sound_dict):
                    i +=1
                    
                sound = copy.copy(self.sound_dict[sound_name])
                
                self.sound_sched.enter(time_delay, 2, self.__removeSound, kwargs={"sound_id":i})
                self.active_sound_dict.update({i:sound})

                self.active_sound_dict[i].play()

                if is_bg:
                    if self.active_bg_index != None:
                        self.active_sound_dict[self.active_bg_index].pause()
                    
                    self.active_bg_index = i
            else:
                self.sound_dict.pop(sound_name)

            ##used for bg no need to re calculate
            return time_delay
                        

    def setContinuousBackgroundList(self, sound_name_list):
        self.sound_bg_index = 0
        self.sound_bg_name_list = [x for x in sound_name_list if x in self.sound_dict]
        self.__playBG()

    def __playBG(self):     
        if self.sound_bg_name_list:#not empty
            self.sound_bg_index %= len(self.sound_bg_name_list)
            
            if self.sound_bg_name_list[self.sound_bg_index] in self.sound_dict:
                time_delay = self.__playSound(self.sound_bg_name_list[self.sound_bg_index], True)

                if time_delay > 0:
                    self.sound_sched.enter(time_delay, 1, self.__playBG)
                    self.sound_bg_index +=1
                else:
                    self.sound_bg_name_list.pop(self.sound_bg_index)
                    self.__playBG()

            else:
                self.sound_bg_name_list.pop(self.sound_bg_index)
                self.__playBG()

####### DOCUMENTATION #######
"""
s1 = simplegui._load_local_sound(<fileName>)
    create a sound object using relative file name, eg "a.wav"
    .wav's work havent tested others

s1.set_volume(<float>)
    set volume, float from 0 to 1, default 1

s = Sound(<sound dict>)
    dict is of form {<String sound_name>:<sound object>}
    basically name to refer to sound object and the sound object

s.setContinuousBackgroundList(<List of <String sound_name>>)
    list of sound names to loop through continuously

s.playSound(<String sound_name>)
    set sound that will play till completion and stop,
    can have multiple of same sound_name playing at once

s.updateSoundDict(<sound dict>)
    adds new sound dict to old one like normal dict

s.update()
    run once per game loop or whenever.
    #cleanup & play next in bg loop
"""

####### TEST #######
"""
def draw(canvas):
    sound_manager.update()
    

from SimpleGUICS2Pygame import simpleguics2pygame
import os

cwd = os.getcwd()

sound_bg = simpleguics2pygame._load_local_sound('background.wav')
sound_bg.set_volume(0.1)
sound_loaded = simpleguics2pygame._load_local_sound('loadingcomplete.wav')
sound_loaded.set_volume(0.2)

sound_dict = {
     "bg":sound_bg,
     "lc":sound_loaded}

sound_manager = SoundManager({})
sound_manager.updateSoundDict(sound_dict)

sound_manager.setContinuousBackgroundList(["bg"])
sound_manager.playSound("lc")

sound_manager.update()

frame = simpleguics2pygame.create_frame('Game', 20, 20)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw)

frame.start()
"""
