# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from GreenPonik_WaterPump_Driver.unpacker import Unpacker


class TestPacker(unittest.TestCase):
    def test_unpacker(self):
        value_to_unpack = [2, 6, 12, 1, 19, 4]
        unpacker = Unpacker()
        unpacker.write(value_to_unpack)
        unpacked = unpacker.read()
        expected = [12, 1]
        self.assertIsNotNone(unpacked)
        self.assertTrue(type(unpacked).__name__ == "list")
        self.assertEqual(expected, unpacked)


if __name__ == "__main__":
    unittest.main()
