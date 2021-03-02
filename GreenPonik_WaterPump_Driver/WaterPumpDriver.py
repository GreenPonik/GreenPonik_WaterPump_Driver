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
from GreenPonik_WaterPump_Driver.packer import Packer
from GreenPonik_WaterPump_Driver.unpacker import Unpacker


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
        "WATER_PUMP_STATE": 0x05,  # i2c Read / Write
        "PUMP_1_STATE": 0x06,  # i2c Read / Write
        "PUMP_2_STATE": 0x07,  # i2c Read / Write
        "PUMP_3_STATE": 0x08,  # i2c Read / Write
        "PUMP_4_STATE": 0x09,  # i2c Read / Write
        "ALL": 0x20,  # i2c Read
    }
    """@brief
    Ordering Pumps Registers
    Array key=>value pump number to i2c register converter
    """
    PUMP_REGISTERS = {
        0: I2C_REGISTERS["WATER_PUMP_STATE"],
        1: I2C_REGISTERS["PUMP_1_STATE"],
        2: I2C_REGISTERS["PUMP_2_STATE"],
        3: I2C_REGISTERS["PUMP_3_STATE"],
        4: I2C_REGISTERS["PUMP_4_STATE"],
    }

    """@brief
    I2C Devices
    Array key=>value for each i2c device type you can read on the bus
    """
    I2C_DEVICES_TYPE = 1

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
        self._short_timeout = 0.6
        self._long_timeout = 1.4

    @property
    def bus(self):
        return self._bus

    @property
    def address(self):
        return self._addr

    @property
    def short_timeout(self):
        return self._short_timeout

    @property
    def long_timeout(self):
        return self._long_timeout

    @property
    def debug(self):
        return self._debug

    @short_timeout.setter
    def short_timeout(self, t):
        self._short_timeout = t

    @long_timeout.setter
    def long_timeout(self, t):
        self._long_timeout = t

    @debug.setter
    def debug(self, d):
        self._debug = d

    def __enter__(self):
        """Context manager enter function."""
        # Just return this object so it can be used in a with statement, like
        #     # do stuff!
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit function, ensures resources are cleaned up."""
        self._smbus.close()
        return False  # Don't suppress exceptions.

    def __del__(self):
        """Clean up any resources instance."""
        self._smbus.close()

    def _device_is_water_pump(self):
        try:
            device_type = None
            try:
                with Packer() as packer:
                    # packer.debug = True
                    # first write => the register address we want read/write
                    packer.write(self.I2C_REGISTERS["TYPE"])
                    packer.end()
                    self._smbus.write_bytes(self._address, bytearray(packer.read()))
            except Exception as e:
                print("ERROR: on packer, {}".format(e))
            try:
                sleep(self._short_timeout)
                raw = self._smbus.read_bytes(
                    self._address, 5
                )  # read 5 bytes from slave due to data format
                if self._debug:
                    print("Raw data from i2c: ", raw)
            except Exception as e:
                print("ERROR: on smbus, {}".format(e))
            try:
                with Unpacker() as unpacker:
                    # unpacker.debug = True
                    unpacker.write(raw)
                    device_type = unpacker.read()[
                        0
                    ]  # type data is the first field of list
            except Exception as e:
                print("ERROR: on unpack, {}".format(e))

            return device_type == self.I2C_DEVICES_TYPE

        except Exception as e:
            print("ERROR: on device type check {}".format(e))

    def read(self, register: int, num_of_bytes: int = 5):
        """
        @brief read data from i2c bus
        @param register > int i2c register to read
        @param num_of_byte > int number of bytes to read started from the register
        by default num_of_bytes = 5 because the data format from ESP32 i2c slave is 5 length
        more information on Packer() and Unpacker() classes
        @return list
        """
        # if not self._device_is_water_pump():
        #     raise Exception("Current device type is not a water pump")
        # else:
        try:
            unpacked = None
            try:
                with Packer() as packer:
                    packer.write(register)
                    packer.end()
                    packed = packer.read()
                    self._smbus.write_bytes(self._address, bytearray(packed))
            except Exception as e:
                print("ERROR: on packer, {}".format(e))
            try:
                sleep(self._short_timeout)  # let the bus process first write
                raw = self._smbus.read_bytes(self._address, num_of_bytes)
                if self._debug:
                    print("Raw data from i2c: ", raw)
            except Exception as e:
                print("ERROR: on smbus, {}".format(e))
            try:
                with Unpacker() as unpacker:
                    unpacker.write(list(raw))
                    unpacked = unpacker.read()
            except Exception as e:
                print("ERROR: on unpacker, {}".format(e))
            if self._debug:
                print(
                    "Read: %s registers start from: %s" % (num_of_bytes, hex(register))
                )
                print("Get values: ", unpacked)
            return unpacked
        except Exception as e:
            print("ERROR: on read, {}".format(e))

    def write(self, register: int, value=None):
        """
        @brief write data through i2c bus
        @param register > int/byte i2c register to read
        @param value > int/list to be write through i2c
        """
        # if not self._device_is_water_pump():
        #     raise Exception("Current device type is not a water pump")
        # else:
        try:
            with Packer() as packer:
                # first write => the register address we want read/write
                packer.write(register)
                # if value == None we just write register we want read into the i2c bus and then read the value
                if None is not value:
                    if int is not type(value) and list is type(value):
                        for elm in value:
                            packer.write(elm)
                    elif int is type(value):
                        packer.write(value)
                    else:
                        raise Exception("cannot format this kind of data: ", value)
                packer.end()  # finish data formatting
                packed = packer.read()
        except Exception as e:
            print("ERROR: {0}, cannot use packer yo prepare data".format(e))

        try:
            self._smbus.write_bytes(self._address, bytearray(packed))
        except Exception as e:
            print(
                "ERROR: {0}, when write data on i2c: ".format(e),
                packed,
            )
        if self._debug:
            print("Write %s on register: %s" % (value, hex(register)))

    def list_i2c_devices(self):
        """
        @brief list all i2c device on the current bus
        @return list of addresses
        """
        try:
            with I2C(self._bus) as i2c:
                scan = i2c.scan()
                if self._debug:
                    print("I2c devices found: ", scan)
                return scan
        except Exception as e:
            print("ERROR: Exception occured during get i2c devices list", e)

    def print_all_registers_values(self):
        """
        @brief print all i2c register value on the cli
        """
        try:
            for reg in range(0, len(self.I2C_REGISTERS)):
                print("Register: %s, Value: %s" % (hex(reg), self.read(reg)))
        except Exception as e:
            print("ERROR: Exception occured during get all registers values", e)

    # ----- getters ----- #

    def get_all(self):
        """
        @brief get the device type
        @return dict all i2c registers values
        """
        try:
            # 13 registers to read from the i2c slave to get all values
            # add 4 bytes to add data format
            _all = self.read(self.I2C_REGISTERS["ALL"], 17)
            if self._debug:
                print("ask for all registers: %s" % _all)
            return _all
        except Exception as e:
            print("ERROR: Exception occured during get type", e)

    def get_type(self):
        """
        @brief get the device type
        @return int 1=>water pump
        """
        try:
            _type = self.read(self.I2C_REGISTERS["TYPE"])[0]
            if self._debug:
                print("ask for type: %s" % _type)
            return _type
        except Exception as e:
            print("ERROR: Exception occured during get type", e)

    def get_firmware(self):
        """
        @brief get the device type
        @return int 2=>firmware rev 2
        """
        try:
            firmware = self.read(self.I2C_REGISTERS["FIRMWARE"])[0]
            if self._debug:
                print("ask for firmware: %s" % firmware)
            return firmware
        except Exception as e:
            print("ERROR: Exception occured during get firmware", e)

    def get_uuid(self):
        """
        @brief get the device uuid
        @return 8 bytes 5241224745987163 => device uuid
        """
        try:
            # ask for 12 bytes because uuid is 8 bytes long + 4 bytes for data formatting
            uuid = "".join(map(str, self.read(self.I2C_REGISTERS["UUID"], 12)))
            if self._debug:
                print("ask for uuid: %s" % uuid)
            return uuid
        except Exception as e:
            print("ERROR: Exception occured during get uuid", e)

    def get_i2c_address(self):
        """
        @brief get the device i2c address
        @return int 100=>address 100 = 0x64
        """
        try:
            add = self.read(self.I2C_REGISTERS["I2C_ADDRESS"])[0]
            if self._debug:
                print("ask for add: %s" % add)
            return add
        except Exception as e:
            print("ERROR: Exception occured during get address", e)

    def get_led_status(self):
        """
        @brief get the device leds status
        @return int 0=>LEDs OFF / 1=>LEDs ON
        """
        try:
            led_status = self.read(self.I2C_REGISTERS["LED_ACTIVATION"])[0]
            if self._debug:
                print("ask for led status: %s" % led_status)
            return led_status
        except Exception as e:
            print("ERROR: Exception occured during get LEDs status", e)

    def get_pump_status(self, pump_register: int):
        """
        @brief get the pump status
        @param int pump register to ask
        @return int 0=>pump OFF / 1=>pump ON
        """
        try:
            status = self.read(pump_register)[0]
            if self._debug:
                print("ask for pump: %s status: %s" % (pump_register, status))
            return status
        except Exception as e:
            print("ERROR: Exception occured during get pump status", e)

    # ----- setters ----- #

    def set_i2c_address(self, addr: int):
        """
        @brief set water pump i2c address
        @param int addr => new address
        """
        try:
            self.write(self.I2C_REGISTERS["I2C_ADDRESS"], addr)
        except Exception as e:
            print("ERROR: Exception occured during set i2c address", e)

    def set_led_status(self, status: int):
        """
        @brief set water pump LEDs activation
        @param int status => new status 0=>OFF / 1=>ON
        """
        try:
            self.write(self.I2C_REGISTERS["LED_ACTIVATION"], status)
        except Exception as e:
            print("ERROR: Exception occured during set LEDs status", e)

    def set_pump_command(self, pump_register: int, command: int):
        """
        @brief set command pump
        @param int pump_register to set
        @param int command 0=>pump OFF / 1=>pump ON
        """
        try:
            self.write(pump_register, command)
            if self._debug:
                print("Pump: %s, Command passed: %s" % (pump_register, command))
        except Exception as e:
            print("ERROR: Exception occured during set pump command", e)
