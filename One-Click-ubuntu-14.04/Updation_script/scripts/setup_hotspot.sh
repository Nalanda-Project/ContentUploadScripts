#!/bin/bash
echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
notify-send "Setting up hotspot on system"
(echo 's'| sudo -S sudo apt-get update;
echo 'y'| sudo -S apt-get install dpkg-dev cdbs debhelper dh-autoreconf libev-dev libpcre3-dev pkg-config;
echo 'y'| sudo -S apt-get -y purge dnsmasq hostapd kolibri-hotspot;
echo 'y'| sudo -S apt-get install -y dnsmasq git;
echo 'y'| sudo -S dpkg -i /home/kolibri/Desktop/Updation_script/kolibri-hotspot/hostapd/hostapd*.deb;
echo 'y'| sudo -S dpkg -i /home/kolibri/Desktop/Updation_script/kolibri-hotspot/kolibri-hotspot*.deb ) 2>> /home/kolibri/Desktop/Updation_script/updation.log
echo "Hotspot setup done " >> /home/kolibri/Desktop/Updation_script/updation.log
zenity --info --text="Hotspot setup Done."
fi
