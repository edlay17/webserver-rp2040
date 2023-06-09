# in the implementation the following reference codes were used
#https://github.com/robert-hh/QMC5883/blob/master/qmc5883.py
#https://github.com/gvalkov/micropython-esp8266-hmc5883l/blob/master/hmc5883l.py

import math
import machine
from ustruct import pack
from array import array
import time

class QMC5883L():
    xs=1
    ys=0.01341575
    xb=-562.5
    yb=-32760.0
    
    def __init__ (self, scl=17, sda=16, declination=(6, 66) ):
        self.i2c = i2c = machine.SoftI2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        print(i2c.scan())
        #self.address=const(13)
        # Initialize sensor.
        i2c.start()
        #Write Register 0BH by 0x01 (Define Set/Reset period)
        i2c.writeto_mem(13, 0xB, b'\x01')
        #Write Register 09H by 0x1D 
        # (Define OSR = 512, Full Scale Range = 8 Gauss, ODR = 200Hz, set continuous measurement mode)
        i2c.writeto_mem(13, 0x9, b'\x11101')
        i2c.stop()
        
        self.declination = (declination[0] + declination[1] / 60) * math.pi / 180

        # Reserve some memory for the raw xyz measurements.
        self.data = array('B', [0] * 9)
           
    def reset(self):
        """performs a reset of the device by writing to the memory address 0xA, the value of b '\ x10000000' """
        #Write Register 0AH by 0x80
        self.i2c.writeto_mem(13, 0xA, b'\x10000000')

    def stanbdy (self):
        """device goes into a sleep state by writing to memory address 0x9, b '\ x00' """
        self.i2c.writeto_mem(13, 0x9, b'\x00')
        
    def heading(self, x, y):
        heading_rad = math.atan2(y, x)
        heading_rad += self.declination

        # Correct reverse heading.
        if heading_rad < 0:
            heading_rad += 2 * math.pi

        # Compensate for wrapping.
        elif heading_rad > 2 * math.pi:
            heading_rad -= 2 * math.pi

        # Convert from radians to degrees.
        heading = heading_rad * 180 / math.pi
        degrees = math.floor(heading)
        minutes = round((heading - degrees) * 60)
        return degrees, minutes

    def read(self):
        """performs a reading of the data in the position of momoria 0x00, by means of a buffer"""
        data = self.data
        #Read data register 00H ~ 05H.
        
        
        self.i2c.readfrom_mem_into(13, 0x00, data)
        time.sleep(0.005)
        #self.i2c.readfrom_mem_into(13, 0x00, temperature)
        #time.sleep(0.005)

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        status =data[6]
        temperature =z = (data[8] << 8) | data[7]
        scale =3000
        temperature_offest=50.0
        
        x = x * self.xs + self.xb
        x = y * self.ys + self.yb

        return x, y

    