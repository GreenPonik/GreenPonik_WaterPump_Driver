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
