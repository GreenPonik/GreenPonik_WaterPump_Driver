# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from unittest.mock import patch

I2C_REGISTERS = {
    "TYPE": 0x00,  # i2c Read Only
    "FIRMWARE": 0x01,  # i2c Read Only
    "UUID": 0x02,  # i2c Read Only
    "I2C_ADDRESS": 0x03,  # i2c Read / Write
    "LED_ACTIVATION": 0x04,  # i2c Read / Write
    "WATER_PUMP_STATE": 0x05,  # i2c Read / Write
    "PUMP_1_STATE": 0x06,  # i2c Read / Write
    "PUMP_2_STATE": 0x07,  # i2c Read / Write
    "PUMP_3_STATE": 0x08,  # i2c Read / Write
    "PUMP_4_STATE": 0x09,  # i2c Read / Write
    "ALL": 0x20,  # i2c Read
}


class FcntlMock:
    def ioctl(self):
        # simulate ioctl for tests only
        pass


sys.modules["fcntl"] = FcntlMock()


class TestWaterPumpDriver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.WaterPumpDriver")
    def test_get_all(self, mock):
        d = mock()
        registers = I2C_REGISTERS
        registers.pop("ALL", 0x20)
        expected = [r for k, r in I2C_REGISTERS.items()]
        d.get_all.return_value = expected
        device_get_all = d.get_all()
        self.assertIsNotNone(device_get_all)
        self.assertTrue(type(device_get_all) is list)
        self.assertEqual(expected, device_get_all)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.WaterPumpDriver")
    def test_get_type(self, mock):
        d = mock()
        expected = 1
        d.get_type.return_value = expected
        device_type = d.get_type()
        self.assertIsNotNone(device_type)
        self.assertTrue(type(device_type) is int)
        self.assertEqual(expected, device_type)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.WaterPumpDriver")
    def test_get_uuid(self, mock):
        d = mock()
        list_from_i2c = [0, 0, 204, 80, 227, 181, 155, 20]
        expected = "".join(map(str, list_from_i2c))
        d.get_uuid.return_value = expected
        uuid = d.get_uuid()
        self.assertIsNotNone(uuid)
        self.assertTrue(type(uuid) is str)
        self.assertEqual(expected, uuid)

    @patch("GreenPonik_WaterPump_Driver.WaterPumpDriver.WaterPumpDriver")
    def test_on_off_pump(self, mock):
        d = mock()
        register = d.I2C_REGISTERS["PUMP_1_STATE"]

        # start pump
        d.pump_run(register, d.I2C_COMMANDS["ON"])

        # get pump ON
        expected_run = d.I2C_COMMANDS["ON"]
        d.read.return_value = expected_run
        p_state = d.read(register)
        self.assertTrue(expected_run == p_state)

        # stop pump
        d.pump_run(register, d.I2C_COMMANDS["OFF"])

        # get pump OFF
        expected_stop = d.I2C_COMMANDS["OFF"]
        d.read.return_value = expected_stop
        p_state = d.read(register)
        self.assertTrue(expected_stop == p_state)


if __name__ == "__main__":
    unittest.main()
