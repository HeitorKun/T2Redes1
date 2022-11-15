from IP import IP
from MAC import MAC

class Router: 
    def __init__(self, name: str, numberOfPorts: int):
        self.name = name
        self.numberOfPorts = numberOfPorts
        self.portsInUse = 0

    def addNewIPAndMac(self, ip: IP, mac: MAC):
        if self.portsInUse < self.numberOfPorts:
            self.ip: IP = ip
            self.mac: MAC = mac
        else:
            print("MAIS PORTAS EM USO DO QUE PERMITIDO NO ROUTER: "+ self.name + ", metodo: addNewIPAndMac ")
