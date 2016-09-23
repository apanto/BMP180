import smbus
from struct import unpack
from time import sleep

class sensor():

  def __init__(self, i2c_channel=1):
    # check that i2c_channel is either 1 or 2
    self.i2c = smbus.SMBus(1)
    self.DEVICE_ADDRESS = 0x77

    # Register addresses
    self.R_OUT_XLSB     = 0xF8
    self.R_OUT_LSB      = 0xF7
    self.R_OUT_MSB      = 0xF6
    self.R_CTRL_MEAS    = 0xF4
    self.R_SOFT_RESET   = 0xE0
    self.R_CALLIBRATION = 0xAA
    self.R_AC1          = 0xAA
    self.R_AC2          = 0xAC
    self.R_AC3          = 0xAE
    self.R_AC4          = 0xB0
    self.R_AC5          = 0xB4
    self.R_AC6          = 0xB6
    self.R_B1           = 0xB6
    self.R_B2           = 0xB8
    self.R_MB           = 0xBA
    self.R_MC           = 0xBC
    self.R_MD           = 0xBE
    
    # constants
    self.SOFT_RESET = 0xB6

    self.init()
    return

  def read_word(self, device_addr, reg_addr):
    return unpack('>H', bytes(bytearray([self.i2c.read_byte_data(device_addr, reg_addr), self.i2c.read_byte_data(device_addr, reg_addr+1)])))
  
  def soft_reset(self):
    #do a soft reset
    self.i2c.write_byte_data(self.DEVICE_ADDRESS, self.R_SOFT_RESET, self.SOFT_RESET)
    sleep(0.1)

  def init(self):
    # read the calibration registers
    (self.ac1, self.ac2, self.ac3, self.ac4, self.ac5, self.ac6, self.b1, self.b2, self.mb, self.mc, self.md) = unpack( '>hhhHHHhhhhh', bytes(bytearray(self.i2c.read_i2c_block_data(self.DEVICE_ADDRESS, self.R_CALLIBRATION)[0:22])) )

    self.soft_reset()

  def temp(self):
    # Write 0x2E into control measurement register to start the measurement
    self.i2c.write_byte_data(self.DEVICE_ADDRESS, self.R_CTRL_MEAS, 0x2E)
    
    # according to DS upon start of measurement the measured values will be written after 4.5 ms
    sleep(0.005)
    #for i in range(10):
    #  print self.i2c.read_byte_data(self.DEVICE_ADDRESS, self.R_CTRL_MEAS)

    # read uncompensated value
    (ut, ) = unpack('>h', bytes(bytearray([self.i2c.read_byte_data(self.DEVICE_ADDRESS, self.R_OUT_MSB), self.i2c.read_byte_data(self.DEVICE_ADDRESS, self.R_OUT_LSB)])))
    #print(ut)
    x1 = (ut - self.ac6) * self.ac5 / 32768.0
    x2 = self.mc * 2048.0 / (x1 + self.md)
    b5 = x1 + x2
    t = ( (b5 + 8.0) / 16.0 ) / 10.0

    return(t)
