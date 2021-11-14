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
        self.assertFalse(self.app.is_start, "Error the attribute \"is_start\" must be to False at instantiation")

    def test_is_interrupted(self):
        """Test after init:  interrupted -> True"""
        self.assertTrue(self.app.is_interrupted, "Error the attribute \"interrupted\" must be to True at instantiation")

    def test_start(self):
        """Test start."""
        self.app.start()
        self.assertTrue(self.app.is_start, "Method start() doesn't work!")

    def test_stop(self):
        """Test stop."""
        self.app.stop()
        self.assertFalse(self.app.is_start, "Method stop() doesn't work!")


if __name__ == '__main__':
    unittest.main()
