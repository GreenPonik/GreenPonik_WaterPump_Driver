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
    DEFAULT_ADDR = 0x01

    """@brief
    I2C Registers
    Array key=>value for each i2c register you can read
    """
    I2C_REGISTERS = {
        "TYPE": 0x00,  # i2c Read Only
        "FIRMWARE": 0x01,  # i2c Read Only
        "UUID": 0x02,  # i2c Read Only
        "I2C_ADDRESS": 0x03,  # i2c Read / Write
        "LED_ACTIVATION": 0x04,  # i2c Read / Write
        "PUMP_1_STATE": 0x05,  # i2c Read / Write
        "PUMP_2_STATE": 0x06,  # i2c Read / Write
        "PUMP_3_STATE": 0x07,  # i2c Read / Write
        "PUMP_4_STATE": 0x08,  # i2c Read / Write
        "WATER_PUMP_STATE": 0x09,  # i2c Read / Write
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

    def read(self, register: int, num_of_bytes=1):
        """
        @brief read data from i2c bus
        @param register > int i2c register to read
        @param num_of_byte > int number of bytes to read started from the register
        """
        try:
            device_type = self._smbus.read_byte_data(
                self._address, self.I2C_REGISTERS["TYPE"]
            )
            if device_type != self.I2C_DEVICES_TYPE:
                raise Exception(
                    "Current device type %x is not a water pump" % device_type
                )
            else:
                if num_of_bytes > 1:
                    raw = self._smbus.read_i2c_block_data(
                        self._address, register, num_of_bytes
                    )
                else:
                    raw = self._smbus.read_byte_data(self._address, register)

                if self._debug:
                    print(
                        "Read: %s registers start from: %s"
                        % (num_of_bytes, hex(register))
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
        try:
            device_type = self._smbus.read(self.I2C_REGISTERS["TYPE"])
            if device_type != self.I2C_DEVICES_TYPE:
                raise Exception("Current device type %x is not a water pump" % device_type)
            else:
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
        except Exception as e:
            print("Exception occured", e)

    def list_i2c_devices(self):
        """
        @brief list all i2c device on the current bus
        """
        try:
            with I2C(self._bus_number) as i2c:
                scan = i2c.scan()
                if self._debug:
                    print("I2c devices found: ", scan)
                return scan
        except Exception as e:
            print("Exception occured during get i2c devices list", e)

    def print_all_registers_values(self):
        """
        @brief print all i2c register value on the cli
        """
        try:
            registers = self.I2C_REGISTERS
            for reg in range(0, len(registers)):
                print("Register: %s, Value: %s" % (hex(reg), self.read(reg)))
        except Exception as e:
            print("Exception occured during print all registers values", e)

    # ----- getters ----- #

    def get_type(self):
        """
        @brief get the device type
        @return int 1=>water pump
        """
        try:
            t = self.read(self.I2C_REGISTERS["TYPE"])
            if self._debug:
                print("ask for type: %s" % t)
            return t
        except Exception as e:
            print("Exception occured during get type", e)

    def get_firmware(self):
        """
        @brief get the device type
        @return int 2=>firmware rev 2
        """
        try:
            firmware = self.read(self.I2C_REGISTERS["FIRMWARE"])
            if self._debug:
                print("ask for firmware: %s" % firmware)
            return firmware
        except Exception as e:
            print("Exception occured during get firmware", e)

    def get_uuid(self):
        """
        @brief get the device uuid
        @return 8 bytes 5241224745987163 => device uuid
        """
        try:
            uuid = self.read(self.I2C_REGISTERS["UUID"])
            if self._debug:
                print("ask for uuid: %s" % uuid)
            return uuid
        except Exception as e:
            print("Exception occured during get uuid", e)

    def get_address(self):
        """
        @brief get the device i2c address
        @return int 100=>address 100 = 0x64
        """
        try:
            add = self.read(self.I2C_REGISTERS["I2C_ADDRESS"])
            if self._debug:
                print("ask for add: %s" % add)
            return add
        except Exception as e:
            print("Exception occured during get address", e)

    def get_led_status(self):
        """
        @brief get the device leds status
        @return int 0=>LEDs OFF / 1=>LEDs ON
        """
        try:
            led_status = self.read(self.I2C_REGISTERS["LED_ACTIVATION"])
            if self._debug:
                print("ask for led status: %s" % led_status)
            return led_status
        except Exception as e:
            print("Exception occured during get LEDs status", e)

    def get_pump_status(self, pump_register: int):
        """
        @brief get the pump status
        @param int pump register to ask
        @return int 0=>pump OFF / 1=>pump ON
        """
        try:
            status = self.read(pump_register)
            if self._debug:
                print("ask for pump: %s status: %s" % (pump_register, status))
            return status
        except Exception as e:
            print("Exception occured during get pump status", e)

    # ----- setters ----- #

    def set_i2c_address(self, addr: int):
        """
        @brief set water pump i2c address
        @param int addr => new address
        """
        try:
            self._smbus.write(self.I2C_REGISTERS["I2C_ADDRESS"], addr)
        except Exception as e:
            print("Exception occured during set i2c address", e)

    def set_led_status(self, status: int):
        """
        @brief set water pump LEDs activation
        @param int status => new status 0=>OFF / 1=>ON
        """
        try:
            self._smbus.write(self.I2C_REGISTERS["LED_ACTIVATION"], status)
        except Exception as e:
            print("Exception occured during set LEDs status", e)

    def set_pump_command(self, pump_register: int, command: int):
        """
        @brief set command pump
        @param int pump_register to set
        @param int command 0=>pump OFF / 1=>pump ON
        """
        try:
            self.write(pump_register, command)
            if self._debug:
                print(
                    "Pump: %s, Command passed: %s"
                    % (pump_register, command)
                )
        except Exception as e:
            print("Exception occured during set pump command", e)
