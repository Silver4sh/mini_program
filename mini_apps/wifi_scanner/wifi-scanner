##need Npcap

from scapy.all import *

import sys
import signal
import os
import ctypes

# Function to hendle when the user enter Ctrl+C
def signal_handler(signal, frame):
    print("\n==================")
    print("Execution aborted by User")
    print("====================")
    sys.exit(1)

# Function to remin the user of the basic syntax, if incorrect
def usage():
    if len(sys.argv) < 3:
        print("\n Usage:")
        print("\t wifi-scanner.py -i <interface>\n")
        sys.exit(1)

# Function to sniff the packets
def sniffpackets(packet):
    try:
        SRCMAC  = packet[0].addr2
        DSTMAC  = packet[0].addr1
        BSSID   = packet[0].addr3
    except:
        print("Cannot read MAC address")
        print(str(packet).encode("hex"))
        sys.exc_clear()

    try:
        SSIDSize    = packet[0][Dot11Elt].len
        SSID        = packet[0][Dot11Elt].info
    except:
        SSID        = ""
        SSIDSize    = 0

    # Function chech to see whether the packet type = 0 and subtype = 8 (Beacon Frames)
    if packet[0].type == 0:
        ST = packet[0][Dot11].subtype
        if str(ST) == "8" and SSID != "" and DSTMAC.lower() == "ff:ff:ff:ff:ff:ff":
            p = packet[Dor11Elt]
            cap = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                                 "{Dot11ProbeResp:%Dot11ProbeResp.cap%}".split("+"))
            channel = None
            crypto = set()

    # Function to track discovered SSID's so as not to list them each time they are discovered
    global ssid_list
    if SSID not in ssid_list:
        ssid_list.add(SSID)
        print("Found SSID : {0:30}  MAC : {1:17}  Channel : {2}".format(SSID, SRCMAC, channel))

# Function to set up wireless interface in monitor mode
def setup_monitor(iface):
    print("Setting up sniffing options ...")
    os.system("netsh interface set interface name=\"" + iface + "\" admin=disable")
    os.system("netsh interface set interface name=\"" + iface + "\" mode=monitor")
    os.system("netsh interface set interface name=\"" + iface + "\" admin=enable")
    return iface

# Function to chech whether the user has administrator privilages and if not to message them
def check_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print("You must runt this script with administrator privilages.")
        exit(1)

# Main Code Body
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    usage()
    check_admin()
    parameters = {sys.argv[1]:sys.argv[2]}
    if "mon" not in str(parameters["-i"]):
        newiface = setup_monitor(parameters["-i"])
    else:
        newiface = str(parameters["-i"])
    ssid_list = set()
    print("Starting Wi-Fi Sniffer")
    print("Sniff on interface " + str(newiface) + " ...\n")
    sniff(iface=newiface, prn=sniffpackets, store=0)
