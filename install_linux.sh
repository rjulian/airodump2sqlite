#!/bin/bash

if [ -z "$1" ]
then
    echo "Please provide network interface name as argument."
fi

echo "Checking if airodump binary is installed."
echo "========================================="
if [[ -x "/usr/sbin/airodump-ng" ]]
then
    echo "Airodump-ng has been found."
else
    sudo apt-get update && sudo apt-get -y install aircrack-ng
fi

echo "========================================="
echo "Starting interface $1 in monitor mode."
echo "========================================="
sudo airmon-ng $1

echo "========================================="
echo "Starting airodump on $1mon."
echo "========================================="
sudo airodump-ng --beacons -o csv -w whoiswalkingby $1mon
