from ICMP import ICMPEchoRequest
import IP
import MAC
from ARP import ARPReply
from ARP import ARPRequest
from NetworkEntityAbstraction import NetworkEntity

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
    def isMyIP(self, ip:IP.IP) -> bool:
        return self.ip == ip

    def isMyMAC(self, mac:MAC.MAC) -> bool:
        return self.mac == mac