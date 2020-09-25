# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from GreenPonik_WaterPump_Driver.crc8 import Crc8


class TestPacker(unittest.TestCase):
    def test_crc8(self):
        value_to_convert = [12, 1]
        crc8 = Crc8()
        _crc8 = crc8.calc(value_to_convert)
        expected = 19
        self.assertIsNotNone(_crc8)
        self.assertTrue(type(_crc8).__name__ == "int")
        self.assertEqual(expected, _crc8)


if __name__ == "__main__":
    unittest.main()
