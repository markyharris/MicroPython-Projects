# ESP32-Runway Light by Mark Harris
# Version 1.2 
#
# Uses an ESP32 to drive addressable LED's,
#  Example ESP32
#    https://www.aliexpress.us/item/3256804928892251.html?spm=a2g0o.order_list.order_list_main.5.773d1802eZ3wP3&gatewayAdapt=glo2usa&_randl_shipto=US
#  Example Addressable LED's
#    https://www.adafruit.com/product/4560
#
# Use this to drive LED's inside the clear lens of a runway light.
# Here's a link to an example runway light;
#    https://www.ebay.com/itm/115559595023?mkcid=16&mkevt=1&mkrid=711-127632-2357-0&ssspo=nkjHLfN6TEK&sssrc=2047675&ssuid=TNlVSH4kTeK&widget_ver=artemis&media=COPY
#
# Install micropython onto ESP32.
#    https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/
#
# Use Thonny's 'Manage Packages' to install the following; (or use command line to install if desired).
#    micropython-xml.etree.ElementTree
#    micropython-xmltok2
#    micropython-urequests
#
# This version includes;
#    WifiManager - https://randomnerdtutorials.com/esp32-wi-fi-manager-asyncwebserver/
#    Dimming (or off) between two times, for night operations if desired
#    Lightning display if lightning is reported in the METAR
#    Display high winds by blinking led's if winds above threshold
#    Can use either RGB LED's (WS2812) or GRB LED's (WS2811)


# Imports
import wifimgr   # Complete wifimanager project details at https://RandomNerdTutorials.com
import time
import machine
import neopixel  # docs, https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
import xml.etree.ElementTree as ET # docs, https://pypi.org/project/micropython-xml.etree.ElementTree/
import urequests # docs, https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html
import gc        # https://docs.micropython.org/en/latest/library/gc.html
import ntptime


# Variables
airport ="KFLG"                   # Choose airport that reports METAR's. Use www.skyvector.com to be sure
hi_winds = 15                     # wind speed in kts to blink LED's
show_lightning = 1                # 1 = Yes, 0 = No. Flash yellow if lightning in area
show_hiwinds = 1                  # 1 = Yes, 0 = No. Blink led if winds are above 'hi_winds'
rgb_grb = 1                       # 1 = Use RGB color codes, 0 = Use GRB color codes
time_zone = -7                    # change to match location. Arizona = -7, Boston = -5
update_interval = 5               # in Minutes
dim_time = (21, 30, 0)            # Use 24 hour time. Set both times to the same to disable 
bright_time = (6, 30, 0)          # format (hours, minutes, seconds) No leading zeros
dim_brightness = 5                # in percentage of normal brightness, 0 to turn off led's
normal_brightness = 100           # 100% = max brightness
hi_wind_brightness = 10           # in %, brightness to blink if hi winds are above hi_winds
num_leds = 50                     # number of LED's in string
pin = 27                          # pin number used to address LED string
metar_age = 2.5                   # Longest acceptable age of metar returned by FAA in hours
wifi_led = machine.Pin(2, machine.Pin.OUT)
url = f"https://aviationweather.gov/api/data/dataserver?requestType=retrieve&dataSource=metars&format=xml&mostRecent=true&mostRecentForEachStation=constraint&hoursBeforeNow="+str(metar_age)+"&stationString="
debug = 0                         # 1 = cycle through each wx color to determine if colors look proper


# Thunderstorm and lightning METAR weather description codes that denote lightning in the area.
wx_lghtn_ck = ["TS", "TSRA", "TSGR", "+TSRA", "TSRG", "FC", "SQ", "VCTS", "VCTSRA", "VCTSDZ", "LTG"]


# Constants
VFR_COLOR = (0, 255, 0)           # GREEN 
MVFR_COLOR = (0,0,255)            # BLUE
IFR_COLOR = (255, 0, 0)           # RED
LIFR_COLOR = (153, 0, 153)        # MAGENTA
NOWX_COLOR = (15,15,15)           # GREY
LIGHTNING_COLOR = (200, 200, 10)  # YELLOW
OFF_COLOR = (0, 0, 0)             # BLACK
WHITE = (255, 255, 255)           # WHITE

COLOR_LIST = [VFR_COLOR, MVFR_COLOR, IFR_COLOR, LIFR_COLOR, NOWX_COLOR]
FC_LIST = ["VFR", "MVFR", "IFR", "LIFR", "NOWX"]


# Set instance of neopixel
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)


# Garbage Collection
gc.enable()      # garbage collecting to speed things up?
gc.collect()     # force collection to start


# Routines
def time_in_range(start, end, x): # See if a time falls within a range
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def dim_leds(brightness, color):
    if brightness > 0:
        brightness = brightness/100 # change from percentage to decimal
    r,g,b = color
    if r > 0:
        r = r * brightness
    if g > 0:
        g = g * brightness
    if b > 0:
        b = b * brightness
    color = (int(r),int(g),int(b))
    return(color)


# Rainbow Animation function, Altered - taken from https://github.com/JJSilva/NeoSectional/blob/master/metar.py
def rainbowCycle(strip=np, iterations=3, wait=.001):
    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    for j in range(256*iterations):
        for led_pin in range(num_leds):
            np[led_pin]=(dim_leds(get_brightness(),(wheel((int(led_pin * 256 / num_leds) + j) & 255))))
        np.write()
        time.sleep(wait/100)
        

def fade(start_color=WHITE, delay=.02):
    for j in range(num_leds):
        r,g,b = start_color
        
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
            color = (r,g,b)
            np[j] = dim_leds(get_brightness(), color)
        np.write()
    time.sleep(.5)
        

def get_fc_color(data):
    if data not in FC_LIST:
        pin_color = NOWX_COLOR
    else:
        for j in range(len(FC_LIST)):
            if data == FC_LIST[j]:
                pin_color = COLOR_LIST[j]
    return(rgbgrb(pin_color))
    

def set_wifi(): # Uses wifimgr.py
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
        
    
def get_brightness():
    global hour, min, sec 
    # Check time of day to see if it should be dimmed or not
    y,m,md,hour,min,sec,wd,yd = time.localtime(time.time() + UTC_OFFSET) #time.localtime()
    if time_in_range(dim_time, bright_time, (hour,min,sec)):
        default_brightness = dim_brightness
    else:
        default_brightness = normal_brightness
    return(default_brightness)


def show_lightning():
    if show_lightning == 0:
        return
    
    # Display Lightning if present in wxstring
    for iter in range(2):
        if wxstring in wx_lghtn_ck:
            clear()
            for j in range(num_leds):
                np[j] = dim_leds(get_brightness(), LIGHTNING_COLOR)
            np.write()
            time.sleep(.2)
            
    for j in range(num_leds):        
        np[j] = dim_leds(get_brightness(), get_fc_color(flight_category))
    np.write()
    time.sleep(2)


def show_hiwinds():
    if show_hiwinds == 0:
        return
    
    global wind_speed
    if int(wind_speed) >= hi_winds:
        r,g,b = get_fc_color(flight_category)
        dr = r * hi_wind_brightness/100
        dg = g * hi_wind_brightness/100
        db = b * hi_wind_brightness/100
        dim_color = (int(dr),int(dg),int(db))
#                print(dim_color) # debug
        for j in range(num_leds):
            np[j] = dim_leds(get_brightness(), dim_color)                    
        np.write()
        time.sleep(1)
            
        for j in range(num_leds):        
            np[j] = dim_leds(get_brightness(), get_fc_color(flight_category))
        np.write()
        time.sleep(1)


def rgbgrb(color):
    if rgb_grb:
        return(color)
    
    r,g,b = color
    xcolor = (g,r,b)
    return(xcolor)


def debug_color():
    if debug == 1:
        for color in COLOR_LIST:
            for j in range(num_leds):        
                np[j] = dim_leds(get_brightness(), color)
            np.write()
            time.sleep(2)
    else:
        return


# Start of Executed Code
if __name__ == "__main__":
    set_wifi()
    
    #Set Time server info
    UTC_OFFSET = time_zone * 60 * 60  # Change the first number to match your timezone
    ntptime.host = "us.pool.ntp.org"  #"1.europe.pool.ntp.org"
    #print("Local time before synchronization：%s" %str(time.localtime())) # debug
    try:
        ntptime.settime()
    except:
        print("Internet Not Available Yet. Will Reboot in 60 sec")
        time.sleep(60)
        machine.reset()

    #print("Local time after synchronization：%s" %str(time.localtime())) # debug

    print("ESP32-Runway Light\n"+"Ctrl-C to Exit"+"\n")
    clear()
    debug_color() # will only run if 'debug = 1'
    rainbowCycle(np,1)

    try: # Comment out when needed to diagnose errors
#    while True: # Uncomment when needed to diagnose errors
        while True:
            fade()
            flight_category = "NOWX"          # Initialize flight category, assuming no weather reporting
            station_id = ""
            wxstring = ""                     # Initialize wxstring
            wind_speed = "0"
            
            # Get Metar Data from FAA
            f = urequests.get(url+airport).text
            root = ET.fromstring(f)
            print(f) # debug, view raw XML data returned

            for j in range(int(root[6].attrib['num_results'])): # Get num or results to iterate
                for metar in root[6][j]:      # will grab an individual airport's data
                    if metar.tag == 'station_id':
                        station_id = metar.text
                    if metar.tag == 'flight_category':
                        flight_category = metar.text
                    if metar.tag == 'wx_string':
                        wxstring = metar.text
                    if metar.tag == 'wind_speed_kt':
                        wind_speed = metar.text

                if station_id != "" or flight_category != "":
                    print(station_id, "is", flight_category)
                else:
                    print(airport,"is not reporting")
                    
                # Standard Output
                if wxstring != "":
                    print("Weather String = "+str(wxstring))
                str_min = str(min)
                str_hour = str(hour)
                if len(str_min) < 2:
                    str_min = "0"+str_min
                if len(str_hour) < 2:
                    str_hour = "0"+str_hour
                print("Time = "+str_hour+":"+str_min)

            timeout_start = time.time() # Set current moment we enter this code
            while time.time() < timeout_start + (update_interval * 60): # Cycle through this until update needed

                # Display flightcategory data on all LED's in string
                for j in range(num_leds):
                    np[j] = dim_leds(get_brightness(), get_fc_color(flight_category))
                np.write()            
                time.sleep(4)

                show_lightning()
                show_hiwinds()

    except KeyboardInterrupt:
        clear()
        print("\nKeyboard Interrupt Received")
        print("\nExiting Program")
        
    except Exception as e: # Reset controller and see if issue is temporary
        clear()
        print("\nResetting ESP32 in 1 minute")
        print("\nException:\n",e)
        timeout_start = time.time() # Set current moment we enter this code
        while time.time() < timeout_start + (60): # Cycle through this until update needed
            fade()
            time.sleep(1)
#        time.sleep(60)
        machine.reset()


