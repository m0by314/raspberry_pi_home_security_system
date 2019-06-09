#!/usr/bin/python3

import time

from lib.camera import Camera
from lib.config import bot_id ,video_path, video_time
from lib.telebot import Telepot
from lib.pir import Motion

bot = Telepot(bot_id, video_path)
cam = Camera(video_path, video_time)
pir = Motion()

print('I am listening ...')

#TODO build loop
while True:
    if bot.islisten:
        pir.dectection()
     else:
        time.sleep(1)
