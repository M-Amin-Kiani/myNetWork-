
# 192.168.1.106

from scapy.all import *
from scapy.layers.inet import IP, ICMPerror
import logging

# log config file
log_file = "app.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# each line is a new packet
def read_file(file_path):

    with open(file_path, "r") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    return lines


def create_send_tunnel_packet(dest_ip, src_ip):
    lines = read_file("packet.txt")
    for payload in lines:   # proto 4 6 ==> 10 nadarim
        tunnel_packet = IP(src=dest_ip, dst=src_ip, proto=10) / payload   # inner tunnle from 102 to me(106)
        packet = IP(src=src_ip, dst=dest_ip) / tunnel_packet   # outter tunnle (my packet) from 106 to me(102)
        send(packet, verbose=False)  #verbos => log
        logging.info(f"send one packet to {dest_ip}")

# end packet to finish code
    tunnel_packet = IP(src=dest_ip, dst=src_ip, proto=10) / "EOF"
    packet = IP(src=src_ip, dst=dest_ip) / tunnel_packet
    send(packet, verbose=False)
    logging.info(f"send one packet to {dest_ip}")


def print_packet(packet): # oon be man
    if packet.haslayer(IP) and packet[IP].dst == '192.168.1.106' and packet[IP].src == '192.168.1.102'\
            and packet[IP].proto == 10:
        logging.info(f"receive one packet from {packet[IP].src}")
        chunk_of_file = packet[IP].payload
        try:
            printable_file_content = bytes(chunk_of_file).decode('utf-8')  # convert byte to string
            print(printable_file_content)

        except:
            print("I can't ")


def start_receiving():
    sniff(prn=print_packet, filter="ip", store=0)


create_send_tunnel_packet(dest_ip='192.168.1.102', src_ip='192.168.1.106')
#-------------------------------------
start_receiving()