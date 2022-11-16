from IP import IP
from MAC import MAC
from RouterTableInfo import RouterTableInfo
import Rede

class Router: 
    
    rede = Rede.redeGlobal

    def __init__(self, name: str, numberOfPorts: int):
        self.name = name
        self.numberOfPorts = numberOfPorts
        self.portsInUse = 0
        self.ports = {}
        self.routerTableInfos = []

    def protocoloDeRede(self, protocol):
        return

    def addNewIPAndMac(self, ip: IP, mac: MAC):
        if self.portsInUse < self.numberOfPorts:
            self.ports[ip.ipStr] = mac
            self.portsInUse += 1
            
        else:
            print("MAIS PORTAS EM USO DO QUE PERMITIDO NO ROUTER: "+ self.name + ", metodo: addNewIPAndMac ")

    def updateNewRouterTable(self, rT: RouterTableInfo):
        self.routerTableInfos.append(rT)
