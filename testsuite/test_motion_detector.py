#!/usr/bin/env python
import unittest

import requests
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('..') + '/lib')

from lib.telebot import Telebot
from lib.config import bot_id


class TestBotMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.response = requests.get("https://api.telegram.org/bot{TOKEN}/getMe".format(TOKEN=bot_id))
        cls.bot = Telebot(bot_id)

    def test_query_url(self):
        self.assertEqual(self.response.status_code, 200, "Error:  query Telegram API Bot fail")

    def test_bot_query(self):
        self.assertEqual(self.bot.getMe(), self.response.json()['result'], "Error: bot query fail")

    def test_bot_status(self):
        self.assertEqual(self.bot.is_listen, 0, "Error: Bot is listen")

    def test_set_start(self):
        self.bot.is_listen = True
        self.assertEqual(self.bot.is_listen, 1, "Error: setter Bot.is_listen")

    def test_set_start(self):
        self.bot.is_listen = False
        self.assertEqual(self.bot.is_listen, 0, "Error: setter Bot.is_listen")

    # TODO SEND msg et VIDEO et handle


if __name__ == '__main__':
    unittest.main()
