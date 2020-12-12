"""
Package to create a telegram bot with the telepot module
"""
import collections
import telepot


class Telebot(telepot.Bot):
    """
    The Telebot class use a telepot bot.

    The management of the bot's command is done through the handle decorator
        Example:
            @bot.handler("/start")
            def on_start():
                bot.is_listen = True
                return bot.sendMessage("Bot start")

            @bot.handler("/photo")
            def on_photo():
                return bot.sendPhoto(camera.take_photo(), "photo")

    Commands can contain arguments arg=value (takes into account only words or numbers)
        Example for the command /hello arg=world:
            @bot.handler("/hello")
                def on_video(*args):
                return bot.send_message("Hello " + args[0])

    :param token_id : the token id
    :param chat_id : your chat_id
    """

    def __init__(self, token_id, chat_id):
        super().__init__(token_id)
        self._handle = collections.defaultdict(list)
        self.message_loop(self._postreceive)
        self.chat_id = chat_id
        self.command = None
        self._is_listen = False

    @property
    def is_listen(self):
        """
        Bot status

        :return: boolean
        """
        return bool(self._is_listen)

    @is_listen.setter
    def is_listen(self, status):
        self._is_listen = status

    def handler(self, cmd):
        """
        Decorator to create the bot commands
        Add commands as a function in a dictionary

        :param cmd: command name
        """

        def decorator(func):
            self._handle[cmd].append(func)
            return func

        return decorator

    def _get_args(self):
        """
        retrieves the arguments of the command

        :return: tuples arguments
        """
        args = self.command.split()
        self.command = args[0]
        return tuple(args[1:])

    def _authorized_chat_id(self, incoming_chat_id):
        """
        check that the incoming chat_id is authorized
        :param incoming_chat_id: the incoming chat id
        :return: boolean
        """
        return bool(int(self.chat_id) == int(incoming_chat_id))

    def _postreceive(self, msg):
        """
        Callback for :attr message_loop()

        :param msg: message received
        """
        incoming_chat_id = msg['chat']['id']
        self.command = msg['text']
        if self._authorized_chat_id(incoming_chat_id):
            args = self._get_args()
            for handle in self._handle.get(self.command, []):
                return handle(*args)
        return None

    def send_photo(self, file, msg):
        """
        Encapsulates the sendPhoto method

        :param file: photo to send
        :param msg: picture title
        """
        with open(file, 'rb') as photo_file:
            self.sendPhoto(self.chat_id, photo=photo_file, caption=msg)

    def send_message(self, msg):
        """
        Encapsulates the sendMessage method

        :param msg: message to send
        """
        self.sendMessage(self.chat_id, str(msg))

    def send_video(self, video, msg):
        """
        Send the video if there are no errors in the recording, otherwise send the error message.

        :param video: a dictionary containing the name of the video,
                      the return code of the recording
                      and the error message if recording fail
        :param msg: video title
        """
        if video["return_code"] is None:
            with open(video["name"], 'rb') as video_file:
                super().sendVideo(self.chat_id, video=video_file, caption=msg)
        else:
            super().sendMessage(self.chat_id, video["return_code"])
