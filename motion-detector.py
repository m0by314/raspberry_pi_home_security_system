#!/usr/bin/env python

import time

from lib.camera import Camera
from lib.config import bot_id, video_path, video_time
from lib.telebot import Telepot
from lib.pir import Motiondetector

camera = Camera(video_path, video_time)
bot = Telepot(bot_id, cam)
pir = Motiondetector()

print('I am listening ...')

try:
    while True:
        if bot.islisten() and pir.detection():
            bot.send_video(camera.start_record())
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera
