import socket
import time

def ping(host, port, timeout = 2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        sock.close()
        return True

def timed_ping(host,port,timeout=2):
    t0 = time.time()
    if ping(host,port,timeout):
       return time.time()-t0