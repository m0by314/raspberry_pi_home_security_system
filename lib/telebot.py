#! /usr/bin/python3

import telepot
import subprocess


class Telepot:
    """
    Class for using telegram bot with telepot
    """

    def __init__(self, bot_id, cam):
        super().__init__()
        self.bot = telepot.Bot(bot_id)
        self.chat_listen = {}
        self.bot.message_loop(self.handle)
        self.chat_id = None
        self.command = None
        self.camera = cam

    def islisten(self):
        if self.chat_id in self.chat_listen:
            return True

    def handle(self, msg):
        """
        parse command send by bot
        """
        self.chat_id = msg['chat']['id']
        self.command = msg['text']

        if self.command == '/start':
            if self.islisten():
                self.bot.sendMessage(self.chat_id, "Listen Motion is already use")
            else:
                self.bot.sendMessage(self.chat_id, "Listen Motion start")
                self.chat_listen[self.chat_id] = True

        elif self.command == '/stop':
            if self.islisten():
                self.bot.sendMessage(self.chat_id, "Listening Motion stop")
                self.chat_listen[self.chat_id] = None
            else:
                self.bot.sendMessage(self.chat_id, "Listen Motion doesn't run")

        elif self.command == '/status':
            if self.islisten():
                self.bot.sendMessage(self.chat_id, "Bot is running")
            else:
                self.bot.sendMessage(self.chat_id, "Bot doesn't run")

        elif self.command == '/help':
            return self.usage()

        elif self.command == '/snap':
            if self.islisten():
                self.bot.sendMessage(self.chat_id, "Take a photo")
                self.bot.sendPhoto(self.chat_id, photo=open(self.camera.selfie(), 'rb'), caption='photo')
            else:
                self.bot.sendMessage(self.chat_id, "Listen Motion not start")

        elif self.command == '/clean':
            self.bot.sendMessage(self.chat_id, self._remove)

    @staticmethod
    def usage():
        str = "command usage:\n"
        str += "\t/start launch the dectection\n"
        str += "\t/stop stop the detection\n"
        str += "\t/snap take a photo\n"
        str += "\t/status show status of the movement detection\n"
        str += "\t/help show help\n"
        str += "\t/clean remove all files in video folder\n"
        return str

    def _remove(self):
        # TODO build getter for video path
        command = "cd " + self.camera.getvid_path + " && rm *"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            status = 'FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output)
            return status
        else:
            status = 'files removed'
            return status

    def send_video(self, vid):
        # TODO revoir le passage de la video camera.start_record. 
        for key, val in vid.items():
            if key == 0:
                self.bot.sendVideo(self.chat_id, video=open(val, 'rb'), caption='Motion Detected')
            else:
                self.bot.sendMessage(self.chat_id, val)
