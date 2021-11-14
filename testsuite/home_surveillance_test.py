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
        self.assertFalse(self.app.is_start, F"The attribute \"is_start\" must be to False instead of {self.app.is_start}")

    def test_is_interrupted(self):
        """Test after init:  interrupted -> True"""
        self.app.is_interrupted
        self.assertFalse(self.app.is_interrupted, F"The attribute \"interrupted\" must be to False instead of {self.app.is_interrupted}")

    def test_signal_handler(self):
        """test signal handler method."""
        self.app._signal_handler()
        self.assertTrue(self.app.is_interrupted, F"Method _signal_handler() must be return True instead of {self.app.is_interrupted}")

    def test_start(self):
        """Test start."""
        self.app.start()
        self.assertTrue(self.app.is_start, F"Method start() must return True instead of {self.app.is_start}")

    def test_stop(self):
        """Test stop."""
        self.app.stop()
        self.assertFalse(self.app.is_start, F"Method stop() must return True instead of {self.app.is_start}")


if __name__ == '__main__':
    unittest.main()
