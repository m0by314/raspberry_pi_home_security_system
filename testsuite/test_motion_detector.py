#!/usr/bin/env python
import unittest

import requests
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('..') + '/lib')

from lib.telebot import Telebot
from lib.config import bot_id


if os.path.isfile('data.raw'):
    with open('data.raw') as fp:
        chat_id = fp.read()
else:
    chat_id = requests.get("https://api.telegram.org/bot{TOKEN}/getUpdates".format(TOKEN=bot_id)) \
        .json()['result'][0]['message']['chat']['id']
    with open('data.raw', 'w') as fp:
        fp.write(str(chat_id))
fp.close()


class TestBotMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.response = requests.get("https://api.telegram.org/bot{TOKEN}/getMe".format(TOKEN=bot_id))
        cls.bot = Telebot(bot_id)

    def test_query_url(self):
        self.assertEqual(self.response.status_code, 200, "Error: query url Telegram API Bot fail")

    def test_bot_query(self):
        self.assertEqual(self.bot.getMe(), self.response.json()['result'], "Error: bot query fail")

    def test_bot_status(self):
        self.assertEqual(self.bot.is_listen, 0, "Error: Bot is listen")

    def test_set_start(self):
        self.bot.is_listen = True
        self.assertEqual(self.bot.is_listen, 1, "Error: setter Bot.is_listen")

    def test_set_stop(self):
        self.bot.is_listen = False
        self.assertEqual(self.bot.is_listen, 0, "Error: setter Bot.is_listen")

    def test_handle(self):
        @self.bot.handler("/testsuite")
        def on_tests():
            return str("Test handler")

        msg = {'message_id': 305, 'chat': {'id': chat_id, 'first_name': 'test', 'last_name': 'test', 'type': 'private'},
               'date': 1586725459, 'text': '/testsuite', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._postreceive(msg), 0, "Error: Handler")

    def test_handler_photo(self):
        @self.bot.handler("/photo")
        def on_test_photo():
            return 'logo-ok.png'

        msg = {'message_id': 305, 'chat': {'id': chat_id, 'first_name': 'test', 'last_name': 'test', 'type': 'private'},
               'date': 1586725459, 'text': '/photo',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._postreceive(msg), 0, "Error: Handler")



if __name__ == '__main__':
    unittest.main()
