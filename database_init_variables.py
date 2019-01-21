#! /usr/local/bin/python3

import ipaddress


region_dict = dict()

#Creating the Network class for the subnets
net_244=ipaddress.ip_network('10.10.244.0/30')
net_245=ipaddress.ip_network('10.10.245.0/30')

net_242=ipaddress.ip_network('10.10.242.0/30')
net_243=ipaddress.ip_network('10.10.243.0/30')

net_240=ipaddress.ip_network('10.10.240.0/30')
net_241=ipaddress.ip_network('10.10.241.0/30')
net_246=ipaddress.ip_network('10.10.246.0/30')


#Getting the list of hosts in the network class
host_244_list=[str(host) for host in net_244.hosts()]
host_245_list=[str(host) for host in net_245.hosts()]

host_242_list=[str(host) for host in net_242.hosts()]
host_243_list=[str(host) for host in net_243.hosts()]

host_240_list=[str(host) for host in net_240.hosts()]
host_241_list=[str(host) for host in net_241.hosts()]
host_246_list=[str(host) for host in net_246.hosts()]



# Creating a flat list of all the hosts and assigning them as key,value pairs to the respective regions
region_dict['us_west_2']=host_244_list + host_245_list
region_dict['us_east_1']=host_242_list + host_243_list
region_dict['us_east_2']=host_240_list + host_241_list+host_246_list






