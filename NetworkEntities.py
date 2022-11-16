from ICMP import ICMPEchoRequest
import IP
import MAC
from ARP import *
from ARP import *

class NetworkEntity:
    def __init__(self, ip: IP):
        self.ip = ip

    def protocoloDeRede(self, protocol):
        return

    def isMyIP(self, ip:IP) -> bool:
        return False

    def isMyMAC(self, mac:MAC) -> bool:
        return False



class Rede:
    dicionarioDeRedes = {}
    def __init__(self):
        pass
    
    def adicionaNodo(self, nodo: NetworkEntity):
        if nodo.ip.redeIPInBinaryStr in Rede.dicionarioDeRedes:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr].append(nodo)
        else:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr] = [nodo]

    def adicionaRouter(self, router: NetworkEntity):
        if router.ip.redeIPInBinaryStr in Rede.dicionarioDeRedes:
            Rede.dicionarioDeRedes[router.ip.redeIPInBinaryStr].append(router)
        else:
            Rede.dicionarioDeRedes[router.ip.redeIPInBinaryStr] = [router]

    def enviaNaRede(self, protocol):
        if isinstance(protocol, ARPReply):
            for host in Rede[protocol.tell.redeIPInBinaryStr]:
                host.protocoloDeRede(protocol)
        elif isinstance(protocol, ARPRequest):
            for host in Rede[protocol.tell.redeIPInBinaryStr]:
                host.protocoloDeRede(protocol)



class Nodo(NetworkEntity):

    def __init__(self, name: str, ip: IP.IP, mac: MAC.MAC, gateway: IP.IP):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.gateway = gateway
        self.arpTable = {}
        

    def protocoloDeRede(self, protocol): # recebendo da rede
        if isinstance(protocol, ARPReply): 
            self.ARPReplyReceive(protocol)
        elif isinstance(protocol, ARPRequest): 
            self.ARPRequestReceive(protocol)

    def ARPReplyReceive(self, arpReply: ARPReply):
        if arpReply.tell == self.ip:
            self.arpTable[arpReply.who] = arpReply.mac
        
    def ARPRequestReceive(self, arpRequest: ARPRequest): #esse nodo RECEBEU DA REDE um ARPRequest

        if arpRequest.who.ipStr == self.ip: # if its me then send arp reply
            # save his mac on arpTable
            self.arpTable[arpRequest.tell] = arpRequest.tellersMac
            # send reply
            arpReply = ARPReply(arpRequest.who, arpRequest.tell, self.mac)
            self.rede.enviaNaRede(arpReply)

    def isMyIP(self, ip:IP.IP) -> bool:
        return self.ip == ip

    def isMyMAC(self, mac:MAC.MAC) -> bool:
        return self.mac == mac

    



from RouterTableInfo import RouterTableInfo

class Router(NetworkEntity): 
    
    rede = Rede()

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
