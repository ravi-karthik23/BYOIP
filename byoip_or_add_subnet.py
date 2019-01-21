#! /usr/local/bin/python3

import getopt
import ipaddress
import sys
from pymongo import MongoClient


def id_extractor(region,collection):
    region_cursor=collection.find({region:{'$exists':1}})
    id_dict=region_cursor.next()
    return id_dict['_id']

def update_one_record(obj_id,region_dict,region,collection):
    new_kv = {k: v for k, v in region_dict.items() if k == region}
    new_data = {"$set": new_kv}
    collection.update_one({'_id': obj_id}, new_data)


def populate_region_dict(db):
    region_dict=dict()
    cursor = db.MyRegionIP4Coll
    for document in cursor.find():
        region_dict.update({k: v for k, v in document.items() if k != '_id'})
    return region_dict


def byiop(region_dict,region,collection):
    try:
        ip=region_dict[region][::-1].pop()
        region_dict[region]=region_dict[region][1:]
    except IndexError:
        print('\nOut of hosts. Use the current script, but with the -a option, to add a new subnet to an existing or a new region')
        sys.exit(2)
    else:
        obj_id=id_extractor(region,collection)
        update_one_record(obj_id,region_dict,region,collection)

        print('BYO-IP allocated:{0}'.format(ip))
        cloud=input('Enter the cloud type. For ex: AWS,Azure,GCP, etc\n')
        account_id=input('Enter the account_id for the customer:\n')
        cluster_id=input('Enter the cluster_id for the account:\n')
        table_name=input("Enter the table's name where you want to add these above entries into:\n")
        print('\nBelow is the generated SQL query:\n')
        print('INSERT INTO {0} (ip,cloud,location,acct_id,IP_type,cluster_id) VALUES ({1},{2},{3},{4},{5},{6})\n'.format(table_name,ip,cloud,region,account_id,'BYOIP',cluster_id))
        sys.exit()


def add_subnet_to_region(subnet,region_dict,collection):

    try:
        new_subnet=ipaddress.ip_network(subnet)
    except ValueError:
        print('Incorrect Subnet {0} added. Please try again'.format(subnet))
        sys.exit(2)
    else:
        new_subnet_host_list=[str(host) for host in new_subnet.hosts()]
        region=input('\nEnter the region where this subnet has to be added to. For example: us_east_1:\n')
        if region not in region_dict.keys():
            # create a new region and append it to the region_list
            print('{0} not present in the list. Adding {1} as the new region within the region list'.format(region,region))
            region_dict[region]=new_subnet_host_list
            data_new_subnet = {k: v for k, v in region_dict.items() if k == region}
            collection.insert_one(data_new_subnet)

        else:
            obj_id=id_extractor(region,collection)
            region_dict[region] += new_subnet_host_list

            update_one_record(obj_id,region_dict,region,collection)

            print('hosts under {0} have now been added to the {1} region'.format(subnet,region))
            sys.exit()



def main(argv):
    region=''
    add_subnet=''

    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.MyRegionIP4
    collection = db['MyRegionIP4Coll']
    cursor = db.MyRegionIP4Coll

    region_dict= populate_region_dict(db)

    try:
        opts, args = getopt.getopt(argv, "hb:a:", ["byiop-region=", "add-subnet="])
    except getopt.GetoptError:
        print('byoip.py -b <region> -a <subnet>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('byoip.py -b <region> -a <subnet>')
            sys.exit()
        elif opt in ("-b","--byiop-region"):
            region=arg
        elif opt in ("-a", "--add-subnet"):
            add_subnet=arg

    if region:
        if region not in region_dict.keys():
            print('\n{0} not in list of regions:{1}'.format(region,[keys for keys in region_dict.keys()]))
            print('\nThis is a new region or there could be a typo. If this is a new region, run the program with the -a option first'
                ' to add a subnet to this new region\n')
            sys.exit(2)
        else:
            byiop(region_dict,region,collection)
            sys.exit()

    elif add_subnet:
        add_subnet_to_region(add_subnet,region_dict,collection)

    else:
        print('byoip.py -b <region> -a <subnet>')
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])



