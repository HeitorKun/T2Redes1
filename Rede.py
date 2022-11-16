from ARP import ARPReply
from ARP import ARPRequest
from ICMP import ICMPEchoRequest
from ICMP import ICMPEchoReply
import Nodo
import Router
from IP import IP
from MAC import MAC

class Rede:
    dicionarioDeRedes = {}
    def __init__(self):
        pass
    
    def adicionaNodo(self, nodo: Nodo.Nodo):
        if nodo.ip.redeIPInBinaryStr in Rede.dicionarioDeRedes:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr].append(nodo)
        else:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr] = [nodo]

    def adicionaRouter(self, router: Router.Router):
        routerAllPorts = router.ports.keys()
        for ports in routerAllPorts:
            
            splitPointIPStr = ports.split(".")
        
            routerIPInBinaryStr = ""
            for ip in splitPointIPStr:
                routerIPInBinaryStr += bin(int(ip)).replace("0b", "").zfill(8)
            routerIPInBinaryStr = routerIPInBinaryStr[:router.mask]

            if routerIPInBinaryStr in Rede.dicionarioDeRedes:
                Rede.dicionarioDeRedes[routerIPInBinaryStr].append(router)
            else:
                Rede.dicionarioDeRedes[routerIPInBinaryStr] = [router]

    def enviaNaRede(self, protocol):
        if isinstance(protocol, ARPReply):
            for host in Rede[protocol.tell.redeIPInBinaryStr]:
                host.protocoloDeRede(protocol)
        elif isinstance(protocol, ARPRequest):
            for host in Rede[protocol.tell.redeIPInBinaryStr]:
                host.protocoloDeRede(protocol)
    def ICMPEchoRequestReceive(self, icmpEchoRequest: ICMPEchoRequest) -> int:
        if icmpEchoRequest.ttl - 1 == 0:
            return 99
        else:
            nodes = Rede.dicionarioDeRedes[icmpEchoRequest.nextNode.redeIPInBinaryStr]
            for node in nodes:
                if isinstance(node, Nodo.Nodo):
                    ip = node.ip.ipStr
                    if icmpEchoRequest.nextNode.ipStr == ip and icmpEchoRequest.dst.ipStr == ip:
                        return 0
                    if icmpEchoRequest.nextNode.ipStr == ip:
                        
                        return 1
                elif isinstance(node, Router.Router):
                    # print(node.ports, arpReply.who.ipStr)
                    if arpReply.who.ipStr in node.ports:
                        node.arpTable[arpReply.tell.ipStr] = arpReply.tellersMac
        
    def ICMPEchoReplyReceive(self, icmpEchoReply: ICMPEchoReply) -> int:
        print()

    def ARPReplyReceive(self, arpReply: ARPReply):
        broadcastNodes = Rede.dicionarioDeRedes[arpReply.tell.redeIPInBinaryStr]
        ip = "" 
        
        # Tell tem que ser tipo NODO para poder printar nomde do nodo.
        print(f"{arpReply.who.ipStr} --> {arpReply.tell.ipStr} : ARP Reply<br/>{arpReply.tell.ipStr} is at {arpReply.tellersMac}")
        for node in broadcastNodes:
            if isinstance(node, Nodo.Nodo):
                ip = node.ip.ipStr
                if arpReply.who.ipStr == ip:
                    #no reply, tellersMac eh string, nao tipo MAC.
                    node.arpTable[arpReply.tell.ipStr] = arpReply.tellersMac
            elif isinstance(node, Router.Router):
                # print(node.ports, arpReply.who.ipStr)
                if arpReply.who.ipStr in node.ports:
                    node.arpTable[arpReply.tell.ipStr] = arpReply.tellersMac
        

    def ARPRequestReceive(self, arpRequest: ARPRequest): #esse nodo RECEBEU DA REDE um ARPRequest
        #Check se who e tell estao na mesma rede
        #Se estao na rede diferente, mudo o who para roteador.
        # if arpRequest.who.redeIPInBinaryStr != arpRequest.tell.redeIPInBinaryStr:
        #     newWho = arpRequest.tell.ipStr[:-1] + "1"
        #     arpRequest.who = IP(newWho, arpRequest.tell.maskStr)

        # Tell tem que ser tipo NODO para poder printar nomde do nodo.
        print(f"Note over {arpRequest.tell.ipStr} : ARP Request<br/>Who has {arpRequest.who.ipStr}? Tell {arpRequest.tell.ipStr}")

        broadcastNodes = Rede.dicionarioDeRedes[arpRequest.tell.redeIPInBinaryStr]
        ip = "" 
        for node in broadcastNodes:
            if isinstance(node, Nodo.Nodo):
                ip = node.ip.ipStr
                if arpRequest.who.ipStr == ip:
                    node.arpTable[arpRequest.tell.ipStr] = arpRequest.tellersMac.macStr
                    tellersMac = node.mac.macStr
                    arpReply = ARPReply(arpRequest.tell, arpRequest.who, tellersMac)
                    self.ARPReplyReceive(arpReply)
            elif isinstance(node, Router.Router):
                # print(node.ports, arpRequest.who.ipStr)
                if arpRequest.who.ipStr in node.ports:
                    node.arpTable[arpRequest.tell.ipStr] = arpRequest.tellersMac
                    tellersMac = node.ports[arpRequest.who.ipStr]
                    arpReply = ARPReply(arpRequest.tell, arpRequest.who, tellersMac)
                    self.ARPReplyReceive(arpReply)

        # if arpRequest.who.ipStr == self.ip: # if its me then send arp reply
        #     # save his mac on arpTable
        #     self.arpTable[arpRequest.tell] = arpRequest.tellersMac
        #     # send reply
        #     arpReply = ARPReply(arpRequest.who, arpRequest.tell, self.mac)
        #     Nodo.rede.enviaNaRede(arpReply)

redeGlobal = Rede()