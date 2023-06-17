import machine
from ssd1306 import SSD1306_I2C
 
class DSP:
    def __init__(self, sdaPIN, sclPIN):
        sda=machine.Pin(sdaPIN)
        scl=machine.Pin(sclPIN)
        
        i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
        
        self.oled = SSD1306_I2C(128, 32, i2c)
        
    def show_message(self, message1, message2):
        self.oled.fill(0)
        self.oled.text(message1, 0, 0)
        self.oled.text(message2, 0, 20)
        self.oled.show()

