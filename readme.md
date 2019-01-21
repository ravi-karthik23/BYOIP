## BYOIP 

This repository contains the python scripts that first initializes a Database within MongoDB with the regions and the list of addresses. The script, byoip_or_add_subnet.py, is used for BYOIP operations and adding subnets to the regions. 


Please run the python program: mongodb_init.py to first initialize the DB.
Once the Mongo DB has the information of the region and the list of IP addresses in them, use the byoip_or_add_subnet.py python script for BYOIP operations ( allocating an IP from the list of IPs that belong to a region) or adding extra IP addresses to a region.