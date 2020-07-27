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


"""@brief
instanciate i2c bus on the second raspberry bus
"""
i2c = busio.i2c(board.SCL, board.SDA)
# Give the I2C device time to settle
sleep(2)


"""@brief
i2c Scanner use to return the list of all addresses find on the i2c bus
"""
def i2c_scanner():
    try:
        i2c_slaves = i2c.scan()
        sleep(1)
        return i2c_slaves
    except Exception as e:
        print("Exception occured", e)


"""@brief
turn pump ON
"""
def pump_on(addr, register):
	try:
		with SMBus(1) as bus:
			device = get_device_type(addr)
			if 0x01 != device:
				raise Exception("Current device is not a pump") 
			else:	
				bus.write_byte_data(addr, register, 0x01)
	except Exception as e:
		print("Exception occured", e)


"""@brief
turn pump OFF
"""
def pump_off(addr, register):
	try:
		with SMBus(1) as bus:
			device = get_device_type(addr)
			if 0x01 != device:
				raise Exception("Current device is not a pump") 
			else:	
				bus.write_byte_data(addr, register, 0x01)
	except Exception as e:
		print("Exception occured", e)


"""@brief
get the TYPE of device
TYPE is 1 for WaterPump
"""
def get_device_type(addr):
	try:
		with SMBus(1) as bus:
			deviceType = bus.read_byte_data(addr, I2C_REGISTER["TYPE"])
			sleep(0.450)
			return deviceType
	except Exception as e:
		print("Exception occured", e)


"""@brief
get the FIRMWARE of device
FIRMWARE is on byte long and need to be divide by 100
"""
def get_device_firmware(addr):
	try:
		with SMBus(1) as bus:
			deviceFirm = bus.read_byte_data(addr, I2C_REGISTER["FIRMWARE"])
			sleep(0.450)
			return deviceFirm
	except Exception as e:
		print("Exception occured", e)


"""@brief
get the UUID of device
UUID is 8 bytes long
"""
def get_device_UUID(addr):
	try:
		with SMBus(1) as bus:
			deviceUUID = bus.read_i2c_block_data(addr, I2C_REGISTER["UUID"], 8)
			sleep(0.450)
			return deviceUUID
	except Exception as e:
		print("Exception occured", e)

