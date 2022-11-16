from ARP import ARPReply
from ARP import ARPRequest
import Nodo
import Router

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


redeGlobal = Rede()