# ESP32 Runway Light by Mark Harris
# Version 1.0
# Uses an ESP32 to drive addressable LED's
# Visit www.livesectional.com for build details
#
# upip docs; https://docs.micropython.org/en/latest/reference/packages.html
# import upip
# upip.install ("install micropython-xml.etree.ElementTree")
# upip.install("micropython-xmltok2")


# Imports
import wifimgr # Complete wifimanager project details at https://RandomNerdTutorials.com
import time
import machine
import neopixel
import xml.etree.ElementTree as ET # docs, https://pypi.org/project/micropython-xml.etree.ElementTree/
import urequests # docs, https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html
import gc
gc.collect() # garbage collecting to speed things up?

# Variables
airports ="KFLG" 
wifi_led = machine.Pin(2, machine.Pin.OUT)
update_interval = 5 # in Minutes
num_leds = 50       # number of LED's in string
pin = 27            # pin number used to address LED string
metar_age = 2.5
url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow="+str(metar_age)+"&stationString="
flight_category = "VFR"
 
# Constants
VFR_COLOR = (0, 255, 0)    # GREEN
MVFR_COLOR = (0,0,255)     # BLUE
IFR_COLOR = (255, 0, 0)    # RED
LIFR_COLOR = (255, 0, 255) # MAGENTA
NOWX_COLOR = (15,15,15)    # GREY
LIGHTNING_COLOR = (200, 200, 10) # YELLOW
OFF_COLOR = (0, 0, 0)      # BLACK
WHITE = (255, 255, 255)    # WHITE

COLOR_LIST = [VFR_COLOR, MVFR_COLOR, IFR_COLOR, LIFR_COLOR, NOWX_COLOR]
FC_LIST = ["VFR", "MVFR", "IFR", "LIFR", "NOWX"]

# Set instance of neopixel
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

# Routines
# Rainbow Animation function - taken from https://github.com/JJSilva/NeoSectional/blob/master/metar.py
def rainbowCycle(strip=np, iterations=3, wait=.01):
    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    nullpins = []
    for j in range(256*iterations):
        for led_pin in range(num_leds):
            if str(led_pin) in nullpins:        #exclude NULL and LGND pins from wipe
                np[led_pin]=(OFF_COLOR)
            else:
                np[led_pin]=(wheel((int(led_pin * 256 / num_leds) + j) & 255))
        np.write()
        time.sleep(wait/100)
        

def fade(start_color=WHITE, delay=.05):
    for j in range(num_leds):
        r,g,b = start_color
        np[j] = (r,g,b)       
        np.write()
        
    for x in range(52):
        time.sleep(delay)
        r = r - 5
        g = g - 5
        b = b - 5
        if r <= 0:
            r = 0
        if g <= 0:
            g = 0
        if b <= 0:
            b = 0
        
        for j in range(num_leds):
            np[j] = (r,g,b)
        np.write()
    time.sleep(.5)
        

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
            pass
    else:
        wifi_led.value(1)


def clear(color=OFF_COLOR):
    for j in range(num_leds):
        np[j] = color
        np.write()
    

# Start of Executed Code
set_wifi()
print("ESP32-Runway Light\n"+"Ctrl-C to Exit"+"\n")

clear()
rainbowCycle(np,1)

try:
    while True:
        fade()
        
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
            print("Local time:", time.localtime())

        # Display flightcategory data on all LED's in string
        for j in range(num_leds):
            np[j] = get_fc_color(flight_category)
        np.write()
        
        time.sleep(update_interval * 60)

except:
    clear()
    print("\nExiting Program")
