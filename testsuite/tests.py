#!/usr/bin/env python3
"""
Testing library
"""
import unittest
import sys
import os
import requests

sys.path.insert(0, os.getcwd())

from lib.telebot import Telebot
from lib.camera import Camera
from lib.pir import Motiondetector
from lib.config import BOT_ID, REGISTRATION_FOLDER


if BOT_ID == 'Your_token_id' or not os.path.exists(REGISTRATION_FOLDER):
    print("Variables bot_id or registration_folder are not defined in lib/config.py")
    sys.exit(1)


class TestBotMethods(unittest.TestCase):
    """
    Test for the Telebot class
    """
    @classmethod
    def setUpClass(cls):
        cls.response = requests.get("https://api.telegram.org/bot{TOKEN}/getMe"
                                    .format(TOKEN=BOT_ID))
        cls.bot = Telebot(BOT_ID)
        if os.path.isfile('data.raw'):
            with open('data.raw') as file:
                cls.chat_id = file.read()
        else:
            cls.chat_id = requests.get("https://api.telegram.org/bot{TOKEN}/getUpdates"
                                       .format(TOKEN=BOT_ID)) \
                                       .json()['result'][0]['message']['chat']['id']
            with open('data.raw', 'w') as file:
                file.write(str(cls.chat_id))
        file.close()

    def test_query_url(self):
        self.assertEqual(self.response.status_code, 200, "Cannot query url Telegram API Bot fail")

    def test_bot_query(self):
        self.assertEqual(self.bot.getMe(), self.response.json()['result'],
                         "The response of the Telebot class and the Telegram url differs")

    def test_bot_status(self):
        self.assertEqual(self.bot.is_listen, 0, "Bot is listen")

    def test_set_start(self):
        self.bot.is_listen = True
        self.assertEqual(self.bot.is_listen, 1, "Cannot set Bot.is_listen to ON")

    def test_set_stop(self):
        self.bot.is_listen = False
        self.assertEqual(self.bot.is_listen, 0, "Cannot set Bot.is_listen to OFF")

    def test_handle(self):
        @self.bot.handler("/testsuite")
        def on_tests():
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


class TestCamera(unittest.TestCase):
    """
    Test for the Camera class
    """
    @classmethod
    def setUpClass(cls):
        cls.camera = Camera(REGISTRATION_FOLDER, 10)

    def setUp(self) -> None:
        open(REGISTRATION_FOLDER + "tests.txt", 'a').close()

    def test_recording(self):
        video = self.camera.start_recording()
        self.assertEqual(video["return_code"], 0, "ERROR: during recording video[\"return_code\"]")

    def test_take_photo(self):
        photo = self.camera.take_photo()
        self.assertTrue(os.path.isfile(photo))

    def test_purge_folder(self):
        self.assertEqual(self.camera.purge_records(),
                         'The records have been deleted',
                         "purge_record doesn't function")


class TestPir(unittest.TestCase):
    """
    Test for the Pir class
    """
    @classmethod
    def setUpClass(cls):
        cls.pir = Motiondetector()

    def test_movement_detected(self):
        self.assertFalse(self.pir.movement_detected())


if __name__ == '__main__':
    unittest.main()
