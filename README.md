[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/workflows/Upload%20Python%20Package/badge.svg?event=release)
<!-- [![Documentation](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/blob/master/assets/doxygen_badge.svg)](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/html/index.html) -->

## GreenPonik_WaterPump_Driver.py Library for Raspberry pi
---------------------------------------------------------
This is the python side driver to manage GreenPonik WaterPump devices

## ! Only tested on Raspberry Pi 3 A+ !<br>

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

from GreenPonik_WaterPump_Driver import WaterPumpDriver

```

## Methods

```python
def i2c_scanner():
"""
@brief i2c Scanner use to return the list of all addresses find on the i2c bus
@return list of addresses
"""

def read_byte_data(addr, register, buffer=bytearray(1)):
"""
@brief read byte data from the device
@param addr > byte i2c address of the device
@param register > byte i2c register to read
@param buffer > bytearray write bytes has bytearray is long
@return byte
"""

def write_byte_data(addr, register, buffer=bytearray(1)):
"""
@brief write byte data on the device
@param addr > byte i2c address of the device
@param register > byte i2c register to write
@param buffer > bytearray write bytes has bytearray is long
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
from GreenPonik_WaterPump_Driver import WaterPumpDriver


if __name__ == "__main__":
    driver = WaterPumpDriver()
    try:
        i2c_devices = driver.i2c_scanner()
        for device in i2c_devices:
            if driver.I2C_DEVICES_TYPE["WATERPUMP"] != driver.read_byte_data(
                device, driver.I2C_REGISTERS["TYPE"]
            ):
                raise Exception("Device isn't a waterpump")
            else:
                UUID = driver.read_byte_data(device, driver.I2C_REGISTERS["UUID"])
                print("Device UUID: %s" % UUID)
                driver.pump_run(
                    device,
                    driver.I2C_REGISTERS["PUMP_1_STATE"],
                    driver.I2C_COMMANDS["ON"],
                )
                sleep(2)
                driver.pump_run(
                    device,
                    driver.I2C_REGISTERS["PUMP_1_STATE"],
                    driver.I2C_COMMANDS["OFF"],
                )
            sleep(0.5)
    except Exception as e:
        print("Exception occured", e)
```
go to [examples](examples/waterpump_driver.py)

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2019