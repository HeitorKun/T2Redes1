from ICMP import ICMPEchoRequest
from IP import IP
from MAC import MAC
from ARP import ARPReply
from ARP import ARPRequest
from Rede import Rede

n2 = Node()
n1.executaProtocoloDeRede(ARPRequest( n2 ,n1.ip))

class Nodo:
    arpTable = {}
    rede = Rede()

    def __init__(self, name: str, ip: IP, mac: MAC, gateway: IP):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.gateway = gateway

    def protocoloDeRede(self, protocol):
        if isinstance(protocol, ARPReply): 
            ARPReply(protocol)
        elif isinstance(protocol, ARPRequest): 
            ARPRequest(protocol)

    def ARPReply(arpReply: ARPReply):
        return
    def ARPRequest(arpRequest: ARPRequest):
        return