from ARP import ARPReply
from ARP import ARPRequest
from IP import IP
from MAC import MAC
from Nodo import Nodo
from Router import Router

class Rede:
    dicionarioDeRedes = {}
    def __init__(self):
        pass
    
    def adicionaNodo(self, nodo: Nodo):
        if nodo.ip.redeIPInBinaryStr in Rede.dicionarioDeRedes:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr].append(nodo)
        else:
            Rede.dicionarioDeRedes[nodo.ip.redeIPInBinaryStr] = [nodo]

    def adicionaRouter(self, router: Router):
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


redeGlobal = Rede()