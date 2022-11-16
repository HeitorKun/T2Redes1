from ICMP import ICMPEchoRequest
from IP import IP
from MAC import MAC
from ARP import ARPReply
from ARP import ARPRequest
import Rede

class Nodo:

    rede = Rede.redeGlobal

    def __init__(self, name: str, ip: IP, mac: MAC, gateway: IP):
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
            Nodo.rede.enviaNaRede(arpReply)

