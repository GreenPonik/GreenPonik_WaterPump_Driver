# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
from time import sleep

from GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver import (
    I2C_REGISTER,
    I2C_DEVICES_TYPE,
    i2c_scanner,
    read_byte_data,
    read_block_data,
    pump_run,
    ON,
    OFF,
)


class TestGreenPonik_WaterPump_Driver(unittest.TestCase):
    def test_i2c_scanner(self):
        devices = i2c_scanner()
        self.assertTrue(self, len(devices) > 0)
        self.assertTrue(self, type(devices).__name__ == "list")

    def test_read_byte_data(self):
        for device in i2c_scanner():
            self.assertTrue(
                self,
                I2C_DEVICES_TYPE["WATERPUMP"]
                == read_byte_data(device, I2C_REGISTER["TYPE"]),
            )
            sleep(0.2)

    def test_read_block_data(self):
        for device in i2c_scanner():
            if I2C_DEVICES_TYPE["WATERPUMP"] == read_byte_data(
                device, I2C_REGISTER["TYPE"]
            ):
                UUID = read_block_data(device, I2C_REGISTER["UUID"])
                print(UUID)
                print(len(UUID))
                self.assertTrue(
                    self, type(UUID).__name__ == "list",
                )
                self.assertTrue(self, len(UUID) == 8)
            sleep(0.2)

    def test_pump_run(self):
        for device in i2c_scanner():
            if I2C_DEVICES_TYPE["WATERPUMP"] == read_byte_data(
                device, I2C_REGISTER["TYPE"]
            ):
                pump_run(device, I2C_REGISTER["PUMP_1_STATE"], ON)
                sleep(10)
                pump_run(device, I2C_REGISTER["PUMP_1_STATE"], OFF)
            sleep(0.2)


if __name__ == "__main__":
    unittest.main()
