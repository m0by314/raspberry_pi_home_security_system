#!/usr/bin/env python

import time

from lib.camera import Camera
from lib.config import bot_id, video_time, registration_folder
from lib.telebot import Telebot
from lib.pir import Motiondetector

camera = Camera(registration_folder, video_time)
bot = Telebot(bot_id)
pir = Motiondetector()


# handle configuration
@bot.handler("/start")
def on_start():
    bot.is_listen = True
    return str("Start Bot")


@bot.handler("/stop")
def on_stop():
    bot.is_listen = False
    return str("Stop Bot")


@bot.handler("/status")
def on_status():
    if bot.is_listen:
        return str("Listening Motion run")
    else:
        return str("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    return camera.take_photo()


@bot.handler("/help")
def on_help():
    str = "command usage:\n"
    str += "\t/start launch the dectection\n"
    str += "\t/stop stop the detection\n"
    str += "\t/photo take a photo\n"
    str += "\t/status show status of the movement detection\n"
    str += "\t/help show help\n"
    str += "\t/clean remove all files in video folder\n"
    return str


@bot.handler("/clean")
def on_clean():
    return camera.purge_records()


print('I am listening ...')
try:
    while True:
        if bot.is_listen and pir.movement_detected():
            bot.send_video(camera.start_recording())
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera

