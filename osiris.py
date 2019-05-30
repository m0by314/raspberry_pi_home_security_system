#!/usr/bin/python3

import time
#from gpiozero import MotionSensor

#from lib.telebot import chat_listen, send_video, handle, bot
#from lib.camera import Camera
from lib.config import chat_id
#c = Camera()
#pir = MotionSensor(4)
import lib.telepot

bot = Telepot(chat_id)

print ('I am listening ...')
"""
try:
    while True:
            if is_listening:
               # if pir.motion_detected:
                   # print ("Motion")
                   # c.send_video(c.start_record())
                else :
                    time.sleep(1)
            else:
                time.sleep(1)

except KeyboardInterrupt:
""""
