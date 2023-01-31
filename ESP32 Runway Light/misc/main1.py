# ESP32 LiveSectional by Mark Harris
# Beta 1
# Uses an ESP32 to drive addressable LED's
# Visit www.livesectional.com for build details

# upip docs; https://docs.micropython.org/en/latest/reference/packages.html
# import upip
# upip.install ("install micropython-xml.etree.ElementTree")
# upip.install("micropython-xmltok2")

# Imports
# Complete wifimanager project details at https://RandomNerdTutorials.com
import wifimgr
import time
import machine
try:
  import usocket as socket
except:
  import socket
import neopixel
import random
import xml.etree.ElementTree as ET # docs, https://pypi.org/project/micropython-xml.etree.ElementTree/
import urequests # docs, https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html
import gc
import sys

gc.collect() # garbage collecting to speed things up?

# Constants
VFR_COLOR = (0, 255, 0)    # GREEN
MVFR_COLOR = (0,0,255)     # BLUE
IFR_COLOR = (255, 0, 0)    # RED
LIFR_COLOR = (255, 0, 255) # MAGENTA
NOWX_COLOR = (15,15,15)    # GREY
LIGHTNING_COLOR = (200, 200, 10) # YELLOW
OFF_COLOR = (0, 0, 0)
COLOR_LIST = [VFR_COLOR, MVFR_COLOR, IFR_COLOR, LIFR_COLOR, NOWX_COLOR]
FC_LIST = ["VFR", "MVFR", "IFR", "LIFR", "NOWX"]

# Variables
wifi_led = machine.Pin(2, machine.Pin.OUT)
delay = .1
num_leds = 50 # number of LED's in string
pin = 27 # pin number used to address LED string
metar_age = 2.5
airports ="KBST" #,KPHX,KSEZ,KGEU,KINW"
url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow="+str(metar_age)+"&stationString="
flightcategory = "VFR"

# Set instance of neopixel
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

# Routines
def get_fc_color(data):
    if data not in FC_LIST:
        pin_color = NOWX_COLOR
    else:
        for j in range(len(FC_LIST)):
            if data == FC_LIST[j]:
                pin_color = COLOR_LIST[j]
    return(pin_color)
    

def set_wifi():
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        wifi_led.value(0)
        while True:
            pass  # you shall not pass :D
    else:
        wifi_led.value(1)


def clear(color=OFF_COLOR):
    for j in range(num_leds):
        np[j] = color
        np.write()
    

# Start of Executed Code
set_wifi()

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP32-LiveSectional")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get Metar Data from FAA
flight_category = NOWX_COLOR
f = urequests.get(url+airports).text
root = ET.fromstring(f)
for j in range(int(root[6].attrib['num_results'])): # Get num or results to iterate
    for metar in root[6][j]: # will grab an individual airport's data
        if metar.tag == 'station_id':
            station_id = metar.text
        if metar.tag == 'flight_category':
            flight_category = metar.text
    print(station_id, "is", flight_category)

#sys.exit()
clear()
# Display flightcategory data on LED's
for j in range(num_leds):
    np[j] = get_fc_color(flight_category) #random.choice(COLOR_LIST)
np.write()
#    time.sleep(delay)
#    print(j)
#    np[j] = OFF_COLOR
#    np.write()

# check internet availability and retry if necessary. If house power outage, map may boot quicker than router.
#while True:
#    set_wifi()
#    s = _socket.socket()
#    ai = socket.getaddrinfo('8.8.8.8', 0)
#    addr = ai[0][-1]
#    print(addr)

#    ipadd = socket.getsocketname()
#    print(ipadd)
