#!/bin/sh

# Check for any errors, quit if any
function check_errors {
  if ! [ $? = 0 ]
  then
    echo "An error occured! Aborting...."
    exit 1
  fi
}

echo "This will transform your Pi into a WiFi Access Point."
read -p "To begin with the installation type in 'yes': " out

if ! [ "$out" = "yes" ]
then
  echo "You did not type in 'yes'. Exiting..."
  exit 1
fi

echo "Updating package sources..."
sudo apt update>/dev/null 2>&1
check_errors

echo "Installing hostapd and bridge-utils..."
sudo apt install hostapd bridge-utils -y>/dev/null 2>&1
check_errors
echo "Successfully installed!"

read -p "Please specify your SSID: " ssid
read -p "Please specify a password: " pw
read -p "Please specify your country code, e.g. DE: " cc
if [ "$ssid" ] && [ "$pw" ] && [ "$cc" ]
then
  a="
  # Bridge mode
  bridge=br0

  # Networking interface
  interface=wlan0

  # WiFi configuration
  ssid=$ssid
  channel=1
  hw_mode=g
  country_code=$cc
  ieee80211n=1
  ieee80211d=1
  wmm_enabled=1

  # WiFi security
  auth_algs=1
  wpa=2
  wpa_key_mgmt=WPA-PSK
  rsn_pairwise=CCMP
  wpa_passphrase=$pw
  "
else
  echo "Empty SSID, password or country code! Exiting..."
  exit 1
fi

echo "Writing hostapd.conf..."
sudo sh -c "echo $a>/etc/hostapd/hostapd.conf"
check_errors
echo "Successfully wrote hostapd.conf!"

read -p "Please specify your wireless interface name: " wi
read -p "Please specify your ethernet interface name: " ei
if [ "$wi" ] && [ "$ei" ]
then
  a="
  auto lo
  iface lo inet loopback

  # Ethernet
  auto $ei
  allow-hotplug $ei
  iface $ei inet manual

  # WiFi
  auto $wi
  allow-hotplug $wi
  iface $wi inet manual
  wireless-power off

  # Bridge
  auto br0
  iface br0 inet dhcp
  bridge_ports $ei $wi
  bridge_fd 0
  bridge_stp off
  "
else
  echo "Empty wireless or ethernet interface name! Exiting..."
  exit 1
fi

echo "Writing /etc/network/interfaces..."
sudo sh -c "echo $a>/etc/network/interfaces"
check_errors
echo "Successfully wrote /etc/network/interfaces!"

echo "Writing to /etc/default/hostapd..."
a="
RUN_DAEMON=yes
DAEMON_CONF="/etc/hostapd/hostapd.conf"
"
sudo sh -c "echo $a>/etc/default/hostapd"
check_errors
echo "Successfully wrote /etc/default/hostapd!"

echo "Installation is complete. You will want to restart your Pi to make this work."
echo "No further action should be required. Closing..."
