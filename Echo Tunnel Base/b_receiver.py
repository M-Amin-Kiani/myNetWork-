
# 192.168.1.102

from scapy.all import *
from scapy.layers.inet import IP
import logging


# log config
packets = []
file_transmission_complete = False
log_file = "net.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def tunnel_packet(packet):  # male man
    if packet.haslayer(IP) and packet[IP].dst == '192.168.1.102':
        print("waiting...")
        inner_packet = packet[IP].payload
        #print(inner_packet.haslayer(IP))
        if inner_packet.haslayer(IP):
            print(inner_packet.show())
            logging.info(f"receive one packet from {packet[IP].src}")
            print(bytes(inner_packet.payload))
            packets.append(inner_packet)


# just give ip packet
def start_receiving():
    sniff(prn=tunnel_packet, filter="ip", store=0, stop_filter=stop_receiving)


def stop_receiving(packet):
    if packet.haslayer(IP) and packet[IP].dst == '192.168.1.102':
        inner_packet = packet[IP].payload
        if b'EOF' in bytes(inner_packet.payload):
            return True


# scapy sniffer
start_receiving()


# --------------------------------------------

for packet in packets:
    send(packet)
    logging.info(f"send one packet to {packet[IP].src}")
    print(packet)