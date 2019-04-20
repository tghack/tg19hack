from scapy.all import *
import binascii

pkts = rdpcap("superb-owlput.pcap")

out=""

for p in pkts:
    if p.dport==53:
        if "dw" in p[DNSQR].qname.decode("utf-8"):
            x = p[DNSQR].qname.decode("utf-8").split(".")[0]
            out+=x

with open("outfile","wb") as f:
    f.write(binascii.unhexlify(out))
