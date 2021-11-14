#!/usr/bin/env python
""" Testing for camera package """
import unittest
import os
import site
from picamera import PiCamera

site.addsitedir('..')
from lib.camera import Camera

REGISTRATION_FOLDER = "testsuite/video"

pi_camera = PiCamera()


class TestCamera(unittest.TestCase):
    """ Test for the Camera class """

    @classmethod
    def setUpClass(cls):
        """Initialize camera"""
        cls.camera = Camera(pi_camera, REGISTRATION_FOLDER)

    def setUp(self) -> None:
        """Create file in REGISTRATION_FOLDER"""
        testfile = os.path.join(os.path.abspath(REGISTRATION_FOLDER), "test.txt")
        open(testfile, 'a').close()

    def tearDown(self) -> None:
        self.camera.purge_records()

    def test_recording(self):
        """Test method camera.start_recording()"""
        try:
            self.camera.start_recording(10)
        except OSError as err:
            self.fail(err)

    def test_take_photo(self):
        """Test method camera.take_photo()"""
        try:
            self.camera.take_photo()
        except Exception as err:
            self.fail(err)

    def test_purge_folder(self):
        """Test method camera.purge_records()"""
        try:
            self.camera.purge_records()
        except OSError as err:
            self.fail(err)


if __name__ == '__main__':
    unittest.main()
