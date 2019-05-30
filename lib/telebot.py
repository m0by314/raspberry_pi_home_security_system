#! /usr/bin/python3

### Fonction for using Telegram bot

import telepot
from datetime    import timedelta
from .config      import bot_id, tmp_path
from .camera     import selfie


class Telepot:
    def __init__(self,bot_id) :
        self.bot = telepot.Bot(bot_id)
        self.chat_listen = {}
        self.bot.message_loop(self.handle())
        
    
    def __islisten(self):
        if self.chat_id in self.chat_listen:
            return True
        else
            self.chat_listen[self.chat_id] = True
            return False
        
    def handle(self,msg):
        self.chat_id = msg['chat']['id]
        self.command = msg['text']
        
        if self.command == '/start':
            if self.__islisten() : 
                self.bot.sendMessage(self.chat_id, "Listen Motion is already use")
            else :
                self.bot.sendMessage(self.chat_id, "Listen Motion start")     
                                   
        elif self.command == '/stop':
            if self.__listen():
                bot.sendMessage(chat_id, "Listening Motion stop"))
            else:
                bot.sendMessage(chat_id, "Listen Motion doesn't run")
                                   
                                   
"""                                
import time
import subprocess

bot = telepot.Bot(bot_id)
chat_listen = {}


def handle(msg):
   
    global chat_id
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Got command: %s' % command)

    if command == '/start':

        if chat_id not in chat_listen:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Started Listen Motion")
        elif chat_listen[chat_id]:
            bot.sendMessage(chat_id, "Already Listening")
        else:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Restarted Listen Motion")

        print ("%s said it want to be notified" % chat_id)

    elif command == '/stop':

        if chat_id not in chat_listen:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Wasn't Listening Motion")
        elif chat_listen[chat_id]:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Stopped Listening")
        else:
            bot.sendMessage(chat_id, "Wasn't Listen Motion")

        print ("%s said it doesn't want to be notified" % chat_id)

    elif command == '/snap':

        if ( chat_id not in chat_listen ) or ( chat_listen[chat_id] == False ):
            bot.sendMessage(chat_id, "Bot doesn't run")
        else:
            bot.sendMessage(chat_id, "Take a photo")
            bot.sendPhoto(chat_id, photo=open(selfie(), 'rb'), caption='photo')

    elif command == '/status':

        if ( chat_id not in chat_listen ) or ( chat_listen[chat_id] == False ):
          bot.sendMessage(chat_id, "status : Not start")
        else:
            bot.sendMessage(chat_id, "status : Running")

    elif command == '/help':

        bot.sendMessage(chat_id, _usage())
        print ("%s send usage" % chat_id)

    elif command == '/clean':
        bot.sendMessage(chat_id, _remove())
        print ("%s remove file" % chat_id)

def _usage():

    str =  "command usage:\n"
    str += "   /start launch the dectection\n"
    str += "   /stop stop the detection\n"
    str += "   /snap take a photo\n"
    str += "   /status show status of the movement detection\n"
    str += "   /help show help\n"
    str += "   /clean remove all files in video folder\n"

    return str

def _remove():

    command ="cd "+ tmp_path + " && rm *"

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        status = 'FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output)
        return status
    else :
        status = 'files removed'
        return status

def send_video(vid):

    for key, val in vid.items():
        if key == 0:
            bot.sendVideo(chat_id, video=open(val, 'rb'), caption='Motion Detected')
        else:
            bot.sendMessage(chat_id, val)
"""
