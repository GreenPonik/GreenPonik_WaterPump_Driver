from time import sleep
from GreenPonik_WaterPump_Driver.WaterPumpDriver import WaterPumpDriver
from adafruit_extended_bus import ExtendedI2C as I2C

if __name__ == "__main__":
    try:
        BUS = 1
        i2c = I2C(BUS)
        i2c_devices = i2c.scan()
        for device_addr in i2c_devices:
            driver = WaterPumpDriver(bus=BUS, addr=device_addr)
            if driver.I2C_DEVICES_TYPE != driver.read(driver.I2C_REGISTERS["TYPE"]):
                raise Exception("Device isn't a waterpump")
            else:
                UUID = driver.read(driver.I2C_REGISTERS["UUID"])
                print("Device UUID: %s" % UUID)
                driver.pump_run(
                    driver.I2C_REGISTERS["PUMP_1_STATE"],
                    driver.I2C_COMMANDS["ON"],
                )
                sleep(2)  # turn on pump 1 during 2sec
                driver.pump_run(
                    driver.I2C_REGISTERS["PUMP_1_STATE"],
                    driver.I2C_COMMANDS["OFF"],
                )
            sleep(0.5)
    except Exception as e:
        print("Exception occured", e)
