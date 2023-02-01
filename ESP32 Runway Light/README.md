README.md
ESP32-Runway Light by Mark Harris
Version 1.2 

Uses an ESP32 to drive addressable LED's,
 Example ESP32
   https://www.aliexpress.us/item/3256804928892251.html?spm=a2g0o.order_list.order_list_main.5.773d1802eZ3wP3&gatewayAdapt=glo2usa&_randl_shipto=US
 Example Addressable LED's
   https://www.adafruit.com/product/4560

Use this to drive LED's inside the clear lens of a runway light.
Here's a link to an example runway light;
   https://www.ebay.com/itm/115559595023?mkcid=16&mkevt=1&mkrid=711-127632-2357-0&ssspo=nkjHLfN6TEK&sssrc=2047675&ssuid=TNlVSH4kTeK&widget_ver=artemis&media=COPY

Install micropython onto ESP32.
   https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/

Use Thonny's 'Manage Packages' to install the following; (or use command line to install if desired).
   micropython-xml.etree.ElementTree
   micropython-xmltok2
   micropython-urequests

This version includes;
   WifiManager - https://randomnerdtutorials.com/esp32-wi-fi-manager-asyncwebserver/
   Dimming (or off) between two times, for night operations if desired
   Lightning display if lightning is reported in the METAR
   Display high winds by blinking led's if winds above threshold
   Can use either RGB LED's (WS2812) or GRB LED's (WS2811)
