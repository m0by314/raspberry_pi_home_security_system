#!/usr/bin/python3

import time
#from gpiozero import MotionSensor

#from lib.telebot import chat_listen, send_video, handle, bot
#from lib.camera import Camera
from lib.config import bot_id
#c = Camera()
#pir = MotionSensor(4
from lib.telebot import Telepot

bot = Telepot(bot_id)

print ('I am listening ...')

while True:
    time.sleep(1)
