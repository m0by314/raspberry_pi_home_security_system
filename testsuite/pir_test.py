#!/usr/bin/env python
""" Testing for Pir package """
import unittest
import site

site.addsitedir('..')
from lib.pir import movement_detected


class TestPir(unittest.TestCase):
    """ Test for the Pir function """

    def test_movement_detected(self):
        """ Test function movement_detected() """
        self.assertFalse(movement_detected())


if __name__ == '__main__':
    unittest.main()
