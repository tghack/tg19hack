#!/usr/bin/python3

from scapy.all import *
import hashlib
import random
from random import uniform

#globs
pkttime=1500000000

def xor_str(a,b):
    xored = []
    for i in range(max(len(a), len(b))):
        xored_value = ord(a[i%len(a)]) ^ ord(b[i%len(b)])
        xored.append(hex(xored_value)[2:])
    return ''.join(xored)

def get_sympackets(dictstream,pkts):
    for pkt in pkts:
        print("pkt: " + pkt.summary())
        
        try:
            src = (str(pkt.src) + ":" + str(pkt.sport))
            dst = (str(pkt.dst) + ":" + str(pkt.dport))
        except:
            continue

        shash = hashlib.sha256(src.encode('utf-8')).hexdigest()
        dhash = hashlib.sha256(dst.encode('utf-8')).hexdigest()

        unique=xor_str(shash,dhash)

        if not unique in dictstream:
            dictstream[unique]=[]

        dictstream[unique].append(pkt)


def packet_time(pkt):
    global pkttime
    pkt.time=pkttime + uniform(0.001, 0.5)
    pkttime=pkt.time
    return

if __name__ == "__main__": 
    pkts_flag = rdpcap('dns.pcap')
    pkts_dnoise = rdpcap('dnsnoise.pcap')
    pkts_noise = rdpcap('noise.pcap')

    new_flag=[]
    new_dnoise=[]
    new_noise=[]

    for pkt in pkts_flag:
        del pkt[IP].chksum
        del pkt[UDP].chksum
        pkt[Ether].src="00:00:00:00:00:00"
        pkt[Ether].dst="00:00:00:00:00:00"
        new_flag.append(pkt)

    for pkt in pkts_dnoise:
        del pkt[IP].chksum
        del pkt[UDP].chksum
        pkt[Ether].src="00:00:00:00:00:00"
        pkt[Ether].dst="00:00:00:00:00:00"
        new_flag.append(pkt)

    for pkt in pkts_noise:
        if ("TCP" in pkt) or ("UDP" in pkt):
            if pkt.sport > pkt.dport:
                pkt[IP].src = "172.19.1.50"
            else:
                pkt[IP].dst = "172.19.1.50"

            if "TCP" in pkt: del pkt[TCP].chksum
            if "UDP" in pkt: del pkt[UDP].chksum
            del pkt[IP].chksum


        pkt[Ether].src="00:00:00:00:00:00"
        pkt[Ether].dst="00:00:00:00:00:00"
        new_noise.append(pkt)

    wrpcap('a.pcap',new_flag)
    wrpcap('b.pcap',new_noise)
    wrpcap('c.pcap',new_dnoise)
    new_flag=rdpcap('a.pcap')
    new_noise=rdpcap('b.pcap')
    new_dnoise=rdpcap('c.pcap')

    flag={}
    noise={}
    dnoise={}
    get_sympackets(flag,new_flag)
    get_sympackets(noise,new_noise)
    get_sympackets(dnoise,new_dnoise)


    out=[]

    lol0=0
    lol1=0
    lol2=0

    __import__("IPython").embed()

    for streams in range(len(list(flag.keys()))):

        if random.randint(0,100) > 90:
            try:
                noisear = list(noise.keys())[lol0]
                for pkt in noise[noisear]:
                    packet_time(pkt)
                    out.append(pkt)
                lol0=lol0+1
            except IndexError:
                continue
        
        if random.randint(0,100) < 10:
            
            try:
                dnoisear = list(dnoise.keys())[lol1]
                for pkt in dnoise[dnoisear]:
                    packet_time(pkt)
                    out.append(pkt)
                lol1=lol1+1
            except IndexError:
                continue

        try: 
            flagar = list(flag.keys())[lol2]
            for pkt in flag[flagar]:
                packet_time(pkt)
                out.append(pkt)
            lol2=lol2+1
        except IndexError:
            continue


    wrpcap('superb-owlput.pcap',out)
