<b>ESP32-Runway Light by Mark Harris<br>
Version 1.2 </b><p>

![alt text](https://github.com/markyharris/MicroPython-Projects/blob/main/ESP32%20Runway%20Light/Pics/Runway%20Light%206.jpg?raw=true)
        
This project uses an ESP32 to drive addressable LED's that are strung around a 'bulb' inside the lens of an airport runway light.<br>
The bulb holds the ESP32 inside and the LED's are run on the outside, held in place with a little hot glue.<br>
The ESP32 seems very capable of supplying the needed power for the string of 50 LED's without an extra power supply. The whole thing is powered off 
the USB cable alone.<p>
  
Below are links to to the various components.<br>
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
   <ul><li>micropython-xml.etree.ElementTree<br>
   <li>micropython-xmltok2<br>
   <li>micropython-urequests
</ul><p>

This version includes;<br>
   <ul><li>WifiManager - https://randomnerdtutorials.com/esp32-wi-fi-manager-asyncwebserver/<br>
   <li>Dimming (or off) between two times, for night operations if desired<br>
   <li>Lightning display if lightning is reported in the METAR<br>
   <li>Display high winds by blinking led's if winds above threshold<br>
   <li>Can use either RGB LED's (WS2812) or GRB LED's (WS2811)
</ul><p>

Configure Software<br>
Copy the files in repository to ESP32. '/Pics' folder and 'Runway Light Metar STL Files' are not necessary.<br>
Open 'airports.py' and fill in the needed information. The format is 'PIN Number:Airport ID'<br>
Open 'config.py' and change the variables and colors to suit your needs.<p>

Depending on the Runway light being used, the STL files can be used to help complete the build by 3D printing the Bulb, Legs, and Lens Gasket.<p>
    
The /Pics directory provides examples of the build.<p>
    
