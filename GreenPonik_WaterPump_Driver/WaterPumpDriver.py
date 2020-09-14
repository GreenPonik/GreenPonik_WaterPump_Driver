#! /usr/bin/env python3

"""
@package Module to drive GreenPonik's WaterPump device
#####################################################################
#####################################################################
#####################################################################
#################### GreenPonik_WaterPump_Driver ####################
#####################################################################
#####################################################################
#####################################################################
"""

from time import sleep
from Adafruit_PureIO.smbus import SMBus
from adafruit_extended_bus import ExtendedI2C as I2C


class WaterPumpDriver:

    DEFAULT_BUS = 1
    DEFAULT_ADDR = 0x0A

    """@brief
    I2C Registers
    Array key=>value for each i2c register you can read
    """
    I2C_REGISTERS = {
        "TYPE": 0x00,  # i2c Read Only
        "FIRMWARE": 0x01,  # i2c Read Only
        "UUID": 0x02,  # i2c Read Only
        "I2C_ADDRESS": 0x03,  # i2c Read / Write
        "LED_ACTIVATION": 0x05,  # i2c Read / Write
        "PUMP_1_STATE": 0x06,  # i2c Read / Write
        "PUMP_2_STATE": 0x07,  # i2c Read / Write
        "PUMP_3_STATE": 0x08,  # i2c Read / Write
        "PUMP_4_STATE": 0x09,  # i2c Read / Write
        "WATER_PUMP_STATE": 0x10,  # i2c Read / Write
    }

    """@brief
    I2C Devices
    Array key=>value for each i2c device type you can read on the bus
    """
    I2C_DEVICES_TYPE = 0x01

    """@brief
    I2C command
    Array key=>value for each command can be send through bus
    """
    I2C_COMMANDS = {"OFF": 0x00, "ON": 0x01}

    def __init__(self, bus=DEFAULT_BUS, addr=DEFAULT_ADDR):
        self._bus = bus
        self._address = addr
        self._smbus = SMBus(bus)
        self._debug = False

    @property
    def bus(self):
        return self._bus

    @property
    def address(self):
        return self._addr

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, d):
        self._debug = d

    def i2c_scanner(self):
        """
        @brief i2c Scanner use to return
        the list of all addresses
        find on the i2c bus
        @return list of addresses
        """
        try:
            i2c = I2C(self._bus)
            sleep(1)
            i2c_devices = i2c.scan()
            i2c.deinit()
            return i2c_devices
        except Exception as e:
            print("Exception occured", e)

    def read(self, register, num_of_bytes=1):
        """
        @brief read data from i2c bus
        @param register > int i2c register to read
        @param num_of_byte > int number of bytes to read started from the register
        """
        try:
            if num_of_bytes > 1:
                raw = self._smbus.read_i2c_block_data(
                    self._address, register, num_of_bytes
                )
            else:
                raw = self._smbus.read_byte_data(self._address, register)

            if self._debug:
                print(
                    "Read: %s registers start from: %s" % (num_of_bytes, hex(register))
                )
                print("Raw response from i2c: ", raw)
            return raw
        except Exception as e:
            print("Exception occured", e)

    def write(self, register: int, v):
        """
        @brief write data through i2c bus
        @param register > int i2c register to read
        @param v > int/bytearray to write through i2c
        """
        if (
            "int" != type(v).__name__
            and len(v) > 1
            and ("bytearray" == type(v).__name__ or "bytes" == type(v).__name__)
        ):
            self._smbus.write_i2c_block_data(self._address, register, v)
        elif "int" == type(v).__name__:
            self._smbus.write_byte_data(self._address, register, v)
        else:
            raise IOError("cannot write this in smbus/i2c: ", v)
        if self._debug:
            print("Write %s on register: %s" % (v, hex(register)))

    def list_i2c_devices(self):
        """
        @brief save the current address so we can restore it after
        """
        with I2C(self._bus_number) as i2c:
            scan = i2c.scan()
            if self._debug:
                print("I2c devices found: ", scan)
            return scan

    def print_all_registers_values(self):
        if "EC" == self._module:
            registers = self.OEM_EC_REGISTERS
        elif "PH" == self._module:
            registers = self.OEM_PH_REGISTERS
        for reg in range(0, len(registers)):
            print("Register: %s, Value: %s" % (hex(reg), self.read(reg)))

    def pump_run(self, register, command):
        """
        @brief command pump
        @param register > byte i2c register of the pump
        @param command > byte order 0x00 = OFF / 0x01 = ON
        """
        try:
            deviceType = self._bus(self.I2C_REGISTERS["TYPE"])
            print(deviceType)
            if self.I2C_DEVICES_TYPE != deviceType:
                raise Exception("Current device type %x is not a pump" % deviceType)
            else:
                self.write(register, command)
        except Exception as e:
            print("Exception occured", e)
