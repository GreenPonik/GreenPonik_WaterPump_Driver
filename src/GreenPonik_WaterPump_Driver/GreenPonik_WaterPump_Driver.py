#!/usr/bin/env python
from time import sleep
from smbus2 import SMBus

import board
import busio


I2C_REGISTER = {
    "TYPE": 0x00,				# i2c Read Only
    "FIRMWARE": 0x01,			# i2c Read Only
    "UUID": 0x02,				# i2c Read Only
    "I2C_ADDRESS": 0x03,		# i2c Read / Write
    "PUMP_1_STATE": 0x05, 		# i2c Read / Write
    "PUMP_1_LED": 0x06,   		# i2c Read / Write
    "PUMP_2_STATE": 0x07, 		# i2c Read / Write
    "PUMP_2_LED": 0x08,   		# i2c Read / Write
    "PUMP_3_STATE": 0x9, 		# i2c Read / Write
    "PUMP_3_LED": 0x10,  		# i2c Read / Write
    "PUMP_4_STATE": 0x11, 		# i2c Read / Write
    "PUMP_4_LED": 0x12,   		# i2c Read / Write
    "WATER_PUMP_STATE": 0x13, 	# i2c Read / Write
    "WATER_PUMP_LED": 0x14, 	# i2c Read / Write
}

I2C_DEVICES_TYPE = {
    "WATERPUMP": 0x01,
}

ON = 0x01
OFF = 0x00

def i2c_scanner():
"""
@brief i2c Scanner use to return the list of all addresses find on the i2c bus
@return list of addresses
"""
   try:
        # instanciate i2c bus on the second raspberry bus
        i2c = busio.i2c(board.SCL, board.SDA)
        # Give the I2C device time to settle
        sleep(2)
        i2c_slaves = i2c.scan()
        i2c.deinit()
        return i2c_slaves
    except Exception as e:
        print("Exception occured", e)


def read_byte_data(addr, register):
"""
@brief read byte data from the device
@param addr > byte i2c address of the device
@param register > byte i2c register to read
"""
   try:
        with SMBus(1) as bus:
            byteData = bus.read_byte_data(addr, register)
            sleep(0.450)
            return byteData
    except Exception as e:
        print("Exception occured", e)


def write_byte_data(addr, register, value):
"""
@brief write byte data on the device
@param addr > byte i2c address of the device
@param register > byte i2c register to write
"""
   try:
        with SMBus(1) as bus:
            bus.write_byte_data(addr, register, value)
    except Exception as e:
        print("Exception occured", e)


def read_block_data(addr, register, size = 8):
"""
@brief read block byte data from the device
@param addr > byte i2c address of the device
@param register > byte i2c register to read
@param size > byte size of block read from i2c bus
"""
   try:
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(addr, register, size)
            sleep(0.450)
            return data
    except Exception as e:
        print("Exception occured", e)


def write_block_data(addr, register, data):
"""
@brief write block byte data on the device
@param addr > byte i2c address of the device
@param register > byte i2c register to write
@param data > array of bytes to be send through i2c bus 
"""
   try:
        with SMBus(1) as bus:
            bus.write_i2c_block_data(addr, register, data)
    except Exception as e:
        print("Exception occured", e)


def pump_run(addr, register, command):
"""
@brief command pump
@param addr > byte i2c address of the pump
@param register > byte i2c register of the pump
@param command > byte order 0x00 = OFF / 0x01 = ON
"""
    try:
        device = read_byte_data(addr, I2C_REGISTER['TYPE'])
        if I2C_DEVICES_TYPE['WATERPUMP'] != device:
            raise Exception(
                "Current device type %x indicate it's not a pump" % device)
        else:
            write_byte_data(addr, register, command)
    except Exception as e:
        print("Exception occured", e)
