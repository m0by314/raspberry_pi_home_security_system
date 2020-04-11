#!/usr/bin/env python

import time

from lib.camera import Camera
from lib.config import bot_id, registration_folder, video_time
from lib.telebot import Telepot
from lib.pir import Motiondetector

camera = Camera(registration_folder, video_time)
bot = Telepot(bot_id, camera)
pir = Motiondetector()

# handle configuration
@bot.handle("/start")
def on_start():
    bot.is_start = True
    return str("Start Bot")


@bot.handle("/stop")
def on_stop():
    bot.is_stop = False
    return str("Stop Bot")


@bot.handle("/status")
def on_status():
    if bot.is_start:
        return str("Listening Motion run")
    else:
        return str("Listen Motion doesn't run")

@bot.handle("/photo")
def on_photo():
    return camera.take_photo()


@bot.handle("/help")
def on_help():
    str = "command usage:\n"
    str += "\t/start launch the dectection\n"
    str += "\t/stop stop the detection\n"
    str += "\t/photo take a photo\n"
    str += "\t/status show status of the movement detection\n"
    str += "\t/help show help\n"
    str += "\t/clean remove all files in video folder\n"
    return str


@bot.handle("/clean")
def on_clean():
    return camera.purge_records()


print('I am listening ...')
try:
    while True:
        if bot.istart() and pir.detection():
            bot.send_video(camera.start_recording())
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera
