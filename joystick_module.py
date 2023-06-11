from machine import Pin, ADC
import utime
 
class JST:
    def __init__(self, xPin, yPin, bPin):
        self.xAxis = ADC(Pin(xPin))
        self.yAxis = ADC(Pin(yPin))
        self.button = Pin(bPin,Pin.IN, Pin.PULL_UP)
        
    def get_value(self):    
        xValue = self.xAxis.read_u16()
        yValue = self.yAxis.read_u16()
        buttonValue = self.button.value()
        
        return xValue, yValue, buttonValue
