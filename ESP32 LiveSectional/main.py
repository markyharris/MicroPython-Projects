# ESP32-LiveSectional Metar Map by Mark Harris
# Version 1.3
#
# Uses an ESP32 to drive addressable LED's,
#  Example ESP32
#    https://www.aliexpress.us/item/3256804928892251.html?spm=a2g0o.order_list.order_list_main.5.773d1802eZ3wP3&gatewayAdapt=glo2usa&_randl_shipto=US
#  Example Addressable LED's
#    https://www.adafruit.com/product/4560
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
#    Display Weather String as color, such as Rain, Snow etc.
#    Display a Legend for the Flight Category Colors. Must use these to denote a legend LED
#      "LG_VFR", "LG_MVFR", "LG_IFR", "LG_LIFR", "LG_NOWX": i.e. 0:"LG_VFR" in airport.py file
#
# Open file 'airports.py' and fill in required LED pin number and 4 character airport identifier
#
# Open file 'config.py' and alter user variables and colors to suit build


# Imports
import wifimgr   # Complete wifimanager project details at https://RandomNerdTutorials.com
import time
import machine
import neopixel  # docs, https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
import xml.etree.ElementTree as ET # docs, https://pypi.org/project/micropython-xml.etree.ElementTree/
import urequests # docs, https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html
import gc        # https://docs.micropython.org/en/latest/library/gc.html
import ntptime
import micropython
import sys
from airports import *
from config import *


# Various variables
num_leds = len(airports)          # number of LED's in string to use (# of airports)
wifi_led = machine.Pin(2, machine.Pin.OUT)
url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow="+str(metar_age)+"&stationString="


# Setup Needed Lists
COLOR_LIST = [VFR_COLOR, MVFR_COLOR, IFR_COLOR, LIFR_COLOR, NOWX_COLOR]
FC_LIST = ["VFR", "MVFR", "IFR", "LIFR", "NOWX"]
LG_LIST = ["LG_VFR", "LG_MVFR", "LG_IFR", "LG_LIFR", "LG_NOWX"]


# Weather String codes
# Thunderstorm and lightning METAR weather description codes that denote lightning in the area.
wx_lghtn_ck = ["TS", "TSRA", "TSGR", "+TSRA", "TSRG", "FC", "SQ", "VCTS", "VCTSRA", "VCTSDZ", "LTG"]
# Snow in various forms
wx_snow_ck = ["BLSN", "DRSN", "-RASN", "RASN", "+RASN", "-SN", "SN", "+SN", "SG", "IC", "PE", "PL", "-SHRASN", "SHRASN", "+SHRASN", "-SHSN", "SHSN", "+SHSN"]
# Rain in various forms
wx_rain_ck = ["-DZ", "DZ", "+DZ", "-DZRA", "DZRA", "-RA", "RA", "+RA", "-SHRA", "SHRA", "+SHRA", "VIRGA", "VCSH"]
# Freezing Rain
wx_frrain_ck = ["-FZDZ", "FZDZ", "+FZDZ", "-FZRA", "FZRA", "+FZRA"]
# Dust Sand and/or Ash
wx_dustsandash_ck = ["DU", "SA", "HZ", "FU", "VA", "BLDU", "BLSA", "PO", "VCSS", "SS", "+SS",]
# Fog
wx_fog_ck = ["BR", "MIFG", "VCFG", "BCFG", "PRFG", "FG", "FZFG"]


# Set instance of neopixel
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)


# Garbage Collection
gc.enable()      # garbage collecting to speed things up?


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
    for pin_num in flt_category: #wx_lightning:
        if flt_category[pin_num][3] in wx_lghtn_ck:
            np[pin_num] = dim_leds(get_brightness(), LIGHTNING_COLOR)
            np.write()
            time.sleep(.3)
            
            np[pin_num] = dim_leds(get_brightness(), flt_category[pin_num][1])
            np.write()
            time.sleep(.1)
            
            np[pin_num] = dim_leds(get_brightness(), LIGHTNING_COLOR)
            np.write()
            time.sleep(.7)
            
            np[pin_num] = dim_leds(get_brightness(), flt_category[pin_num][1])
            np.write()
            time.sleep(1)


def show_hiwinds():
    if show_hiwinds == 0:
        return
    
    for pin_num in flt_category:        
        if int(flt_category[pin_num][2]) >= hi_winds:
            r,g,b = flt_category[pin_num][1]
            dr = r * hi_wind_brightness/100
            dg = g * hi_wind_brightness/100
            db = b * hi_wind_brightness/100
            dim_color = (int(dr),int(dg),int(db))
#                print(dim_color) # debug
            np[pin_num] = dim_leds(get_brightness(), dim_color)
    np.write()
    time.sleep(1)
        
    for pin_num in flt_category:        
        if int(flt_category[pin_num][2]) >= hi_winds:
            color = flt_category[pin_num][1]
            np[pin_num] = dim_leds(get_brightness(), color)
    np.write()
    time.sleep(2)


def show_wxstring():
    if show_wxstring == 0:
        return
    
    for pin_num in flt_category:
        wx_split = flt_category[pin_num][3].split()
        if len(wx_split) == 0:
            wx_split = ["",""]
            
        # Check for Rain
        if  wx_split[0] in wx_rain_ck:
            np[pin_num] = dim_leds(get_brightness(), RAIN)            
        # Check for Snow
        elif  wx_split[0] in wx_snow_ck:
            np[pin_num] = dim_leds(get_brightness(), SNOW)            
        # Check for Freezing Rain
        elif  wx_split[0] in wx_frrain_ck:
            np[pin_num] = dim_leds(get_brightness(), FRRAIN)
        # Check for Fog            
        elif  wx_split[0] in wx_fog_ck:
            np[pin_num] = dim_leds(get_brightness(), FOG)
        # Check for Sand/Dust/Ash            
        if  wx_split[0] in wx_dustsandash_ck:
            np[pin_num] = dim_leds(get_brightness(), DUST)

    np.write()
    time.sleep(2)
        
    # Restore Flight Category Color
    for pin_num in flt_category:        
        color = flt_category[pin_num][1]
        np[pin_num] = dim_leds(get_brightness(), color)
    np.write()
    time.sleep(1)


def rgbgrb(color):
    if rgb_grb:
        return(color)
    
    r,g,b = color
    xcolor = (g,r,b)
    return(xcolor)


def show_legend():
    for pin_num in airports:
        if airports[pin_num] in LG_LIST:
#            print(airports[pin_num]) # debug
            index = LG_LIST.index(airports[pin_num])
            np[pin_num]  = dim_leds(get_brightness(),COLOR_LIST[index]) # help transition as new data is received
#            print(COLOR_LIST[index]) # debug
    np.write()


# Start of Executed Code
if __name__ == "__main__":
    set_wifi()
    
    #Set Time server info
    UTC_OFFSET = time_zone * 60 * 60
    ntptime.host = "us.pool.ntp.org"
    ntptime.settime()

    # Boot up stuff
    print("ESP32-LiveSectional Metar Map\n"+"Ctrl-C to Exit"+"\n")
    clear()
    fade()
    rainbowCycle(np,3)
    show_legend()

    try: # Comment out when needed to diagnose errors
#    while True: # Uncomment when needed to diagnose errors
        while True:            
            wx_lightning = {}
            flt_category = {}
#            clear()
#            rainbowCycle(np,3)
            gc.collect()     # force collection to start
#            micropython.mem_info(1) # https://forum.micropython.org/viewtopic.php?t=4912
            
            for pin_num in airports:
                if airports[pin_num] in LG_LIST: # skip if its a legend item
                    print(pin_num,"is a Legend LED;",airports[pin_num])
                    continue
                
                print(pin_num, airports[pin_num]) # debug
                np[pin_num]  = dim_leds(get_brightness(), WHITE) # help transition as new data is received
                np.write()
                
                # Get Metar Data from FAA
                f = urequests.get(url+airports[pin_num]).text
                root = ET.fromstring(f)

                # Check to see if a weather is being reported back from airport
                if int(root[6].attrib['num_results']) == 0:
                    print("NO WX PROVIDED")
                    flt_category[pin_num] = (airports[pin_num],NOWX_COLOR,"0","")

                for j in range(int(root[6].attrib['num_results'])): # Get num or results to iterate
                    # Re-Initialize variables
                    wxstring = ""                     # Initialize wxstring
                    flight_category = "NOWX"          # Initialize flight category, assuming no weather reporting
                    station_id = ""
                    wxstring = ""
                    wind_speed = "0"
                    wind_dir = "0"

                    for metar in root[6][j]:      # will grab an individual airports's data
                        if metar.tag == 'station_id':
                            station_id = metar.text
                            
                        if metar.tag == 'flight_category':
                            flight_category = metar.text

                        elif metar.tag == 'wx_string':
                            wxstring = metar.text
                            
                        elif metar.tag == 'wind_speed_kt':
                            wind_speed = metar.text
                            
                        elif metar.tag == 'wind_dir_degrees':
                            wind_dir = metar.text
                                
                    if station_id != "" or flight_category != "":
                        print(station_id, "is", flight_category)
                        print("Wind Speed:",str(wind_speed),"Wind Dir:",str(wind_dir))
                        
                    else:
                        print(station_id,"is not reporting")
                        flight_category = "NOWX"
                        
                    np[pin_num] = dim_leds(get_brightness(), get_fc_color(flight_category))
                    flt_category[pin_num] = (airports[pin_num],get_fc_color(flight_category),wind_speed,wxstring)
            np.write()
#            print(flt_category) # debug
            if debug == 1:
                flt_category = debug_list # debug
             
            # Print current time after updating all LED's
            str_min = str(min)
            str_hour = str(hour)
            if len(str_hour) < 2:
                str_hour = "0"+str_min
            if len(str_min) < 2:
                str_min = "0"+str_min
            print("Time = "+str_hour+":"+str_min+"\n")
                      
            timeout_start = time.time() # Set current moment we enter this code
            while time.time() < timeout_start + (update_interval * 60): # Cycle through this until update needed
                show_lightning()
                show_hiwinds()
                show_wxstring()
                time.sleep(2)


    except KeyboardInterrupt:
        clear()
        print("Keyboard Interrupt Received")
        print("\nExiting Program")
        
    except Exception as e: # Reset controller and see if issue is temporary
        clear()
        print("\nResetting ESP32 in 1 minute")
        print("Exception:\n",e)
        timeout_start = time.time() # Set current moment we enter this code
        while time.time() < timeout_start + (60): # Cycle through this until update needed
            fade()
            time.sleep(1)
        machine.reset()


        


