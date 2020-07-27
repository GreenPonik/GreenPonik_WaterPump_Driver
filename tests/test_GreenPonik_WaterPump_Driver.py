# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver import i2c_scanner, pump_on, pump_off


class TestGreenPonik_WaterPump_Driver(unittest.TestCase):

    i2c_slaves = i2c_scanner()
    

    def test_pump_on(self):
        self.assertListEqual(pump_on())

    
    def test_pump_off(self):
        self.assertListEqual(pump_off())


if __name__ == '__main__':
    unittest.main()
