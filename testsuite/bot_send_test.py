#!/usr/bin/env python
"""Testing Bot"""
import unittest
import sys
import telegram

from config import TOKEN_ID, CHAT_ID

if TOKEN_ID == 'Your_token_id':
    print("Your token_id is not defined in config.py")
    sys.exit(1)


class TestBotMethods(unittest.TestCase):
    """Test Bot"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.bot = telegram.Bot(TOKEN_ID)
        cls.chat_id = CHAT_ID

    def test_send_message(self):
        """Test send message."""
        try:
            self.bot.send_message(chat_id=CHAT_ID, text="Testsuite")
        except Exception as err:
            self.fail(err)

    def test_handler_photo(self):
        """Test send photo."""
        with open("testsuite/logo-ok.png", 'rb') as logo:
            try:
                self.bot.send_photo(chat_id=CHAT_ID, photo=logo, caption="testsuite")
            except Exception as err:
                self.fail(err)


if __name__ == '__main__':
    unittest.main()