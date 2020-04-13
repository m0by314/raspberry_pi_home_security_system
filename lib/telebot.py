import telepot
import collections


class Telebot(telepot.Bot):
    """
    The Telepot object use a telepot bot.
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
        return self._islisten

    @is_listen.setter
    def is_listen(self, status):
        self._islisten = status

    def handler(self, rule):
        """
        Decorator to create the bot commands
        Add commands as a function in a dictionary

        :param rule: The rule this handle will created
        :return decorator:
        """

        def decorator(func):
            self._handle[rule].append(func)
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
            if "photo" in self.command:
                self.sendPhoto(self.chat_id, photo=open(handle(), 'rb'), caption='photo')
            else:
                self.sendMessage(self.chat_id, handle())
            return 0
        return 1

    def send_video(self, video):
        """
        Send the video if there are no errors in the recording, otherwise send the error message.

        :param video: a dictionary containing the name of the video,
                                the return code of the recording
                                and the error message if recording fail
        """
        if video["return_code"] == 0:
            self.sendVideo(self.chat_id, video=open(video["name"], 'rb'), caption='Motion Detected')
        else:
            self.sendMessage(self.chat_id, video["return_code"])
