# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
from unittest.mock import patch, MagicMock
import sys
import os


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


from GreenPonik_WaterPump_Driver import WaterPumpDriver


class TestGreenPonik_WaterPump_Driver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.i2c_scanner")
    def test_i2c_scanner(self, MockScan):
        scan = MockScan()
        expected = [i for i in range(20, 101)]
        scan.return_value = expected
        devices = scan()
        self.assertIsNotNone(self, devices)
        self.assertTrue(self, len(devices) > 0)
        self.assertTrue(self, type(devices).__name__ == "list")

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.read_byte_data")
    def test_read_byte_data(self, MockRead):
        read = MockRead()
        read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        deviceType = read(devices[0], WaterPumpDriver.I2C_REGISTERS["TYPE"])
        self.assertIsNotNone(self, deviceType)
        self.assertTrue(self, type(deviceType).__name__ == "int")
        self.assertTrue(
            self, deviceType == WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        )

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.read_byte_data")
    def test_read_block_data(self, MockRead):
        read = MockRead()
        read.return_value = [55, 89, 63, 35, 54, 21, 25, 47]
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        b = bytearray(8)
        UUID = (read(devices[0], WaterPumpDriver.I2C_REGISTERS["UUID"], b),)
        self.assertIsNotNone(self, UUID)
        self.assertTrue(
            self, type(UUID).__name__ == "list",
        )
        self.assertTrue(self, len(UUID) == 8)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.read_byte_data")
    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.pump_run")
    def test_pump_run(self, MockRead, MockRun):
        read = MockRead()
        read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        r = MockRun()
        devices = WaterPumpDriver.i2c_scanner(self)
        self.assertIsNotNone(self, devices)
        r.pump_run(
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
        r.pump_run(
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
