from pyb import I2C
from struct import *
#i2c = I2C(1, I2C.MASTER)

class sensor():

  def __init__(self, i2c_channel=1):
    # check that i2c_channel is either 1 or 2
    self.i2c = I2C(i2c_channel, I2C.MASTER)
    self.init()
    return
  
  def soft_reset(self):
    #do a soft reset
    self.i2c.mem_read(0xB6, 119, 0xE0)

  def init(self):
    self.soft_reset()

    # read the calibration registers
    (self.ac1, self.ac2, self.ac3, self.ac4, self.ac5, self.ac6, self.b1, self.b2, self.mb, self.mc, self.md) = unpack('>hhhHHHhhhhh', self.i2c.mem_read(22, 119, 0xAA))

  def temp(self):
    self.i2c.mem_write(0x2E, 119, 0xF4)

    # read uncompensated value
    x = self.i2c.mem_read(3, 119, 0xF6)
    ut = unpack('>h', x)[0]
    x1 = (ut - self.ac6) * self.ac5 / 32768
    x2 = self.mc * 2048 / (x1 + self.md)
    b5 = x1 + x2
    t = (b5 + 8) / 16

    return(t)

