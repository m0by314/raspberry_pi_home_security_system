#!/usr/bin/env python
"""
Home surveillance application
"""
import time

from lib.camera import Camera
from lib.config import BOT_ID, REGISTRATION_FOLDER, VIDEO_TIME
from lib.telebot import Telebot
from lib.pir import Motiondetector

camera = Camera(REGISTRATION_FOLDER, VIDEO_TIME)
bot = Telebot(BOT_ID)
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
    return str("Listening Motion run") if bot.is_listen else str("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    return camera.take_photo()


@bot.handler("/help")
def on_help():
    msg = "command usage:\n"
    msg += "\t/start launch the dectection\n"
    msg += "\t/stop stop the detection\n"
    msg += "\t/photo take a photo\n"
    msg += "\t/status show status of the movement detection\n"
    msg += "\t/help show help\n"
    msg += "\t/clean remove all files in video folder\n"
    return msg


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
