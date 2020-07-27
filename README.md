[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/workflows/Upload%20Python%20Package/badge.svg?event=release)

## GreenPonik_WaterPump_Driver.py Library for Raspberry pi
---------------------------------------------------------
This is the python side driver to manage GreenPonik WaterPump devices


## Table of Contents

- [GreenPonik_WaterPump_Driver.py Library for Raspberry pi](#GreenPonikWaterPumpDriverpy-library-for-raspberry-pi)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Methods](#methods)
- [Examples](#examples)
- [Credits](#credits)


## Installation
```shell
> git clone https://github.com/GreenPonik/GreenPonik_WaterPump_Driver.git
cd GreenPonik_WaterPump_Driver
pip3 install -r requirements.txt

or 

> pip3 install greenponik-waterpump-driver
```
```Python

from GreenPonik_WaterPump_Driver import i2c_scanner, read_byte_data

```

## Methods

```python
def i2c_scanner():
"""
@brief i2c Scanner use to return the list of all addresses find on the i2c bus
@return list of addresses
"""

def read_byte_data(addr, register):
"""
@brief read byte data from the device
@param addr > byte i2c address of the device
@param register > byte i2c register to read
"""

def write_byte_data(addr, register, value):
"""
@brief write byte data on the device
@param addr > byte i2c address of the device
@param register > byte i2c register to write
"""

def read_block_data(addr, register, size = 8):
"""
@brief read block byte data from the device
@param addr > byte i2c address of the device
@param register > byte i2c register to read
@param size > byte size of block read from i2c bus
"""

def write_block_data(addr, register, data):
"""
@brief write block byte data on the device
@param addr > byte i2c address of the device
@param register > byte i2c register to write
@param data > array of bytes to be send through i2c bus 
"""

def pump_run(addr, register, command):
"""
@brief command pump
@param addr > byte i2c address of the pump
@param register > byte i2c register of the pump
@param command > byte order 0x00 = OFF / 0x01 = ON
"""

```

## Example
```Python
from time import sleep
from GreenPonik_WaterPump_Driver import i2c_scanner, read_byte_data, read_block_data


if __name__ == "__main__":
    try:
        while True:
            i2c_devices = i2c_scanner()
            for device in i2c_devices:
                if I2C_DEVICES_TYPE['WATERPUMP'] != read_byte_data(device, I2C_REGISTERS['TYPE']:
                    raise Exception("Current device is not a WaterPump")
                else:
                    UUID = read_block_data(device, I2C_REGISTERS['UUID'])
                    print("Device UUID: %s" % UUID)
                sleep(0.5)
            sleep(2)
    except Exception as e:
        print("Exception occured", e)
```

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2019