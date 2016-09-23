#!/usr/bin/env python
import BMP180_rpi
import time

s = BMP180_rpi.sensor()


for i in range(100): 
  print(s.temp()) 
#  time.sleep(0.5)


quit()
