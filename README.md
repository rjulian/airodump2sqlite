# WhoIsWalkingBy
A tool to collect 802.11 client data from airodump-ng into a sqlite database. A few additional metadata have been appended to the original data collected by airodump-ng, namely an "easy_name" field for referring to the individual MAC addresses and a "last ten visits" field.

## Requirements
WhoIsWalkingBy simply requires a running `airodump-ng` process outputting to a file in the CSV format. Check out `install_linux.sh` for more info. 

## Usage
Simply run the provided script `whoiswalkingby` pointing to the airodump output file and the database location you're looking for. Example: `whoiswalkingby --airodump-file ./output-01.csv --database-file ./whoiswalkingby.db`
