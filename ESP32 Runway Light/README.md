README.md<br>
ESP32-Runway Light by Mark Harris<br>
Version 1.2 <p>
 
<p align="center">
<img src="/Pics/Runway%20Light%206.jpg?raw=true)
</p>
          
Uses an ESP32 to drive addressable LED's,<br>
 Example ESP32<br>
   https://www.aliexpress.us/item/3256804928892251.html?spm=a2g0o.order_list.order_list_main.5.773d1802eZ3wP3&gatewayAdapt=glo2usa&_randl_shipto=US<br>
 Example Addressable LED's<br>
   https://www.adafruit.com/product/4560<p>

Use this to drive LED's inside the clear lens of a runway light.<br>
Here's a link to an example runway light;<br>
   https://www.ebay.com/itm/115559595023?mkcid=16&mkevt=1&mkrid=711-127632-2357-0&ssspo=nkjHLfN6TEK&sssrc=2047675&ssuid=TNlVSH4kTeK&widget_ver=artemis&media=COPY<p>

Install micropython onto ESP32.<br>
   https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/<p>

Use Thonny's 'Manage Packages' to install the following; (or use command line to install if desired).<br>
   micropython-xml.etree.ElementTree<br>
   micropython-xmltok2<br>
   micropython-urequests<p>

This version includes;<br>
   WifiManager - https://randomnerdtutorials.com/esp32-wi-fi-manager-asyncwebserver/<br>
   Dimming (or off) between two times, for night operations if desired<br>
   Lightning display if lightning is reported in the METAR<br>
   Display high winds by blinking led's if winds above threshold<br>
   Can use either RGB LED's (WS2812) or GRB LED's (WS2811)<br>
