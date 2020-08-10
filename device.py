################################################################################
# BLE Scanner
#
# Created by Zerynth Team 2019 CC
# Author: G. Baldi
###############################################################################

import streams
# import a BLE driver: in this example we use NRF52
# from nordic.nrf52_ble import nrf52_ble as bledrv
from espressif.esp32ble import esp32ble as bledrv
# then import the BLE modue
from wireless import ble
from worldsemi.ws2812 import ledstrips as pixel

import timers
import gc

streams.serial()

notifications_enabled = True
connected = False
scan_time=1000
mylist=[]
scanned_list = []
counter = 0
_isSend = False
_isStop = False

num_leds = 1                     # adjust this to match the number of LEDs on your strip

led_pin = D27                      # this should match the data pin of the LED strip

leds = pixel.LedStrip(led_pin, num_leds)
leds.on()
leds.set_fading(100, 0, 0) 

def set_standby_led():
    leds.clear()
    leds[0] = (50, 50, 50)
    leds.on()

def set_connect_led():
    leds.clear()
    leds[0] = (50, 0 ,0)
    leds.on()

def set_disconnect_led():
    leds.clear()
    leds[0] = (0, 50 ,0)
    leds.on()
    

def set_send_led():
    leds.clear()
    leds[0] = (0, 0 ,50)
    leds.on()
# How long to scan for in milliseconds

def receive_cb(status, data):
    global _isSend
    global notifications_enabled
    if int(data) == 1:
        _isSend = True
        print(_isSend)

def connected_cb(address):
    global connected
    print(ble.btos(address))
    connected = True
    set_connect_led()
    
def disconnected_cb(address):
    global connected
    print(ble.btos(address))
    ble.start_advertising()
    connected = False
    set_disconnect_led()

def scan_report_cb(data):
    global scanned_list
    scanned_time = int(timers.now() / 1000)
    rssi = -int(data[2]) 
    data_save = {
        "identifier": data[4],
        "timestamp":scanned_time,
        "rssi":rssi
    }
    scanned_list.append(data_save)
    
def scan_start_cb(data):
    global _isStop
    _isStop = False

def scan_stop_cb(data):
    global _isStop
    _isStop = True
    gc.collect()
    #let's start it up again

try:
    # initialize BLE driver
    bledrv.init()
    
    # Set GAP name and no security
    ble.gap("ct2",security=(ble.SECURITY_MODE_1,ble.SECURITY_LEVEL_1))

    ble.add_callback(ble.EVT_CONNECTED, connected_cb)
    ble.add_callback(ble.EVT_DISCONNECTED, disconnected_cb)


    service_object_transfer = ble.Service(0x1825)
    
    characteristic_object_changed = ble.Characteristic(0x2AC8, ble.NOTIFY | ble.READ,16,"Object Changed",ble.BYTES)

    characteristic_object_control = ble.Characteristic(0x2AC5, ble.WRITE ,1,"Object Control Point",ble.BYTES)
    
    service_object_transfer.add_characteristic(characteristic_object_changed)
    service_object_transfer.add_characteristic(characteristic_object_control)
    
    characteristic_object_control.set_callback(receive_cb)
    
    ble.add_service(service_object_transfer)
    
    
    #set scanning parameters: every 100ms for 50ms and no duplicates

    ble.advertising(50)
    
    # Start the BLE stack
    
    ble.add_callback(ble.EVT_SCAN_REPORT,scan_report_cb)
    ble.add_callback(ble.EVT_SCAN_STOPPED,scan_stop_cb)
    
    ble.scanning(100,50,duplicates=0)    

    ble.start()
    ble.start_advertising()

    # Now start scanning for 30 seconds
    ble.start_scanning(scan_time)
    
except Exception as e:
    print(e)


set_standby_led()

# loop forever
while True:
    global counter
    if _isSend and notifications_enabled and connected:
        set_send_led()
        value = bytearray(characteristic_object_changed.get_value())
        if len(scanned_list) != 0:
            for data in scanned_list:
                full_data = str(data["identifier"]) +","+ str(data["timestamp"])+","+ str(data["rssi"])
                value[0:len(full_data)] = full_data
            # set the new value. If ble notifications are enabled, the connected device will receive the change
                characteristic_object_changed.set_value(value)
            scanned_list = []
            _isSend = False
            value[0] = 0x06
            value[1] = 0x17
            characteristic_object_changed.set_value(value)
        _isSend = False
    

    sleep(5000)    
    if connected:
        set_connect_led()
    else:
        set_standby_led()
    counter+=1
    if (counter % 3) == 0:
        if _isStop:
            ble.start_scanning(scan_time)
            
