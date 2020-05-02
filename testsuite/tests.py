#!/usr/bin/env python3
"""
Testing bot module
"""
import unittest
import sys
import os
import requests

sys.path.insert(0, os.getcwd())

from lib.telebot import Telebot
from lib.config import TOKEN_ID, REGISTRATION_FOLDER

if TOKEN_ID == 'Your_token_id' or not os.path.exists(REGISTRATION_FOLDER):
    print("Variables bot_id or registration_folder are not defined in lib/config.py")
    sys.exit(1)


class TestBotMethods(unittest.TestCase):
    """
    Test for the Telebot class
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize Telebot
        Query Telegram API
        Get chat_id and write in data.raw
        """
        cls.bot = Telebot(TOKEN_ID)
        cls.response = requests.get("https://api.telegram.org/bot{TOKEN}/getMe"
                                    .format(TOKEN=TOKEN_ID))
        data = os.getcwd() + 'data.raw'
        if os.path.isfile(data):
            with open(data) as file:
                cls.chat_id = file.read()
        else:
            cls.chat_id = requests.get("https://api.telegram.org/bot{TOKEN}/getUpdates"
                                       .format(TOKEN=TOKEN_ID)) \
                .json()['result'][0]['message']['chat']['id']
            with open(data, 'w') as file:
                file.write(str(cls.chat_id))
        file.close()

    def test_query_url(self):
        """
        Test query Telegram API Bot
        """
        self.assertEqual(self.response.status_code, 200, "Cannot query url Telegram API Bot fail")

    def test_bot_query(self):
        """
        Test to query Telegram API with the method bot.getMe()
        :return:
        """
        self.assertEqual(self.bot.getMe(), self.response.json()['result'],
                         "The response of the Telebot class and the Telegram url differs")

    def test_bot_status(self):
        """
        Test method bot.is_listen
        """
        self.assertEqual(self.bot.is_listen, 0, "Bot is listen")

    def test_set_start(self):
        """
        Test setter bot.is_listen start
        """
        self.bot.is_listen = True
        self.assertEqual(self.bot.is_listen, 1, "Cannot set Bot.is_listen to ON")

    def test_set_stop(self):
        """
        Test setter bot.is_listen stop
        :return:
        """
        self.bot.is_listen = False
        self.assertEqual(self.bot.is_listen, 0, "Cannot set Bot.is_listen to OFF")

    def test_handle(self):
        """
        Test handler
        """

        @self.bot.handler("/testsuite")
        def on_test():
            return str("Test handler")

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459,
               'text': '/testsuite',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._postreceive(msg), 0, "Handler doesn't function")

    def test_handler_photo(self):
        """
        Test handler photo
        """

        @self.bot.handler("/photo")
        def on_test_photo():
            return 'testsuite/logo-ok.png'

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459, 'text': '/photo',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._postreceive(msg), 0, "Handler photo doesn't function")


if __name__ == '__main__':
    unittest.main()
