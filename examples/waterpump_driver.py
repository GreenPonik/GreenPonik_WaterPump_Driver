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
