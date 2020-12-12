#!/usr/bin/env python
"""
Testing for camera package
"""
import unittest
import os
import site

site.addsitedir('..')
from lib.camera import Camera
from config import REGISTRATION_FOLDER


class TestCamera(unittest.TestCase):
    """
    Test for the Camera class
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize camera
        """
        cls.camera = Camera(REGISTRATION_FOLDER)

    def setUp(self) -> None:
        """
        Create file in REGISTRATION_FOLDER
        """
        testfile = os.path.join(os.path.abspath(REGISTRATION_FOLDER), "test.txt")
        open(testfile, 'a').close()

    def test_recording(self):
        """
        Test method camera.start_recording()
        """
        video = self.camera.start_recording(10)
        self.assertEqual(video["return_code"], None,
                         "ERROR: during recording video[\"return_code\"]")

    def test_take_photo(self):
        """
        Test method camera.take_photo()
        """
        photo = self.camera.take_photo()
        self.assertTrue(os.path.isfile(photo))

    def test_purge_folder(self):
        """
        Test method camera.purge_records()
        """
        self.assertEqual(self.camera.purge_records(),
                         'The records have been deleted',
                         "purge_record doesn't function")


if __name__ == '__main__':
    unittest.main()
