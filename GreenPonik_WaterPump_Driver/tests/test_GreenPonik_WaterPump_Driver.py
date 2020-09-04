# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from unittest.mock import patch, MagicMock


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
    WaterPumpDriver
)


class Test_GreenPonik_WaterPump_Driver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_i2c_scanner(self, Mock):
        d = Mock()
        expected = [i for i in range(20, 101)]
        d.scan.return_value = expected
        devices = d.scan()
        self.assertIsNotNone(self, devices)
        self.assertTrue(self, len(devices) > 0)
        self.assertTrue(self, type(devices).__name__ == "list")

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_read_byte_data(self, Mock):
        d = Mock()
        d.read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        deviceType = d.read(devices[0], WaterPumpDriver.I2C_REGISTERS["TYPE"])
        self.assertIsNotNone(self, deviceType)
        self.assertTrue(self, type(deviceType).__name__ == "int")
        self.assertTrue(
            self, deviceType == WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        )

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_read_block_data(self, Mock):
        d = Mock()
        d.read.return_value = [55, 89, 63, 35, 54, 21, 25, 47]
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        b = bytearray(8)
        UUID = (d.read(devices[0], WaterPumpDriver.I2C_REGISTERS["UUID"], b),)
        self.assertIsNotNone(self, UUID)
        self.assertTrue(
            self, type(UUID).__name__ == "list",
        )
        self.assertTrue(self, len(UUID) == 8)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_pump_run(self, Mock):
        d = Mock()
        d.read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        d.pump_run(
            devices[0],
            WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"],
            WaterPumpDriver.I2C_COMMANDS["ON"],
        )
        b = bytearray(1)
        self.assertTrue(
            self,
            WaterPumpDriver.read_byte_data(
                devices[0], WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"], b
            )
            == WaterPumpDriver.I2C_COMMANDS["ON"],
        )
        d.pump_run(
            devices[0],
            WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"],
            WaterPumpDriver.I2C_COMMANDS["OFF"],
        )
        self.assertTrue(
            self,
            WaterPumpDriver.read_byte_data(
                devices[0], WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"], b
            )
            == WaterPumpDriver.I2C_COMMANDS["OFF"],
        )


if __name__ == "__main__":
    unittest.main()
