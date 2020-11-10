#!/usr/lib/env python
import argparse
import scapy.all as scapy

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="Target ip address or the range")

    options=parser.parse_args()

    return options


def scan(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_reaquest_broadcast=broadcast/arp_request

    answer_list=scapy.srp(arp_reaquest_broadcast,timeout=1,verbose=False)[0]

    client_list=[]

    for element in answer_list:
        client_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dict)

    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n----------------------------------------")

    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])


options=get_args()
scan_list=scan(options.target)      ##EVERYONE MAKES MISTAKE AT THIS POINT SO PLEASE NOT IT
print_result(scan_list)        