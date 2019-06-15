#!/usr/bin/python3

import time

from lib.camera import Camera
from lib.config import bot_id, video_path, video_time
from lib.telebot import Telepot
from lib.pir import Motion

cam = Camera(video_path, video_time)
bot = Telepot(bot_id, cam)
pir = Motion(cam)

print('I am listening ...')


try:
    while True:
        if bot.islisten() and pir.detection():
            cam.start_record()
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del cam
