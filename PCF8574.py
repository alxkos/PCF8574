from machine import I2C
# from typing import List, object as I2C

# PC8574/5 can be used in interrupt mode (use pin #1)
# set the I2C address using A0-A2 pins (from datasheet)

class PCF8574:
    """
    PCF8574 class

    """
    def __init__(self, i2c: I2C, address: hex = 0x40, validation: bool = True) -> None:
        """"""
        if isinstance(i2c, I2C):
            self.i2c = i2c
            self.address = address
            if validation:
                self._validateDevice()
        else:
            raise Exception("I2C is not an object")
            
    def _validateDevice(self) -> None or Exception: #check for given address on i2C bus
        """
            Validation for device
        """
        _addrs = self.i2c.scan()
        if not self.address in _addrs:
            raise Exception("Device address not found")
            #raise RuntimeError("Device is not accesable or not conected")
    
    def getPort(self) -> bytes or Exception: # read from device address nbytes and return port bytes
        """"""
        try:
            return int.from_bytes(self.i2c.readfrom(self.address, 1), 'little')
        except:
            raise Exception("Cannot read from device")

    def setPort(self, set: bool = True) -> int or Exception: #set all pins to HIGH or LOW, returns n of ACKs
        """"""
        _port = bytearray(1)
        if set:	_port[0] = 0xff
        else: _port[0] = 0x00
        try:
            return self.i2c.writeto(self.address, _port)
        except:
            raise Exception("Cannot write to device")

    def getPin(self, pin: int) -> int or Exception:
        """"""
        try:
            return ( int.from_bytes(self.i2c.readfrom(self.address, 8), 'little' ) >> pin) & 1
        except:
            raise Exception("Cannnot read from device")
        
    def setPin(self, pin: int, set: bool = True) -> int or Exception: #set pin to HIGH(True) or LOW(False) P0-P7
        """"""
        _port = bytearray(1)
        if set: _port[0] = self.getPort() | 1 << pin
        else:   _port[0] = self.getPort() ^ 1 << pin
        try:
            return self.i2c.writeto(self.address, _port)
        except:
            raise Exception("Cannot write to device")

    def setPins(self, pins: int) -> int or Exception: #set some pins to values ex:01101100
        """"""
        _pins = bytearray(1)
        _pins[0] = pins
        try:
            return self.i2c.writeto(self.address, _pins)
        except:
            raise Exception("Cannot write to device")
        
        

