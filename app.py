#!/usr/bin/env python
"""
Home surveillance application
"""
import time
import subprocess

from gpiozero import CPUTemperature
from lib.camera import Camera
from lib.telebot import Telebot
from lib.pir import MotionDetector
from config import TOKEN_ID, REGISTRATION_FOLDER, VIDEO_TIME, CHAT_ID

camera = Camera(REGISTRATION_FOLDER)
bot = Telebot(TOKEN_ID, CHAT_ID)
pir = MotionDetector()
temp = cpu.temperature


@bot.handler("/start")
def on_start():
    """
    command /start: start bot
    """
    bot.is_listen = True
    return bot.send_message("Bot start")


@bot.handler("/stop")
def on_stop():
    """
    command /stop: stop bot
    """
    bot.is_listen = False
    return bot.send_message("Bot stop")


@bot.handler("/status")
def on_status():
    """
    command /status: show bot status
    """
    return bot.send_message("Listening Motion run") \
        if bot.is_listen else bot.send_message("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    """
    command /photo: take a photo
    """
    return bot.send_photo(camera.take_photo(), "photo")


@bot.handler("/video")
def on_video(*args):
    """
    command /video: record a video

    :param args: arguments of the bot's command
    """
    delay = args[0] if args else VIDEO_TIME
    bot.send_message("Recording start")
    return bot.send_video(camera.start_recording(delay), "video")


@bot.handler("/temp")
def on_temp():

    return bot.send_message(str("CPU temp. : ") + str(temp))


@bot.handler("/reboot")
def on_reboot():

    bot.send_message("Reboot command sent..")
    subprocess.call('sudo reboot now', shell=True)


@bot.handler("/usb")
def on_usb():

    p = subprocess.Popen("lsusb", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    return bot.send_message(str(p))


@bot.handler("/help")
def on_help():
    """
    command /help: show help
    :return: string
    """
    msg = "command usage:\n"
    msg += "\t/start : start the home monitoring system \n"
    msg += "\t/stop  : stop the home monitoring system\n"
    msg += "\t/status  : show the status of the monitoring system \n"
    msg += "\t/photo : take a picture\n"
    msg += "\t/video <delay> : records a video, by default delay is " + str(VIDEO_TIME) + "s \n"
    msg += "\t/clean : remove all files in video folder\n"
    msg += "\t/temp : CPU Temperature\n"
    msg += "\t/reboot : Reboot RPi\n"
    msg += "\t/usb : See connected USB devices\n"
    msg += "\t/help  : show help\n"
    return bot.send_message(msg)


@bot.handler("/clean")
def on_clean():
    """
    command /clean: remove file in REGISTRATION_FOLDER
    """
    return bot.send_message(camera.purge_records())


print('I am listening ...')
try:
    while True:
        if bot.is_listen and pir.movement_detected():
            bot.send_video(camera.start_recording(VIDEO_TIME), 'motion detected')
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera
