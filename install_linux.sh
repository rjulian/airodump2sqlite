sudo apt-get update && sudo apt-get -y install aircrack-ng
sudo airmon-ng $1
sudo airodump-ng --beacons -o csv -w whoiswalkingby $1mon
