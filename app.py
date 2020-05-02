#!/usr/bin/env python
"""
Home surveillance application
"""
import time

from lib.camera import Camera
from lib.config import TOKEN_ID, REGISTRATION_FOLDER, VIDEO_TIME
from lib.telebot import Telebot
from lib.pir import MotionDetector

camera = Camera(REGISTRATION_FOLDER, VIDEO_TIME)
bot = Telebot(TOKEN_ID)
pir = MotionDetector()


@bot.handler("/start")
def on_start():
    """
    command /start: start bot
    :return: string
    """
    bot.is_listen = True
    return str("Start Bot")


@bot.handler("/stop")
def on_stop():
    """
    command /stop: stop bot
    :return: string
    """
    bot.is_listen = False
    return str("Stop Bot")


@bot.handler("/status")
def on_status():
    """
    command /status: show bot status
    :return: string
    """
    return str("Listening Motion run") if bot.is_listen else str("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    """
    command /photo: take a photo
    :return: file format .jpeg
    """
    return camera.take_photo()


@bot.handler("/help")
def on_help():
    """
    command /help: show help
    :return: string
    """
    msg = "command usage:\n"
    msg += "\t/start the home monitoring system \n"
    msg += "\t/stop the home monitoring system\n"
    msg += "\t/show the status of the monitoring system \n"
    msg += "\t/photo take a picture\n"
    msg += "\t/clean remove all files in video folder\n"
    msg += "\t/help show help\n"
    return msg


@bot.handler("/clean")
def on_clean():
    """
    command /clean: remove file in REGISTRATION_FOLDER
    :return: function
    """
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
