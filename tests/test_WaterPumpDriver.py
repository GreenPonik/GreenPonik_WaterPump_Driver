# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from unittest.mock import patch


class FcntlMock:
    def ioctl():
        # simulate ioctl for tests only
        pass


class BoardMock:
    def __init__(self):
        self._scl = 18
        self._sda = 15

    def SCL(self):
        return self._scl

    def SDA(self):
        return self._sda


class BusioMock:
    def I2C(self, sda, scl):
        return True


sys.modules["fcntl"] = FcntlMock()
sys.modules["board"] = BoardMock()
sys.modules["busio"] = BusioMock()

from GreenPonik_WaterPump_Driver.WaterPumpDriver import WaterPumpDriver


class TestWaterPumpDriver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_i2c_scanner(self, mock):
        d = mock()
        expected = [i for i in range(20, 101)]
        d.scan.return_value = expected
        devices = d.scan()
        self.assertIsNotNone(devices)
        self.assertTrue(len(devices) > 0)
        self.assertTrue(type(devices).__name__ == "list")

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_read(self, mock):
        d = mock()
        d.read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        devices = WaterPumpDriver.i2c_scanner()
        self.assertIsNotNone(devices)
        deviceType = d.read(devices[0], WaterPumpDriver.I2C_REGISTERS["TYPE"])
        self.assertIsNotNone(deviceType)
        self.assertTrue(type(deviceType).__name__ == "int")
        self.assertTrue(deviceType == WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"])

    # @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    # def test_read(self, mock):
    #     d = mock()
    #     d.read.return_value = [55, 89, 63, 35, 54, 21, 25, 47]
    #     devices = WaterPumpDriver.i2c_scanner(self)
    #     self.assertIsNotNone(self, devices)
    #     b = bytearray(8)
    #     UUID = (d.read(devices[0], WaterPumpDriver.I2C_REGISTERS["UUID"], b),)
    #     self.assertIsNotNone(self, UUID)
    #     self.assertTrue(
    #         self, type(UUID).__name__ == "list",
    #     )
    #     self.assertTrue(self, len(UUID) == 8)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver")
    def test_pump_run(self, mock):
        d = mock()
        d.read.return_value = WaterPumpDriver.I2C_DEVICES_TYPE["WATERPUMP"]
        devices = WaterPumpDriver.i2c_scanner()
        self.assertIsNotNone(devices)
        d.pump_run(
            devices[0],
            WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"],
            WaterPumpDriver.I2C_COMMANDS["ON"],
        )
        self.assertTrue(
            WaterPumpDriver.read(
                devices[0], WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"]
            )
            == WaterPumpDriver.I2C_COMMANDS["ON"],
        )
        d.pump_run(
            devices[0],
            WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"],
            WaterPumpDriver.I2C_COMMANDS["OFF"],
        )
        self.assertTrue(
            WaterPumpDriver.read(
                devices[0], WaterPumpDriver.I2C_REGISTERS["PUMP_1_STATE"]
            )
            == WaterPumpDriver.I2C_COMMANDS["OFF"],
        )


if __name__ == "__main__":
    unittest.main()
