# config.py
# change the variables below to create the behavior desired

# User Variables
hi_winds = 15                     # High winds threshold in kts to blink leds.
show_lightning = 1                # 1 = Yes, 0 = No. Flash yellow if lightning in area
show_hiwinds = 1                  # 1 = Yes, 0 = No. Blink led if winds are above 'hi_winds'
show_wxstring = 1                 # 1 = Yes, 0 = No. Display color to represent weather type
rgb_grb = 1                       # 1 = Use RGB color codes, 0 = Use GRB color codes
time_zone = -7                    # change to match location. Arizona = -7, Boston = -5
update_interval = 5               # how often to update the METAR data; in Minutes
dim_time = (21, 30, 0)            # Use 24 hour time. Set both times to the same to disable dimming
bright_time = (6, 30, 0)          # format (hours, minutes, seconds) No leading zeros
dim_brightness = 5                # in percentage of normal brightness, 0 to turn off led's
normal_brightness = 100           # 100% = max brightness
hi_wind_brightness = 10           # how bright the airport gets dimmed to when winds are above hi_winds
pin = 27                          # pin number used to address LED string
metar_age = 2.5                   # Longest acceptable age of metar returned by FAA in hours
debug = 0                         # 1 use debug list, 0 don't use it.


# LED Color Constants
VFR_COLOR = (0, 255, 0)           # GREEN 
MVFR_COLOR = (0,0,255)            # BLUE
IFR_COLOR = (255, 0, 0)           # RED
LIFR_COLOR = (255, 0, 255)        # MAGENTA
NOWX_COLOR = (15,15,15)           # GREY
LIGHTNING_COLOR = (255, 255, 0)   # YELLOW
OFF_COLOR = (0, 0, 0)             # BLACK
WHITE = (255, 255, 255)           # WHITE

RAIN = (4, 0, 54)                 # DARK BLUE
FRRAIN = (68, 0, 124)             # DK PURPLE
SNOW = (255, 255, 255)            # WHITE
DUST = (101, 35, 2)               # BROWN
FOG = (30, 30, 45)                # DK GREY


# Debug list allows for testing of features without relying on live weather data. 
debug_list = {
              0: ('KDVT', (0, 255, 0), '4', '-RA BR'), 1: ('KSDL', (0, 255, 0), '3', '-SN BR'),\
              2: ('KLUF', (0, 255, 0), '6', 'FZRA'), 3: ('KGEU', (0, 255, 0), '6', 'DU'),\
              4: ('KBXK', (0, 255, 0), '4', 'BR'), 5: ('KGYR', (0, 255, 0), '6', 'TS'),\
              6: ('KPHX', (0, 255, 0), '16', 'VCTS'), 7: ('KFFZ', (0, 255, 0), '0', ''),\
              8: ('KCHD', (0, 255, 0), '30', ''), 9: ('KIWA', (0, 255, 0), '0', ''),\
              10: ('KP08', (0, 255, 0), '20', ''), 11: ('KCGZ', (15, 15, 15), '0', ''),\
              12: ('KA39', (0, 255, 0), '15', ''), 13: ('KGXF', (0, 0, 255), '7', '')
              }
