import network
from time import sleep

SSID = "hua"
SSI_PASSWORD = "123456vvv"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, SSI_PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
print("Connecting to your wifi...")
do_connect()