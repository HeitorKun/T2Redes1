from IP import IP
from MAC import MAC

class ARPRequest:
    def __init__(self, who: IP, tell: IP):  
        self.who: IP = who
        self.tell: IP = tell
        

class ARPReply:
        def __init__(self, who: IP, tell: IP, mac: MAC):  
            self.who: IP = who
            self.tell: IP = tell
            self.mac: MAC = mac