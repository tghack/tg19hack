import os
import sys
import tempfile
import subprocess
from binascii import hexlify
import signal
import zlib

qemu_pid = None

def sigterm_handler(signum, frame):
    try:
        if qemu_pid:
            os.kill(qemu_pid, signal.SIGKILL)
        os.unlink(loader_path)
        os.rmdir(tmp_dir)
    except:
        pass

    sys.exit()


signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGPIPE, sigterm_handler)
signal.signal(signal.SIGALRM, sigterm_handler)
signal.alarm(30)

sys.stdout.write("Give me data (pad to 1024 bytes): ")
sys.stdout.flush()
data = sys.stdin.read(1024)
data = zlib.decompress(data, 15 + 32)

tmp_dir = tempfile.mkdtemp(dir="/tmp")

loader_path = tmp_dir + "/loader.elf"
with open(loader_path, "wb+") as f:
    f.write(data)

cmd = ["/home/tghack/qemu-system-arm",
       "-M", "raspi2", "-serial", "stdio",
       "-kernel", loader_path]
sys.stdout.write("[+] running command: {}\n".format(str(cmd)))
sys.stdout.flush()
proc = subprocess.Popen(cmd)
qemu_pid = proc.pid

proc.wait()

try:
    os.unlink(loader_path)
    os.rmdir(tmp_dir)
except:
    pass
