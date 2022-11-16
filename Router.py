from IP import IP
from MAC import MAC
from NetworkEntityAbstraction import NetworkEntity
from RouterTableInfo import RouterTableInfo

class Router(NetworkEntity): 
    
    def __init__(self, name: str, numberOfPorts: int):
        self.name = name
        self.numberOfPorts = int(numberOfPorts)
        self.portsInUse = 0
        self.mask = 0
        self.ports = {}
        self.routerTableInfos = []

    def protocoloDeRede(self, protocol):
        return

    def addNewIPAndMac(self, ip: IP, mac: MAC):
        if self.portsInUse < self.numberOfPorts:
            self.mask = ip.maskInt
            self.ports[ip.ipStr] = mac.macStr
            self.portsInUse += 1

        else:
            print("MAIS PORTAS EM USO DO QUE PERMITIDO NO ROUTER: "+ self.name + ", metodo: addNewIPAndMac ")

    def updateNewRouterTable(self, rT: RouterTableInfo):
        self.routerTableInfos.append(rT)

    def isMyIP(self, ip:IP) -> bool:
        for thisIp in self.ports: 
            if thisIp == ip.ipStr:
                return True

        return False

    def isMyMAC(self, mac:MAC) -> bool:
        for thisMac in self.ports.values(): 
            if thisMac == mac.macStr:
                return True

        return False