# RouteryPi

## Summary

**Hey there! I'm working on this. I'll add some images in the next couple of days and update some missing text. Thanks for your patience! :D**

The RouteryPi is a WiFi access point based on a Raspberry Pi Zero W. Together with a pretty case and some status LEDs it makes a really nice alternative AP that can easily be programmed and customized. The only downside of using a Raspberry Pi is it's relative slow networking speed compared to high quality(!) retail APs - nevertheless it has great potential and makes an even better addition if you want to upgrade some random old AP that you found in your basement!

## Hardware

You will need the following parts for this project:
- A neat looking case maybe with holes for status lights. Reusing an old router case would be ideal here (yay, upcycling!).
- A Raspberry Pi Zero W - the mainboard.
- An OTG Ethernet Adapter (USB 2.0).
- A MicroSD card (anything class 6 and higher will do really).
- A good power supply and connector (1A is plenty of power).
- Some wire to connect everything.

Optional:
- Some LEDs and resistors if you want status LEDs.
- A push button to reset the Pi.
- On/Off switch (to kill the power obviously).
- A heatsink - you don't need it but your Pi will thank you.

## Specs

**Raspberry Pi Zero W:**
- 1GHz, single-core CPU
- 512MB RAM
- USB OTG port
- 802.11 b/g/n wireless LAN
- 40 GPIO pins
- Some other stuff, that isn't relevant to this project. For full specs visit https://www.raspberrypi.org/products/raspberry-pi-zero-w/

**OTG Ethernet:**
- USB 2.0 OTG to 10/100 Fast Ethernet
- Standard RJ45 Ethernet port
- No external power required
- Link and Activity LEDs
- More info about the one I bought, at https://plugable.com/products/usb2-otge100/

## Software

This build uses the latest version of Raspbian which is Raspbian Stretch. You can download it on the official RaspberryPi website, at https://www.raspberrypi.org/downloads/raspbian/. I guess you already know how to flash the image onto the SD Card - however, if you don't have a look at this tutorial: https://www.raspberrypi.org/documentation/installation/installing-images/

You will also need Python (my scripts use 2.7) if you have some LEDs and want to easily program them as status LEDs.
If you aim to do something like that be ready to also install python-pip and some packages like psutil.

The heart of this whole installation will be 'hostapd' and 'bridge-utils' because we will be using the Pi as a network bridge between the LAN and WiFi. This means that **you will need an additonal DHCP and DNS server**. Nevertheless, this simplifies the whole installation a lot and makes it less error-prone. If you already have a router (which I assume you do) you can plug in your RouteryPi via LAN and everything will work out of the box.

Note: You will need **no additional drivers** for anything!

## Installation

**Preparation**

The first step is, obviously, to install the image onto the SD Card and booting it up. The first boot usually takes longer than a normal startup because the Pi has to do stuff like generating new SSH keys and so on.

Then use ```sudo raspi-config``` to configure the Pi to your linkings.

Now update it using ```sudo apt update && sudo apt full-upgrade``` - once it's done updating reboot it and we'll start with the actual AP installation.

**AP setup**

Firstly, install hostapd and bridge-utils with the following command.
```
sudo apt-get install hostapd bridge-utils
```

Now comes the important part. After the installation go on and edit the hostapd.conf.
```
sudo nano /etc/hostapd/hostapd.conf
```

If the file is not empty, just delete it's content. We will be using a custom config anyways. The minimal config that you should use too looks like that:
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
wpa_passphrase=YourCustomPasswordWhichShouldBePrettyStrong123$%
```
Just paste the text into the hostapd config file, save it and you're good to go.

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
This will result in the Pi using DHCP which means it can be used in **any** network. The downside of this is that you have to find out the IP address if you want to, let's say, use SSH. You could use a static IP address by changing the br0 interface config a little bit - just google 'static ip raspberry pi'. (For the lazy: https://duckduckgo.com/?q=static+ip+raspberry+pi)

**Final steps**

After you did a quick reboot using ```sudo reboot```, you can start testing the whole thing. To test the hostapd config use this command: ```sudo hostapd /etc/hostapd/hostapd.conf```. Note: If it does exit without you doing something, then there is something wrong with it. To go into debug mode use ```sudo hostapd -dd /etc/hostapd/hostapd.conf```.

While testing the hostapd config you can also try connecting as a client. If you've done everything correctly you should be able to do so without any problems.

To enable hostapd to run upon boot you have to edit one more file.
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

Detailed speedtest results will come soon! 

So far the WiFi range seems to be quite good, I'll test it once more and put some more detail here!

I will also provide some info about the power consumption. Stay tuned!

## Optional

* You could add an automatic speedtest with [speedtest-cli-extras](https://github.com/HenrikBengtsson/speedtest-cli-extras) by utilizing crontab and outputting the results in a file. You'll have more convincing arguments when contacting your ISP because your connection is not what you paid for ;)

* You could remove some unused software from your pi to decrease the disk size even more - although this will only clean up some 10s of MBytes. Stuff you could remove would be e.g. vim-common, triggerhappy, bluez and so on. You can get a list of all installed packages by typing ```apt list --installed```. Don't forget to do ```sudo apt autoremove``` afterwards!

* You could also solder an external antenna onto the Pi if you aren't satisfied with it's range. The Pi Zero W has tiny solder pads for soldering a U.FL RF connector. Together with a small adapter cable you could use your standard WiFi antennas. You can read into this with a nice tutorial like this one: http://www.briandorey.com/post/Raspberry-Pi-Zero-W-external-antenna-mod

* Security Related: Raspbian Stretch is **no longer vulnerable to the WPA2 Krack attack**. Since the system got patched you are totally safe with using the RouteryPi as AP **as long as all your clients are secure**. So please immediately update your system! 

## Images

![image1](https://phoenix1747.github.io/host/image1.png)
![image2](https://phoenix1747.github.io/host/image2.png)
![image3](https://phoenix1747.github.io/host/image3.png)
![image4](https://phoenix1747.github.io/host/image4.png)
![image5](https://phoenix1747.github.io/host/image5.png)
![image6](https://phoenix1747.github.io/host/image6.png)


Note: I'm still waiting for some parts to arrive, so the hardware-side of my build isn't completely finished yet. I'm going to update these photos as soon as I'm finished!

---

Everyone who dislikes calling 'WLAN' 'WiFi' which I did because of simplicity: SORRY.

© 2017 RouteryPi, Phoenix1747.
