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

    def send_message(self, text):
        """
        Send message to your chat_id.

        :param text: message as string
        """
        self.__bot.send_message(chat_id=self.__chat_id, text=text)

    def send_video(self, video):
        """
        Send video to your chat_id.

        :param video: video file open in 'rb'
        """
        self.__bot.send_video(chat_id=self.__chat_id, video=video)

    def send_photo(self, photo, caption):
        """
        Send video to your chat_id.

        :param photo: video file open in 'rb'
        :param caption: message as string
        """
        self.__bot.send_photo(chat_id=self.__chat_id, photo=photo, caption=caption)
