"""
@file Packer.py
@author Mickael Lehoux <https://github.com/MkLHX>
@brief Class to allow raspberry I2C Master to deal with ESP32 using ESP32 Slave I2C library
@date 2020-09-18

The ESP32 Slave I2C library use packing and upacking
classes to format data
On python side we need to adapt data format
before send them through i2c

Packet format:
    [0]: start byte (0x02)
    [1]: packet length
    [2]: data[0]
    [3]: data[1]
    ...
    [n+1]: data[n-1]
    [n+2]: CRC8 of packet length and data
    [n+3]: end byte (0x04)
based on:
https://github.com/gutierrezps/ESP32_I2C_Slave/blob/master/src/WirePacker.h
https://github.com/gutierrezps/ESP32_I2C_Slave/blob/master/src/WirePacker.cpp
"""
from crc8 import _Crc8


class Packer:
    PACKER_BUFFER_LENGTH = 128

    def __init__(self):
        self._frame_start = 0x02
        self._frame_end = 0x04
        # uint8_t buffer_[PACKER_BUFFER_LENGTH]
        self._buffer = [0] * self.PACKER_BUFFER_LENGTH
        self._index = 0
        self._total_length = 0
        self._is_packet_open = 0
        self.reset()

    def __enter__(self):
        """Context manager enter function."""
        # Just return this object so it can be used in a with statement, like
        # with Packer() as packer:
        #     # do stuff!
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit function, ensures resources are cleaned up."""
        self.reset()
        return False  # Don't suppress exceptions.

    def read(self):
        """
        Read the next available packet byte. At each call,
        the value returned by available() will be decremented.
        @return int -1 if no bytes to read / byte value
        """
        value = -1
        if not self._is_packet_open and self._index < self._total_length:
            value = self._buffer[self._index]
            self._index += 1
        return value

    def write(self, data):
        if not self._is_packet_open or self._total_length >= (
            self.PACKER_BUFFER_LENGTH - 2
        ):
            return 0
        if "bytes" == type(data).__name__:
            self._buffer[self._index] = int.from_bytes(data, byteorder="big")
        elif "int" == type(data).__name__:
            self._buffer[self._index] = data
        # elif "str" == type(data).__name__:
        #     self._buffer.extend(data.encode())
        else:
            raise TypeError("cannot write this data type on i2c bus")

        self._index += 1
        print(self._index)
        self._total_length = self._index
        return 1

    def end(self):
        """
        @brief Closes the packet. After that, use avaiable() and read()
        to get the packet bytes.
        """
        self._is_packet_open = False
        # make room for CRC byte
        self._index += 1
        self._buffer[self._index] = self._frame_end
        self._index += 1
        self._total_length = self._index
        self._buffer[1] = self._total_length

        # ignore crc and end bytes
        payload_range = self._total_length - 2

        # print(payload_range)
        # ignore start and length bytes [2:payload_range]
        crc = _Crc8()
        _crc8 = crc.calc(self._buffer[2:payload_range])

        self._buffer[self._index - 2] = _crc8
        #  prepare for reading
        self._index = 0

    def reset(self):
        """
        @brief Reset the packing process.
        """
        self._buffer[0] = self._frame_start
        self._index = 2
        self._total_length = 2
        self._is_packet_open = True

    def available(self):
        """
        @brief Returns how many packet bytes are available to be read
        """
        if self._is_packet_open:
            return 0
        return self._total_length - self._index

    def packet_length(self):
        """
        @brief Returns packet length so far
        @return int
        """
        if self._is_packet_open_:
            return self._total_length + 2
        return self._total_length
