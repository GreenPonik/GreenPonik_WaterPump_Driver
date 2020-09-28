# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import unittest
from unittest.mock import patch


class FcntlMock:
    def ioctl(self):
        # simulate ioctl for tests only
        pass


sys.modules["fcntl"] = FcntlMock()


class TestWaterPumpDriver(unittest.TestCase):
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
        expected = ''.join(map(str, list_from_i2c))
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
