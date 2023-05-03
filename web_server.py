import network
import socket
from time import sleep
import time
from picozero import pico_temp_sensor, pico_led, Button
import machine

ssid = 'huaweip40'
password = '123456azx'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta http-equiv="refresh" content="1"/>
            </head>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def getTemp():
    adc = machine.ADC(4)
    ADC_voltage = adc.read_u16() * (3.3 / (65535))
    temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
    temp_fahrenheit=32+(1.8*temperature_celcius)
    return temperature_celcius, temp_fahrenheit
    
def serve(connection):
    #Start a web server
    state = 'OFF'
    led = machine.Pin("LED", machine.Pin.OUT)
    led.off()

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        
        temperature = getTemp()
        
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led.on()
            state = 'ON'
        elif request == '/lightoff?':
            led.off()
            state = 'OFF'
            
        html = webpage(temperature, state)
        client.send(html)
        client.close()

try:
    led = machine.Pin("LED", machine.Pin.OUT)
    but = Button(15)
    
    #ip = connect()
    #connection = open_socket(ip)
    #serve(connection)
    while True:
        if but.is_pressed:
            print('yes')
            led.on()
            time.sleep(1)
        else:
            print('no')
            led.off()
            time.sleep(1)    
except KeyboardInterrupt:
    machine.reset()