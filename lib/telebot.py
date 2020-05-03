"""
Module Telebot
"""
import collections
import telepot


class Telebot(telepot.Bot):
    """
    The Telebot class use a telepot bot.
    The management of the bot is done through the handle decorator
        Example:
            @bot.handle("/start")
            def start_listen():
                bot.is_listen = True
                return str("Bot is listening")


            @bot.handle("/stop")
            def stop_listen():
                 bot.is_listen = False
                 return str("Bot isn't listening")

    :param bot_id : the bot's token
    """

    def __init__(self, bot_id):
        super().__init__(bot_id)
        self._handle = collections.defaultdict(list)
        self.message_loop(self._postreceive)
        self.chat_id = None
        self.command = None
        self._islisten = False

    @property
    def is_listen(self):
        """
        Return bot status
        """
        return self._islisten

    @is_listen.setter
    def is_listen(self, status):
        self._islisten = status

    def handler(self, cmd):
        """
        Decorator to create the bot commands
        Add commands as a function in a dictionary

        :param cmd: the command name
        :return decorator:
        """

        def decorator(func):
            print(cmd)
            self._handle[cmd].append(func)
            return func

        return decorator

    def _postreceive(self, msg):
        """
        callback from telepot.message_loop

        :param msg: message received
        """
        self.chat_id = msg['chat']['id']
        self.command = msg['text']

        for handle in self._handle.get(self.command, []):
            handle()
            return 0
        return 1

    def sendPhoto(self, file, msg):
        """
        Method for send photo
        :param file: photo to send
        :param msg:
        :return:
        """
        super().sendPhoto(self.chat_id, photo=open(file, 'rb'), caption=msg)

    def sendMessage(self, msg):
        """

        :param msg:
        :return:
        """
        super().sendMessage(self.chat_id, msg)

    def sendVideo(self, video, msg):
        """
        Send the video if there are no errors in the recording, otherwise send the error message.

        :param video: a dictionary containing the name of the video,
                      the return code of the recording
                      and the error message if recording fail
        :param msg:
        """
        if video["return_code"] == 0:
            super().sendVideo(self.chat_id, video=open(video["name"], 'rb'), caption=msg)
        else:
            super().sendMessage(self.chat_id, video["return_code"])
