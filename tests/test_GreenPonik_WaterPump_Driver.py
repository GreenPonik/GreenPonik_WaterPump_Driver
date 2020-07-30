# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from time import sleep
import unittest
from unittest.mock import patch, MagicMock

# MockRPi = MagicMock()
# modules = {
#     "board": MockRPi.board,
#     "busio": MockRPi.busio,
# }
# patcher = patch.dict("sys.modules", modules)


# def setUp():
#     patcher.start()


# def teardownModules():
#     patcher.stop()


class BoardMock:
    def __init__(self):
        self._scl = 18
        self._sda = 15

    def SCL(self):
        return self._scl

    def SDA(self):
        return self._sda


class BusioMock:
    def i2c(self, sda, scl):
        return True


class I2CMock:
    board = BoardMock()
    busio = BusioMock()

    def i2c_scanner(self):
        i2c = busio.i2c(board.SDA(), board.SCL())
        return [100]


modules = {
    "board": BoardMock(),
    "busio": BusioMock(),
}
patcher = patch.dict("sys.modules", modules)


from GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver import (
    #     I2C_REGISTERS,
    #     I2C_DEVICES_TYPE,
    i2c_scanner,
    #     read_byte_data,
    #     read_block_data,
    #     pump_run,
    #     ON,
    #     OFF,
)


class TestGreenPonik_WaterPump_Driver(unittest.TestCase):
    @patch("GreenPonik_WaterPump_Driver.GreenPonik_WaterPump_Driver.i2c_scanner")
    def test_i2c_scanner(self, mock_scan):
        expected_result = [100]
        mock_scan.return_value = expected_result

        devices = i2c_scanner()

        self.assertTrue(self, len(devices) > 0)
        self.assertTrue(self, type(devices).__name__ == "list")

    # def test_read_byte_data(self):
    #     for device in i2c_scanner():
    #         self.assertTrue(
    #             self,
    #             I2C_DEVICES_TYPE["WATERPUMP"]
    #             == read_byte_data(device, I2C_REGISTERS["TYPE"]),
    #         )
    #         sleep(0.2)

    # def test_read_block_data(self):
    #     for device in i2c_scanner():
    #         if I2C_DEVICES_TYPE["WATERPUMP"] == read_byte_data(
    #             device, I2C_REGISTERS["TYPE"]
    #         ):
    #             UUID = read_block_data(device, I2C_REGISTERS["UUID"])
    #             print(UUID)
    #             print(len(UUID))
    #             self.assertTrue(
    #                 self, type(UUID).__name__ == "list",
    #             )
    #             self.assertTrue(self, len(UUID) == 8)
    #         sleep(0.2)

    # def test_pump_run(self):
    #     for device in i2c_scanner():
    #         if I2C_DEVICES_TYPE["WATERPUMP"] == read_byte_data(
    #             device, I2C_REGISTERS["TYPE"]
    #         ):
    #             pump_run(device, I2C_REGISTERS["PUMP_1_STATE"], ON)
    #             self.assertTrue(
    #                 self, read_byte_data(device, I2C_REGISTERS["PUMP_1_STATE"]) == ON
    #             )
    #             sleep(10)
    #             pump_run(device, I2C_REGISTERS["PUMP_1_STATE"], OFF)
    #             self.assertTrue(
    #                 self, read_byte_data(device, I2C_REGISTERS["PUMP_1_STATE"]) == OFF
    #             )
    #         sleep(0.2)


if __name__ == "__main__":
    unittest.main()
