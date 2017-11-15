# RouteryPi

## Summary

RouteryPi is a WiFi access point based on a Raspberry Pi Zero W. Together with a pretty case and some status LEDs it makes a really nice alternative to a commercial AP because of easy programming and customization. The only downside of using a Raspberry Pi is it's relatively slow networking speed compared to high quality retail APs - nevertheless it has great potential and makes an even better addition if you want to upgrade some generic old AP that you found in your basement!

## Hardware

You will need the following parts for this project:
- A neat looking case maybe with holes for status lights. Reusing an old router case would be ideal here (Yay, upcycling!)
- A Raspberry Pi Zero W
- An OTG Ethernet Adapter (USB 2.0)
- A MicroSD card (anything class 6 and higher will do actually)
- A good power supply and connector (1A more than enough!)
- Some wire to connect everything

Optional:
- Some LEDs and resistors if you want status LEDs
- A push button to reset the Pi
- On/Off switch (to kill the power obviously)
- A heatsink - not needed, but your Pi will thank you

## Specs

**Raspberry Pi Zero W:**
- 1GHz, single-core CPU
- 512MB RAM
- USB OTG port (2.0)
- 802.11 b/g/n 2.4 GHz wireless LAN
- 40 GPIO pins
- Some other stuff, that's not relevant to this project. For full specs visit https://www.raspberrypi.org/products/raspberry-pi-zero-w/

**OTG Ethernet:**
- USB 2.0 OTG to 10/100 Fast Ethernet
- Standard RJ45 Ethernet port
- No external power required
- Link and Activity LEDs
- More info about the one I bought, at https://plugable.com/products/usb2-otge100/

## Software

This build uses the latest version of Raspbian which is Raspbian Stretch. You can download it on the official Raspberry Pi website, at https://www.raspberrypi.org/downloads/raspbian/. I guess you already know how to flash the image onto the SD Card - if you don't however, have a look at this tutorial: https://www.raspberrypi.org/documentation/installation/installing-images/

You will also need Python (my scripts use 2.7) if you have some LEDs and want to easily program them like status LEDs.
If you aim to do something like that be ready to also install python-pip and some packages like psutil.

The heart of this whole installation will be 'hostapd' and 'bridge-utils' because we will be using the Pi as a network bridge between the LAN and WiFi. This means that **you will need an additonal DHCP and DNS server**. Nevertheless, this simplifies the whole installation a lot and makes it less error-prone. If you already have a router (which I assume you do) you can connect it with your RouteryPi and everything will work out of the box.

Note: You will need **no additional drivers** at all!

## Installation

**Preparation**

The first step is, obviously, to install the image onto the SD Card and booting it up. The first boot usually takes longer than a normal startup because the Pi has to do stuff like generating new SSH keys and so on.

Then use ```sudo raspi-config``` to configure the Pi to your likings.

Now update it using ```sudo apt update && sudo apt full-upgrade``` - once it's done reboot it and we'll start with the actual AP installation.

**AP setup**

Firstly, install hostapd and bridge-utils with the following command.
```
sudo apt install hostapd bridge-utils
```

Now comes the important part. The next step is editing the hostapd.conf.
```
sudo nano /etc/hostapd/hostapd.conf
```

If the file is not empty just delete it's content. We will be using a custom config anyways. The minimal config that you should use looks like that:
```
# Bridge mode
bridge=br0

# Networking interface
interface=wlan0

# WiFi configuration
ssid=RouteryPi
channel=1
hw_mode=g
country_code=US
ieee80211n=1
ieee80211d=1
wmm_enabled=1

# WiFi security
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=YourCustom!PassWordWhichShou1dBePrettyStronG123$%
```
Just paste the text into the hostapd config file, edit ```country_code=US``` to your country, save it and you're good to go.

To create and use the network bridge we only have to edit one more file. Now edit the network interfaces file like that:
```
sudo nano /etc/network/interfaces
```

Delete anything that's in here and paste the following configuration:
```
auto lo
iface lo inet loopback

# Ethernet
auto eth0
allow-hotplug eth0
iface eth0 inet manual

# WiFi
auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
wireless-power off

# Bridge
auto br0
iface br0 inet dhcp
bridge_ports eth0 wlan0
bridge_fd 0
bridge_stp off
```
This will result in the Pi using DHCP which means it can be used in **any** network. The downside of this is that you have to find out the IP address if you want to, let's say, use SSH. You could use a static IP address by changing the **br0**(!) interface config a little bit - just google 'static ip raspberry pi'. (For the lazy: https://duckduckgo.com/?q=static+ip+raspberry+pi)

**Final steps**

After you did a quick reboot using ```sudo reboot```, you can start testing the whole thing. To test the hostapd config use this command: ```sudo hostapd /etc/hostapd/hostapd.conf```. Note: If it does exit without you doing something, then there is something wrong with it. To go into debug mode use ```sudo hostapd -dd /etc/hostapd/hostapd.conf```.

While testing the hostapd config you can also try connecting as a client. If you've done everything correctly you should be able to do so without any problems.

To enable hostapd to run upon boot you have to edit one last file.
```
sudo nano /etc/default/hostapd
```

Now paste this text into the file and save it:
```
RUN_DAEMON=yes
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

You're ready to go! From now on hostapd will start whenever your Pi boots up. If you're working with status LEDs, you can download my python scripts, put it in some folder like ~/led/ and paste ```@reboot python /home/YOURUSERNAME/led/start.py``` into crontab by using ```sudo crontab -e```. Done!

Note: Don't forget to edit the GPIO pins according to how you soldered your LEDs!

## Performance

**Network speed**

I tested the RouteryPi under the following conditions:

![normal results](https://phoenix1747.github.io/host/normal_result.png)

One thing to take into consideration is that I (unfairly) tested my 5GHz WiFi which the Raspberry Pi Zero W cannot provide. I have to admit the RouteryPi's results are not that great, especially compared to my normal connection. But if you don't have a fast connection in the first place, this will be sufficent. Although the results seem pretty poor, I tested if you could watch Full HD (1080p) Youtube videos and play a little game like Minecraft on a server and it worked just fine!

![routery results](https://phoenix1747.github.io/host/routery_result.png)

**WiFi Range**

The WiFi range is pretty good for it's small size. Without any external antenna, i.e. only using the tiny onboard antenna, I achieved only slightly less (~2-3m) range than with my ISP's router. The overall range depends heavily on walls and is in my case round about 6m (through 3 walls!)

**Power consumption**

I will also provide some info about the power consumption. Stay tuned!

## Optional

* You could add an automatic speedtest with [speedtest-cli-extras](https://github.com/HenrikBengtsson/speedtest-cli-extras) by utilizing crontab and outputting the results in a file. You'll have more convincing arguments when contacting your ISP in case something's not working again ;)

* You could remove some unused software from your pi to decrease the disk size even more - although this will only clean up some 10s of MBytes. Stuff you could remove would be e.g. vim-common, triggerhappy, bluez and so on. You can get a list of all installed packages by typing ```apt list --installed```. Don't forget to do ```sudo apt autoremove``` afterwards!

* You could also solder an external antenna onto the Pi if you aren't satisfied with it's range. The Pi Zero W has tiny solder pads for soldering a U.FL RF connector. Together with a small adapter cable you could use your standard WiFi antennas. You can read into this with a nice tutorial like this one: http://www.briandorey.com/post/Raspberry-Pi-Zero-W-external-antenna-mod

* Security related: Raspbian Stretch is **no longer vulnerable to the WPA2 Krack attack**. Since the system got patched you are totally safe with using any Raspberry Pi as AP or client**as long as all your other devices are secure**. So please always update your system! 

## Images

![image1](https://phoenix1747.github.io/host/image1.png)
![image2](https://phoenix1747.github.io/host/image2.png)
![image3](https://phoenix1747.github.io/host/image3.png)
![image4](https://phoenix1747.github.io/host/image4.png)
![image5](https://phoenix1747.github.io/host/image5.png)
![image6](https://phoenix1747.github.io/host/image6.png)
![image7](https://phoenix1747.github.io/host/image7.png)
![image8](https://phoenix1747.github.io/host/image8.png)


Note: I'm still waiting for some parts to arrive, so the hardware-side of my build isn't completely finished yet. I'm going to update these photos when I'm done.

---

Everyone who dislikes calling 'WLAN' 'WiFi' which I did because of simplicity: I'm sincerely sorry.

© 2017 RouteryPi, Phoenix1747.
