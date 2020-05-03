#!/usr/bin/env python
"""
Home surveillance application
"""
import time

from lib.camera import Camera
from lib.config import TOKEN_ID, REGISTRATION_FOLDER, VIDEO_TIME
from lib.telebot import Telebot
from lib.pir import MotionDetector

camera = Camera(REGISTRATION_FOLDER)
bot = Telebot(TOKEN_ID)
pir = MotionDetector()


@bot.handler("/start")
def on_start():
    """
    command /start: start bot
    """
    bot.is_listen = True
    bot.send_message("Bot start")


@bot.handler("/stop")
def on_stop():
    """
    command /stop: stop bot
    """
    bot.is_listen = False
    bot.send_message("Bot stop")


@bot.handler("/status")
def on_status():
    """
    command /status: show bot status
    """
    bot.send_message("Listening Motion run") if bot.is_listen else bot.send_message("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    """
    command /photo: take a photo
    """
    bot.send_photo(camera.take_photo(), "photo")


@bot.handler("/video")
def on_video(*args):
    """
    command /video: record a video

    :param args: arguments of the bot's command
    """
    bot.send_message("Recording start")
    bot.send_video(camera.start_recording(args[0]), "video")


@bot.handler("/help")
def on_help():
    """
    command /help: show help
    :return: string
    """
    msg = "command usage:\n"
    msg += "\t/start : start the home monitoring system \n"
    msg += "\t/stop  : stop the home monitoring system\n"
    msg += "\t/show  : show the status of the monitoring system \n"
    msg += "\t/photo : take a picture\n"
    msg += "\t/video time=<delay> : records a video, argument time defines the duration of the recording\n"
    msg += "\t/clean : remove all files in video folder\n"
    msg += "\t/help  : show help\n"
    bot.send_message(msg)


@bot.handler("/clean")
def on_clean():
    """
    command /clean: remove file in REGISTRATION_FOLDER
    """
    bot.send_message(camera.purge_records())


print('I am listening ...')
try:
    while True:
        if bot.is_listen and pir.movement_detected():
            bot.send_video(camera.start_recording(VIDEO_TIME), 'motion detected')
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera
