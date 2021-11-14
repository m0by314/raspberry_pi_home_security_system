#!/usr/bin/env python
""" Testing for Pir package """
import unittest
import site

site.addsitedir('..')
from lib.pir import motion_detected


class TestPir(unittest.TestCase):
    """Test for the Pir function"""

    def test_motion_detected(self):
        """Test function movement_detected()"""
        motion = motion_detected()
        self.assertFalse(motion, F"Function motion_detected() must be return False instead of {motion}")


if __name__ == '__main__':
    unittest.main()
