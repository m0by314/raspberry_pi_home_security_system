"""SenderBot interface"""


class SenderBot:
    """
    Interface with Telegram bot, for send message and video only to your chat_id

    :param bot: Telegram bot instance
    :param chat_id: Your chat_id
    """
    def __init__(self, bot, chat_id):
        self.__bot = bot
        self.__chat_id = chat_id

    def send_message(self, msg):
        """
        Send message to your chat_id.

        :param msg: message as string
        """
        self.__bot(chat_id=self.__chat_id, text=msg)

    def send_video(self, video_rb):
        """
        Send video to your chat_id.

        :param video_rb: video file open in 'rb'
        """
        self.__bot(chat_id=self.__chat_id, video=video_rb)
