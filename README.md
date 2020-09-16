[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=alert_status)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=ncloc)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=security_rating)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GreenPonik_GreenPonik_WaterPump_Driver&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=GreenPonik_GreenPonik_WaterPump_Driver)


![Upload Python Package](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/workflows/Upload%20Python%20Package/badge.svg?event=release)
<!-- [![Documentation](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/blob/master/assets/doxygen_badge.svg)](https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/docs/index.html) -->

# GreenPonik_WaterPump_Driver.py Library for Raspberry pi
## A python3 class to manage GreenPonik WaterPump devices<br>

## ! Only tested on Raspberry Pi 3 A+ !<br>

# Table of Contents

- [GreenPonik_WaterPump_Driver.py Library for Raspberry pi](#GreenPonikWaterPumpDriverpy-library-for-raspberry-pi)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Examples](#examples)
- [Credits](#credits)


# Installation
```shell
> git clone https://github.com/GreenPonik/GreenPonik_WaterPump_Driver.git
cd GreenPonik_WaterPump_Driver
pip3 install -r requirements.txt

or 

> pip3 install greenponik-waterpump-driver
```
```Python

from GreenPonik_WaterPump_Driver.WaterPumpDriver import WaterPumpDriver
```

## Example
```Python
import time
from GreenPonik_WaterPump_Driver.WaterPumpDriver import WaterPumpDriver


if __name__ == "__main__":
    # run pump one during 2sec
    try:
        with WaterPumpDriver() as driver:  # default bus=1, default address=0x01
            print("My UUIDis : %s" % driver.get_uuid())
            driver.set_pump_command(
                driver.I2C_REGISTERS["PUMP_1_STATE"],
                driver.I2C_COMMANDS["ON"],
            )
            time.sleep(2)
            driver.set_pump_command(
                driver.I2C_REGISTERS["PUMP_1_STATE"],
                driver.I2C_COMMANDS["OFF"],
            )
    except Exception as e:
        print("Exception occured", e)

```
go to [examples](examples/waterpump_driver.py)

## Credits
Write by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2020