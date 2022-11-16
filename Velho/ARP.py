from IP import IP
from MAC import MAC

class ARPRequest:
    def __init__(self, who: IP, tell: IP, tellersMac: MAC):  
        self.who: IP = who
        self.tell: IP = tell
        self.tellersMac: MAC = tellersMac
        

class ARPReply:
        def __init__(self, who: IP, tell: IP, tellersMac: MAC):  
            self.who: IP = who
            self.tell: IP = tell
            self.tellersMac: MAC = tellersMac