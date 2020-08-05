# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from time import sleep
import unittest
from unittest.mock import patch, MagicMock
import sys


class BoardMock:
    def __init__(self):
        self._scl = 18
        self._sda = 15

    def SCL(self):
        return self._scl

    def SDA(self):
        return self._sda


class BusioMock(MagicMock()):
    def I2C(self, sda, scl):
        return True


sys.modules["board"] = BoardMock()
sys.modules["busio"] = BusioMock()


from GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver import (
    I2C_REGISTERS,
    I2C_DEVICES_TYPE,
    i2c_scanner,
    read_byte_data,
    pump_run,
    ON,
    OFF,
)


class TestGreenPonik_WaterPump_Driver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.i2c_scanner")
    def test_i2c_scanner(self, MockScan):
        scan = MockScan()
        expected = [i for i in range(20, 101)]
        scan.return_value = expected
        devices = scan()
        self.assertIsNotNone(self, devices)
        self.assertTrue(self, len(devices) > 0)
        self.assertTrue(self, type(devices).__name__ == "list")

    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.read_byte_data")
    def test_read_byte_data(self, MockRead):
        read = MockRead()
        read.return_value = I2C_DEVICES_TYPE["WATERPUMP"]
        devices = i2c_scanner()
        self.assertIsNotNone(self, devices)
        deviceType = read(devices[0], I2C_REGISTERS["TYPE"])
        self.assertIsNotNone(self, deviceType)
        self.assertTrue(self, type(deviceType).__name__ == "int")
        self.assertTrue(self, deviceType == I2C_DEVICES_TYPE["WATERPUMP"])

    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.read_byte_data")
    def test_read_block_data(self, MockRead):
        read = MockRead()
        read.return_value = [55, 89, 63, 35, 54, 21, 25, 47]
        devices = i2c_scanner()
        self.assertIsNotNone(self, devices)
        b = bytearray(8)
        UUID = (read(devices[0], I2C_REGISTERS["UUID"], b),)
        self.assertIsNotNone(self, UUID)
        self.assertTrue(
            self, type(UUID).__name__ == "list",
        )
        self.assertTrue(self, len(UUID) == 8)

    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.read_byte_data")
    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.pump_run")
    def test_pump_run(self, MockRead, MockRun):
        read = MockRead()
        read.return_value = I2C_DEVICES_TYPE["WATERPUMP"]
        r = MockRun()
        devices = i2c_scanner()
        self.assertIsNotNone(self, devices)
        r(devices[0], I2C_REGISTERS["PUMP_1_STATE"], ON)
        b = bytearray(1)
        self.assertTrue(
            self, read_byte_data(devices[0], I2C_REGISTERS["PUMP_1_STATE"], b) == ON
        )
        r(devices[0], I2C_REGISTERS["PUMP_1_STATE"], OFF)
        self.assertTrue(
            self, read_byte_data(devices[0], I2C_REGISTERS["PUMP_1_STATE"], b) == OFF
        )


if __name__ == "__main__":
    unittest.main()
