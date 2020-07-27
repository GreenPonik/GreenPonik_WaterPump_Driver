from time import sleep
from GreenPonik_WaterPump_Driver import (
    I2C_REGISTERS, 
    I2C_DEVICES_TYPE, 
    ON, 
    OFF, 
    i2c_scanner, 
    read_block_data, 
    read_byte_data, 
    pump_run
)


if __name__ == "__main__":
    try:
        i2c_devices = i2c_scanner()
        for device in i2c_devices:
            if I2C_DEVICES_TYPE['WATERPUMP'] != read_byte_data(device, I2C_REGISTERS['TYPE']):
                raise Exception("Device isn't a waterpump")
            else:
                UUID = read_block_data(device, I2C_REGISTERS['UUID'])
                print("Device UUID: %s" % UUID)
                pump_run(device, I2C_REGISTERS['PUMP_1_STATE'], ON)
                sleep(2)
                pump_run(device, I2C_REGISTERS['PUMP_1_STATE'], OFF)
            sleep(0.5)
    except Exception as e:
        print("Exception occured", e)
