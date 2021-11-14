#!/usr/bin/env python
"""Testing Bot"""
import unittest
import site

site.addsitedir('..')
from lib.home_surveillance import HomeSurveillance


class TestHomeSurveillance(unittest.TestCase):
    """Test HomeSurveillance class"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = HomeSurveillance()

    def test_is_start(self):
        """Test after init:  is_start -> False."""
        is_start = self.app.is_start
        self.assertFalse(is_start, F"The attribute \"is_start\" must be to False instead of {is_start}")

    def test_is_interrupted(self):
        """Test after init:  interrupted -> True"""
        is_interrupted = self.app.is_interrupted
        self.assertTrue(is_interrupted, F"The attribute \"interrupted\" must be to True instead of {is_interrupted}")

    def test_start(self):
        """Test start."""
        start = self.app.start()
        self.assertTrue(start, F"Method start() must return True instead of {start}")

    def test_stop(self):
        """Test stop."""
        stop = self.app.stop()
        self.assertFalse(stop, F"Method stop() must return True instead of {stop}")


if __name__ == '__main__':
    unittest.main()
