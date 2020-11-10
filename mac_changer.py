#!/usr/bin/env python

import subprocess
import re
import optparse

def get_arguments():
    parser=optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface",help="Interface to change")
    parser.add_option("-m", "--mac", dest="new_mac",help="New MAC Address")

    (options,arguments)=parser.parse_args()

    if not options.interface:
        parser.error("[-]Please specify Interface or use --help for more info")
    elif not options.new_mac:
        parser.error("[-]Please specify New MAC Address or use --help for more info")
    else:
        return options

def change_mac(i,m):
    print("[+]Changing MAC Address of "+ i +" to "+m)

    subprocess.call(["ifconfig", i, "down"])
    subprocess.call(["ifconfig", i, "hw", "ether", m])
    subprocess.call(["ifconfig", i, "up"])

def get_current_mac(i):
    ifconfig_result = subprocess.check_output(["ifconfig", i])

    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if current_mac:
        return current_mac.group(0)
    else:
        print("[-]Coudn't find MAC Address")


options=get_arguments()
current_mac=get_current_mac(options.interface)
print("Current MAC > "+str(current_mac))

change_mac(options.interface,options.new_mac)

current_mac=get_current_mac(options.interface)


if current_mac==options.new_mac:
    print("[+]Mac Address successsfully change to "+current_mac)
else:
    print("[-]Mac Address didn't get change")










