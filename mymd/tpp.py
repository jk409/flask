import socket
#import sys
def run(ip, port):
    port = int(port)
    try:
        sc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sc.settimeout(2)
        sc.connect((ip, port))
        sc.close()
        return('%-18s %-6s Ok'%(ip, port))
    except socket.timeout:
        sc.close()
        return('%-18s %-6s Fail'%(ip, port))
    except:
        sc.close()
        return('%-18s %-6s Fail'%(ip, port))

if __name__ == "__main__":
    import sys
    ip=sys.argv[1]
    port=sys.argv[2]
    while 1:
        print(run(ip, port))
