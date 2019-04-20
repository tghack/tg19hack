from scapy.all import *
import binascii
import random
import numpy
import base64
import string


SRVIP="172.19.0.3"
CLIENTIP="172.19.1.50"

CLIENTMAC="6f:5e:4d:3c:2b:1a" 
SRVMAC="1a:2b:3c:4d:5e:6f"

salt=""

usedports=[]
usedids=[]

with open("salt.jpg", "rb") as f:
    salt=f.read()
    salt=str(binascii.hexlify(salt))
    salt=salt[2:-1]


#function to generate DNS A request and response
#returns array with request and response pair
def gendns(clientmac,srvmac,clientip,srvip,dnsq,dnsr,dtype):
    packets=[]

    while True:
        rsport=random.randint(40000,65535)
        if rsport not in usedports:
            usedports.append(rsport)
            break

    while True:
        tid=random.randint(0,65535)
        if tid not in usedids:
            usedids.append(tid)
            break

    request = Ether(src=clientmac,dst=srvmac)\
            /IP(src=clientip,dst=srvip)\
            /UDP(sport=rsport,dport=53)\
            /DNS(id=tid,rd=1,qd=DNSQR(qname=dnsq,qtype=dtype))

    response = Ether(src=srvmac,dst=clientmac)\
            /IP(src=srvip,dst=clientip)\
            /UDP(sport=53,dport=rsport)/\
            DNS(id=tid,rd=1,qr=1,qdcount=1,
                    ancount=1,
                    qd=request.qd,
                    rcode=0,
                    an=DNSRR(rrname=dnsq + '.',
                        type=dtype,rclass="IN",ttl=3600,rdata=dnsr))

    packets.append(request)
    packets.append(response)
    return packets

if __name__ == '__main__':


    flagpackets=[]
    noisepackets=[]
    
    
    salt = [salt[i:i+62] for i in range(0, len(salt), 62)]
    for x in salt:
        flagpackets+=gendns(CLIENTMAC,SRVMAC,CLIENTIP,SRVIP, x + ".dw.tghekk.local","0.0.0.0","A")
    
    for x in (numpy.random.randint(200, size=30)):
        noisepackets+= gendns(CLIENTMAC,SRVMAC,CLIENTIP,SRVIP, "win" + str(x) + ".tghekk.local","172.19.20." + str(random.randint(1,254)),"A")
    
    wrpcap('dns.pcap',flagpackets)
    wrpcap('dnsnoise.pcap',noisepackets)
