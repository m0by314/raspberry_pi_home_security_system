#!/usr/bin/env python
"""
Testing for telebot package.
"""
import unittest
import sys
import os


sys.path.insert(0, os.getcwd())

from lib.telebot import Telebot
from lib.config import TOKEN_ID, REGISTRATION_FOLDER, CHAT_ID

if TOKEN_ID == 'Your_token_id' or not os.path.exists(REGISTRATION_FOLDER):
    print("Variables bot_id or registration_folder are not defined in lib/config.py")
    sys.exit(1)


class TestBotMethods(unittest.TestCase):
    """
    Test for the Telebot class
    """

    @classmethod
    def setUpClass(cls):
        cls.bot = Telebot(TOKEN_ID, CHAT_ID)
        cls.chat_id = CHAT_ID

    def authorised(self):
        """
        Checks if the bot accepts other chats_id than the authorized one
        """
        self.assertEqual(self.bot._authorized_chat_id(18545452), False, "The method self.bot._authorized_chat_id "
                                                                        "doesn't work")

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
        """
        self.bot.is_listen = False
        self.assertEqual(self.bot.is_listen, 0, "Cannot set Bot.is_listen to OFF")

    def test_handler(self):
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

        self.assertEqual(self.bot._postreceive(msg), "Test handler", "Handler doesn't function")

    def test_send_message(self):
        """
        Test send message
        """

        @self.bot.handler("/message")
        def on_test():
            return self.bot.send_message("Test send message")

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459,
               'text': '/message',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}

        self.assertEqual(self.bot._postreceive(msg), None, "Send message doesn't function")

    def test_handler_photo(self):
        """
        Test send photo
        """

        @self.bot.handler("/photo")
        def on_test_photo():
            return self.bot.send_photo('testsuite/logo-ok.png', "Testsuite")

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459, 'text': '/photo',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}

        self.assertEqual(self.bot._postreceive(msg), None, "Send photo doesn't function")


if __name__ == '__main__':
    unittest.main()
