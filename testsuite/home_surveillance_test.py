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
        cls.home_sur = HomeSurveillance(camera=None, bot=None, motion_detector=None)

    def test_is_start(self):
        """Test after init:  is_start = False."""
        self.assertFalse(self.home_sur.is_start, "Error after __init__ is_start must return False")

    def test_loop_is_run(self):
        """Test after init:  loop_is_run -> True"""
        self.assertTrue(self.home_sur.loop_is_run, "Error after __init__ loop_is_run must return True")

    def test_start(self):
        """Test start."""
        self.home_sur.start()
        self.assertTrue(self.home_sur.is_start, "Method start() doesn't work!")

    def test_stop(self):
        """Test stop."""
        self.home_sur.stop()
        self.assertFalse(self.home_sur.is_start, "Method stop() doesn't work!")


if __name__ == '__main__':
    unittest.main()
