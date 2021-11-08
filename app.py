#!/usr/bin/env python
""" Home surveillance application """
import time
from functools import wraps
import RPi.GPIO

from telegram import Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)

from config import TOKEN_ID, REGISTRATION_FOLDER, VIDEO_TIME, CHAT_ID
from lib.camera import Camera
from lib.home_surveillance import HomeSurveillance


# Setup PIR Sensor
PIR_PIN = 4
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(PIR_PIN, RPi.GPIO.IN)

# Create an instance of the telegram.Bot
bot = Bot(token=TOKEN_ID)

# Create an instance of the camera
camera = Camera(REGISTRATION_FOLDER)

# Create an instance of HomeSurveillance
surveillance = HomeSurveillance()


def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        if int(chat_id) != int(CHAT_ID):
            update.message.reply_text('Unauthorized access.')
            return None  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped


###############
# Bot command #
###############


@restricted
def start(update: Update, context: CallbackContext) -> None:
    """Command /start: start surveillance."""
    surveillance.start()
    context.bot.send_message(chat_id=CHAT_ID, text="Surveillance is start")


@restricted
def stop(update: Update, context: CallbackContext) -> None:
    """Command /stop: stop surveillance."""
    surveillance.stop()
    context.bot.send_message(chat_id=CHAT_ID, text="Surveillance is stop")


@restricted
def status(update: Update, context: CallbackContext) -> None:
    """Command /status: show surveillance status."""
    context.bot.send_message(
        chat_id=CHAT_ID,
        text="Surveillance is active" if surveillance.is_start else "Surveillance is deactivated"
    )


@restricted
def man(update: Update, context: CallbackContext) -> None:
    """Command /help: show help."""
    usage = "command help:\n"
    usage += "\t/start : start the home monitoring system \n"
    usage += "\t/stop  : stop the home monitoring system\n"
    usage += "\t/status  : show the status of the monitoring system \n"
    usage += "\t/photo : take a picture\n"
    usage += "\t/video time=<duration> : records a video, \
                by default duration is " + str(VIDEO_TIME) + "s \n"
    usage += "\t/clean : remove all files in video folder\n"
    usage += "\t/help  : show help\n"
    context.bot.send_message(chat_id=CHAT_ID, text=usage)


@restricted
def photo(update: Update, context: CallbackContext) -> None:
    """ Command /photo: take a photo"""
    with open(camera.take_photo(), 'rb') as img:
        context.bot.send_photo(chat_id=CHAT_ID, photo=img)


@restricted
def video(update: Update, context: CallbackContext) -> None:
    """
    Command /video: record a video
    Takes an argument named time, corresponds to the duration of the video
    """
    # Default video time
    duration = VIDEO_TIME
    # Parse args to get duration value
    if context.args:
        key, value = context.args[0].split('=')
        if key == 'time':
            duration = value
        else:
            context.bot.send_message(chat_id=CHAT_ID, text=F"Argument {key} not recognized")
    # Start video recording
    record = camera.start_recording(duration)
    if record["error"] is None:
        with open(record["name"], 'rb') as video_file:
            bot.send_video(chat_id=CHAT_ID, video=video_file)
    else:
        bot.send_message(chat_id=CHAT_ID, text=video["error"])


@restricted
def clean(update: Update, context: CallbackContext) -> None:
    """ command /clean: remove file in REGISTRATION_FOLDER """
    context.bot.send_message(chat_id=CHAT_ID, text=camera.purge_records())


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN_ID)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("help", man))
    dispatcher.add_handler(CommandHandler("photo", photo))
    dispatcher.add_handler(CommandHandler("video", video, pass_args=True))
    dispatcher.add_handler(CommandHandler("clean", clean))

    # Start the Bot
    updater.start_polling()

    # Infinite loop for motion detection,
    # if motion is detected and surveillance is activated a video recording is taken
    # and sent through the telegram bot.
    time.sleep(2)  # We wait for 1 second to settle the sensor
    while True:
        if surveillance.is_start and RPi.GPIO.input(PIR_PIN):
            record = camera.start_recording(VIDEO_TIME)
            if record["error"] is None:
                with open(record["name"], 'rb') as video_file:
                    bot.send_video(chat_id=CHAT_ID, video=video_file, caption="Motion detected")
            else:
                bot.send_message(chat_id=CHAT_ID, text=video["error"])
            time.sleep(5)  # the sensor signal moves from high to low, it take around 5 seconds
        time.sleep(1)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
