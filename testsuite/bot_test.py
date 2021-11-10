#!/usr/bin/env python
"""Testing Bot"""
import unittest
import sys
import site
import telegram

from config import TOKEN_ID, CHAT_ID

site.addsitedir('..')
from lib.bot import SenderBot


if TOKEN_ID == 'Your_token_id':
    print("Your token_id is not defined in config.py")
    sys.exit(1)

telegram_bot = telegram.Bot(TOKEN_ID)


class TestSenderBotMethods(unittest.TestCase):
    """Test Bot"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.bot = SenderBot(telegram_bot, CHAT_ID)

    def test_send_message(self):
        """Test send message."""
        try:
            self.bot.send_message(text="Testsuite")
        except Exception as err:
            self.fail(err)

    def test_send_photo(self):
        """Test send photo."""
        with open("testsuite/logo-ok.png", 'rb') as logo:
            try:
                self.bot.send_photo(photo=logo, text="testsuite")
            except Exception as err:
                self.fail(err)


if __name__ == '__main__':
    unittest.main()
