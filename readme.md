# Color Clock
This traffic-light clock was designed to help my daughter understand when she can get out of bed in the morning.  It has a simple design and a customizable schedule that can be programmed in the web interface.  This clock uses Python3 to control the GPIO Pins on the Raspberry Pi Zero and also run the simple web server.  This guide will give you all the software, inluding the OpenSCAD 3D model for the case, to allow you to create one of your own.  Just supply the hardware, print the case, and load the software.

![Color Clock](/images/1.png)

![Color Clock Parts](/images/2.png)

## Hardware Needed
* Rasberry Pi Zero W V1.1 [https://amzn.to/2YNBUNQ](https://amzn.to/2YNBUNQ)
* Low Voltage Labs Traffic Light [https://amzn.to/2MVWmtl](https://amzn.to/2MVWmtl)

## Soldering
You may be able to get by without soldering, but I soldered the wires onto my board.  I used GPIO spots GND/17/27/22

## Case and Assembly
Once soldered, put the traffic lights onto the wires.  With the lights facing towards the USB/HDMI ports, insert the wires in sequence to the traffic light.  While slightly pushing down, twist the traffic light 180 degrees, facing away from the ports.  Place the PI Zero into the base of the case.  Fit the traffic light into the hole in the top part of the case, and then snap the top down onto the base.  Then, gently press the LEDs into the holes on the front.  Once it is securely in place, fit the back of the light tower on.

## Getting the Pi ready for booting
1. Download the latest image for your pi at [www.raspberrypi.org](https://www.raspberrypi.org/software/operating-systems/)

1. Use software, such as [Etcher](https://www.balena.io/etcher/), to burn the image onto the SDCard

1. Re-insert the SDCard into your computer (where you burned the image) and browse to the /boot directory on the card

1. Create an empty file called `ssh`
1. Create a file called `wpa_supplicant.conf`
```
country=US
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
 scan_ssid=1
 ssid="YOUR_NETWORK_SSID"
 psk="your_password"
}
```

## Boot the Pi
Boot the pi with the SDCard card inside.  When it comes online, it will have SSH enabled.  If it does not connect, be sure you have the SSID and PSK correct for your wireless.  

SSH into the machine, using `raspberry` as the default password
```
#ssh pi@ip_address
#example:
ssh pi@192.168.1.100
```
Make sure to fully update your pi
```
sudo apt update
sudo apt -y upgrade
```
Install Pip and Git
```
sudo apt -y install python3-pip git
```
Clone this repo
```
https://github.com/ralphyz/color_clock.git
```
Install the required Python modules
```
cd color_clock
pip -r install requirements.txt
```
Get the JavaScript Libraries
```
curl https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js -o js/jquery.min.js
curl https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js -o js/jquery-ui.min.js -o js/jquery-ui.min.js
curl https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js -o js/jquery.mobile.min.js
curl https://raw.githubusercontent.com/loebi-ch/jquery-clock-timepicker/master/jquery-clock-timepicker.min.js -o js/jquery-clock-timepicker.min.js
curl https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css -o css/jquery-ui.css
curl https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css -o css/jquery.mobile.min.css
curl https://unpkg.com/purecss@2.0.5/build/pure-min.css -o css/pure-min.css

```

Schedule the program to run when the unit is rebooted:
```
crontab -l > mycron && echo "@reboot /usr/bin/python3 /home/pi/color_clock/app.py 2>/dev/null" >> mycron && crontab mycron && rm mycron
```
Reboot to start the clock!
```
sudo reboot
```

## Web Server
Once the pi reboots, you should be able to browse to the web server in any browser by typing in the IP Address.  From the page you will see, you can touch a LED to enable that color.  When a color is enabled and it is not the scheduled time for that color, the "Temporary Override" button will turn on.  You can click it off, or you can select a different LED.  

You may also select the Schedule Tab, and set the schedule for the light changes.


## Conclusion
I hope this small project helps someone else.  It was fun to write, and fun to see my daughter use.

