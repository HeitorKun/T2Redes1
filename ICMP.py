# class ICMPEchoRequest:
#     def __init__(self):
#         pass

from IP import IP
from MAC import MAC

class ICMPEchoRequest:
    def __init__(self, currentNode: IP, nextNode: IP, tellersMac: MAC, src: IP, dst: IP, ttl: int):  
        self.currentNode: IP = currentNode 
        self.nextNode: IP = nextNode
        self.tellersMac: MAC = tellersMac
        self.src = src
        self.dst = dst
        self.ttl = ttl
        

class ICMPEchoReply:
        def __init__(self, currentNode: IP, nextNode: IP, tellersMac: MAC, src: IP, dst: IP, ttl: int):  
            self.currentNode: IP = currentNode
            self.nextNode: IP = nextNode
            self.tellersMac: MAC = tellersMac
            self.src = src
            self.dst = dst
            self.ttl = ttl