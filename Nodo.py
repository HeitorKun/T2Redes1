from IP import IP
from MAC import MAC
from ARP import ARPReply
from ARP import ARPRequest

class Nodo:
    arpTable = {}

    def __init__(self, name: str, ip: IP, mac: MAC, gateway: IP):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.gateway = gateway

    def executaProtocoloDeRede(self, protocol):
        return

    def recebeProtocoloDeRede(self, protocol):
        if isinstance(protocol, ARPReply): 
            ARPReply(protocol)
        elif isinstance(protocol, ARPRequest): 
            ARPRequest(protocol)

    def ARPReply(arpReply: ARPReply):
        return
    def ARPRequest(arpRequest: ARPRequest):
        return