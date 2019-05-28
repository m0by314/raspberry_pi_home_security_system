#!/usr/bin/python3

import time
from gpiozero import MotionSensor

from lib.telebot import chat_listen, send_video, handle, bot
import lib.camera as camera

c = camera.()
pir = MotionSensor(4)

bot.message_loop(handle) # start bot , wait commands

print ('I am listening ...')

try:
    while True:
        for chat_id, is_listening in chat_listen.items():
            if is_listening:
                if pir.motion_detected:
                    print ("Motion")
                    c.send_video(c.start_record())
                else :
                    time.sleep(1)
            else:
                time.sleep(1)

except KeyboardInterrupt:
    c.camera.close()
