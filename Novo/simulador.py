from enum import Enum
import sys

class Topologia:
    def __init__(self, nodes, routers, routertable, nomesNodos):
        self.nodes = nodes
        self.routers = routers
        self.routertable = routertable
        self.nomesNodos = nomesNodos

    def confereRoteador(self, nodo):
        for router in self.routers:
            if nodo in router.nodoRouters:
                return True
        return False

    def getRouterPorNodo(self, nodo):
        for router in self.routers:
            if nodo in router.nodoRouters:
                return router
        return None

class Node:
    def __init__(self, nodeNome, nodeMac, IpNodo, nodeGateway, nodeArptable):
        self.nodeNome = nodeNome
        self.nodeMac = nodeMac
        self.IpNodo = IpNodo
        self.nodeGateway = nodeGateway
        self.nodeArptable = nodeArptable 

class Router:
    def __init__(self, nodeNome, numPortas, nodoRouters):
        self.nodeNome = nodeNome
        self.numPortas = numPortas
        self.nodoRouters = []
        self.nodeArptable = {} 

        for router in nodoRouters:
            self.nodoRouters.append(Node(nodeNome, router[0], router[1], None, self.nodeArptable))
        
class Routertable:
    def __init__(self, nodeNome, destPrefix, nexthop, porta):
        self.nodeNome = nodeNome
        self.destPrefix = destPrefix
        self.nexthop = nexthop
        self.porta = porta
        self.size = len(nodeNome)

class Ethernet:
    def __init__(self, MACOrigem, MACDestino,  tipoProtocolo, dado):
        self.MACOrigem = MACOrigem
        self.MACDestino = MACDestino
        self.tipoProtocolo = tipoProtocolo 
        self.dado = dado 

    def isArp(self):
        return self.tipoProtocolo == "ARP"
    
    def isIp(self):
        return self.tipoProtocolo == "IP"

    def desempacota(self):
        return self.dado

class ARP:
    def __init__(self, MACOrigem, MACDestino, IpOrigem, IpDestino, op):
        self.MACOrigem  = MACOrigem
        self.MACDestino  = MACDestino 
        self.IpDestino   = IpDestino
        self.IpOrigem    = IpOrigem
        self.op = op

    def isArpRequest(self):
        return self.op == 1

    def isArpReply(self):
        return self.op == 2
       
def ARP_Request(nodoOrigem, ipDestino):
    return ARP(nodoOrigem.nodeMac, None, nodoOrigem.IpNodo, ipDestino,  1) 

def ARP_Reply(nodo, arp):
    return ARP(nodo.nodeMac, arp.MACOrigem, nodo.IpNodo, arp.IpOrigem, 2) 

class IP:
    def __init__(self, IpOrigem, IpDestino, tipoProtocolo, dado, ttl=8):
        self.IpOrigem = IpOrigem
        self.IpDestino = IpDestino
        self.dado = dado
        self.tipoProtocolo = tipoProtocolo
        self.ttl = ttl

    def desempacota(self):
        return self.dado

class ICMPType(Enum):
    ERROR_NOTIFICATION = 1
    SEARCH = 2

class ICMPCode(Enum):
    TIME_EXCEED = 11
    ECHO_REQUEST = 8
    ECHO_REPLY = 0

class ICMP:
    def __init__(self, tipoMensagem, codigo):
        self.tipoMensagem = tipoMensagem 
        self.codigo = codigo

def ICMP_Echo_Request():
   return ICMP(ICMPType.SEARCH, ICMPCode.ECHO_REQUEST)

def ICMP_Echo_Reply():
   return ICMP(ICMPType.SEARCH, ICMPCode.ECHO_REPLY)

def lerArquivoTopologia(filePath):
    nodes = []
    routers = []
    routerTable = None
    listaNodos = {}

    f = open(filePath, 'r')

    line = f.readline()
    while True:
        line = f.readline().replace("\n", "")
        if line == "#ROUTER":
            break
        n = line.split(",")
        nodes.append(Node(n[0], n[1], n[2], n[3], {}))
        listaNodos[n[1]] = n[0]

    while True:
        line = f.readline().replace("\n", "")
        if line == "#ROUTERTABLE":
            break
        r = line.split(",")
        listaMacIp = []
        for i in range(2, len(r), 2):
            listaMacIp.append([r[i], r[i+1]])
            listaNodos[r[i]] = r[0]

        routers.append(Router(r[0], r[1], listaMacIp))

    nomesRouters = []
    ipsRouters = []
    nextHopRouters = []
    portRouters = []
    while True:
        line = f.readline().replace("\n", "")
        if not line:
            break
        r = line.split(",")

        nomesRouters.append(r[0])
        ipsRouters.append(r[1])
        nextHopRouters.append(r[2])
        portRouters.append(r[3])
    
    routerTable = Routertable(nomesRouters, ipsRouters, nextHopRouters, portRouters)
    return Topologia(nodes, routers, routerTable, listaNodos)

def binParaDec(bin):
    decimal = int(bin, 2)
    return decimal

def aplicaMascara(endIp, cidr):
    masc = mask(cidr)
    ip = endIp.split(".")
    result = []
    for i in range(len(ip)):
        result.append( str(int(ip[i]) & masc[i]) )
        
    return '.'.join(result)
        
def mask(cidr):
    mascaraBin = []
    mascaraDec = []
    splitter = 0
    mascaraBin.append([])
    
    for it in range(32): 
        if(splitter == 8):
            splitter = 0
            mascaraDec.append(binParaDec(''.join(mascaraBin[-1])))
            mascaraBin.append([])
        
        if it < cidr:
            mascaraBin[-1].append('1')
        else:
            mascaraBin[-1].append('0')
        
        splitter += 1
    
    mascaraDec.append(binParaDec( ''.join( mascaraBin[-1] ) ))
            
    return mascaraDec

def getMask(ip):
    aux = ip.split("/")
    return "/" + aux[1]

def mesmaRede(ip1, ip2):
    aux = ip1.split("/")
    ip1, cidr1 = aux[0], aux[1]
    aux = ip2.split("/")
    ip2 = aux[0]
    
    return aplicaMascara(ip1, int(cidr1)) == aplicaMascara(ip2, int(cidr1))


def envio(pct, topologia):
    if pct.isArp():
        return envioARP(pct, topologia)
    elif pct.isIp():
        return envioIP(pct, topologia)

def envioARP(pct, topologia):
    arp = pct.desempacota()
    
    # envia ARP REQUEST para todos os nodos da rede, menos para si próprio
    if pct.MACDestino == ":FF": # broadcast:
        print("Note over "+ topologia.nomesNodos[pct.MACOrigem] +" : ARP Request<br/>Who has "+ arp.IpDestino.split("/")[0] +"? Tell "+ arp.IpOrigem.split("/")[0])
        for n in topologia.nodes:
            if mesmaRede(arp.IpOrigem, n.IpNodo) and n.IpNodo != arp.IpOrigem:
                res = recebe(n, pct, topologia)
                if res != None:
                    return res
                
        for router in topologia.routers:
            for n in router.nodoRouters:
                if mesmaRede(arp.IpOrigem, n.IpNodo) and n.IpNodo != arp.IpOrigem:
                    res = recebe(n, pct, topologia)
                    if res != None:
                        return res

    else: # envia ARP REPLY para endereço Mac específico
        print(topologia.nomesNodos[pct.MACOrigem] +" ->> "+ topologia.nomesNodos[pct.MACDestino] +" : ARP Reply<br/>"+ arp.IpOrigem.split("/")[0] +" is at "+ arp.MACOrigem)
        for n in topologia.nodes:
            if (n.nodeMac == arp.MACDestino):
                return recebe(n, pct, topologia)
        for router in topologia.routers:
            for n in router.nodoRouters:
                if (n.nodeMac == arp.MACDestino):
                    return recebe(n, pct, topologia)

def envioIP(pct, topologia):
    for n in topologia.nodes:
        if (n.nodeMac == pct.MACDestino):
            return recebe(n, pct, topologia)
    for router in topologia.routers:
            for n in router.nodoRouters:
                if (n.nodeMac == pct.MACDestino):
                    return recebe(n, pct, topologia)

def recebe(nodo, pct, topologia):
    if pct.isArp():
        return recebeArp(nodo, pct, topologia)
    elif pct.isIp():
        return recebeIp(nodo, pct, topologia)

def recebeArp(nodo, pct, topologia):
    
    arp = pct.desempacota()
    if arp.isArpRequest():
        if arp.IpDestino == nodo.IpNodo:
            nodo.nodeArptable[arp.IpOrigem] = arp.MACOrigem
            novoPacoteARP = ARP_Reply(nodo, arp) 
            novoPacoteEthernet = Ethernet(novoPacoteARP.MACOrigem, novoPacoteARP.MACDestino, "ARP" , novoPacoteARP)
            return envio(novoPacoteEthernet, topologia)
    elif arp.isArpReply():
        nodo.nodeArptable[arp.IpOrigem] = arp.MACOrigem

def recebeIp(nodo, pct, topologia):
    ip = pct.desempacota()
    
    if ip.desempacota().tipoMensagem == ICMPType.SEARCH: 
        if ip.desempacota().codigo == ICMPCode.ECHO_REQUEST:
            print(topologia.nomesNodos[pct.MACOrigem] + " ->> " + topologia.nomesNodos[pct.MACDestino] +
            " : ICMP Echo Request<br/>src=" + ip.IpOrigem.split("/")[0] +" dst=" + ip.IpDestino.split("/")[0] +" ttl=" + str(ip.ttl))
        else:
            print(topologia.nomesNodos[pct.MACOrigem] + " ->> " + topologia.nomesNodos[pct.MACDestino] +
            " : ICMP Echo Reply<br/>src=" + ip.IpOrigem.split("/")[0] +" dst=" + ip.IpDestino.split("/")[0] +" ttl=" + str(ip.ttl))
    else:
        print(topologia.nomesNodos[pct.MACOrigem] + " ->> " + topologia.nomesNodos[pct.MACDestino] +
            " : ICMP Time Exceeded<br/>src=" + ip.IpOrigem.split("/")[0] +" dst=" + ip.IpDestino.split("/")[0] +" ttl=" + str(ip.ttl))
    
    
    if not mesmaRede(nodo.IpNodo, ip.IpDestino):
        if topologia.confereRoteador(nodo):
            return redirecionaNetwork(nodo, ip, topologia)
        else:
            return redirecionamentoDefault(nodo, ip, topologia)

    else: 
        return recebeICMP(nodo, pct, topologia) 

def recebeICMP(nodo, pct, topologia):
    ip = pct.desempacota()
    icmp = ip.desempacota()
        
    if icmp.tipoMensagem == ICMPType.SEARCH: 
        if icmp.codigo == ICMPCode.ECHO_REQUEST:
            novoIpOrigem = ip.IpDestino
            novoIpDestino = ip.IpOrigem
            
            pacoteICMP = ICMP_Echo_Reply()
            pacoteIP = IP(novoIpOrigem, novoIpDestino, "ICMP", pacoteICMP)             
            
            if not mesmaRede(novoIpOrigem, novoIpDestino):
                return redirecionamentoDefault(nodo, pacoteIP, topologia)
            else:
                if not ip.IpOrigem in nodo.nodeArptable:
                    PacoteARP = ARP_Request(nodo, ip.IpOrigem)
                    pacoteEthernet = Ethernet(nodo.nodeMac, ":FF", "ARP", PacoteARP)
                    envio(pacoteEthernet, topologia)
                pacoteEthernet = Ethernet(nodo.nodeMac, nodo.nodeArptable[ip.IpOrigem], "IP", pacoteIP)
                return envio(pacoteEthernet, topologia)

        elif icmp.codigo == ICMPCode.ECHO_REPLY:
            return ICMPCode.ECHO_REPLY
    else:
        return ICMPCode.TIME_EXCEED


def redirecionamentoDefault(nodo, ip, topologia):
    ipDestino = nodo.nodeGateway + getMask(nodo.IpNodo) 
    if not ipDestino in nodo.nodeArptable: 
        PacoteARP = ARP_Request(nodo, ipDestino)
        pacoteEthernet = Ethernet(nodo.nodeMac, ":FF", "ARP", PacoteARP)
        
    
    pacoteEthernet = Ethernet(nodo.nodeMac, nodo.nodeArptable[ipDestino], "IP", ip)
    return envio(pacoteEthernet, topologia)

def redirecionaNetwork(nodo, ip, topologia, discount = True):
    router = topologia.getRouterPorNodo(nodo)
    pacoteIP = None
    
    if ip.ttl-1 == 0 and ip.tipoProtocolo == "ICMP":
        if ip.dado.codigo == ICMPCode.TIME_EXCEED: 
            return None
        
        pacoteIP = IP(nodo.IpNodo, ip.IpOrigem, "ICMP", ICMP(ICMPType.ERROR_NOTIFICATION, ICMPCode.TIME_EXCEED),8)
        if not mesmaRede(pacoteIP.IpOrigem, pacoteIP.IpDestino):
            return redirecionaNetwork(nodo, pacoteIP, topologia, False)
        else:
            if not pacoteIP.IpDestino in nodo.nodeArptable:
                PacoteARP = ARP_Request(nodo, pacoteIP.IpDestino)
                pacoteEthernet = Ethernet(nodo.nodeMac, ":FF", "ARP", PacoteARP)
                envio(pacoteEthernet, topologia)

            pacoteEthernet = Ethernet(nodo.nodeMac, nodo.nodeArptable[pacoteIP.IpDestino], "IP", pacoteIP)
            return envio(pacoteEthernet, topologia)
    else:
        for linha in range(topologia.routertable.size): 
            rtNome = topologia.routertable.nodeNome[linha]
            rtIP = topologia.routertable.destPrefix[linha]
            rtInterface = topologia.routertable.nexthop[linha]
            rtPorta = topologia.routertable.porta[linha]

            if rtNome == nodo.nodeNome and mesmaRede(rtIP, ip.IpDestino):
                nodoRouter = router.nodoRouters[int(rtPorta)] 
                arpIP = None

                
                if rtInterface == "0.0.0.0": 
                    arpIP = ip.IpDestino
                else:
                    arpIP = rtInterface + getMask(nodoRouter.IpNodo) 

                
                ttl = ip.ttl
                if discount == True:
                    ttl -=1
                    pacoteIP = IP(ip.IpOrigem, ip.IpDestino, "ICMP", ip.dado, ttl) 
                else:
                    ipOrigem = nodoRouter.IpNodo 
                    pacoteIP = IP(ipOrigem, ip.IpDestino, "ICMP", ip.dado, ttl)


                
                if not arpIP in router.nodeArptable:
                    PacoteARP = ARP_Request(nodoRouter, arpIP)
                    pacoteEthernet = Ethernet(nodoRouter.nodeMac, ":FF", "ARP", PacoteARP)
                    envio(pacoteEthernet, topologia)
                pacoteEthernet = Ethernet(nodoRouter.nodeMac, router.nodeArptable[arpIP], "IP", pacoteIP)
                return envio(pacoteEthernet, topologia)


# PING
def ping(nodeOrigem, nodeDestino): 
    ipDestino = None
    if mesmaRede(nodeOrigem.IpNodo, nodeDestino.IpNodo): #verifica se está na mesma rede e altera ipDest
        ipDestino = nodeDestino.IpNodo
    else:
        ipDestino = nodeOrigem.nodeGateway + "/" +nodeOrigem.IpNodo.split("/")[1]

    PacoteARP = ARP_Request(nodeOrigem, ipDestino) #cria pacote ARP
    pacoteEthernet = Ethernet(nodeOrigem.nodeMac, ":FF", "ARP", PacoteARP) #cria pacoteEth
    envio(pacoteEthernet, topo)

    pacoteICMP = ICMP_Echo_Request()
    pacoteIp = IP(nodeOrigem.IpNodo, nodeDestino.IpNodo, "ICMP", pacoteICMP)
    pacoteEthernet = Ethernet(nodeOrigem.nodeMac, nodeOrigem.nodeArptable[ipDestino], "IP", pacoteIp)
    envio(pacoteEthernet, topo)

# TRACEROUTE
def traceroute(nodeOrigem, nodeDestino):
    ipDestino = None
    if mesmaRede(nodeOrigem.IpNodo, nodeDestino.IpNodo): #verifica se está na mesma rede e altera ipDest
        ipDestino = nodeDestino.IpNodo
    else:
        ipDestino = nodeOrigem.nodeGateway + "/" +nodeOrigem.IpNodo.split("/")[1]

    PacoteARP = ARP_Request(nodeOrigem, ipDestino) #cria pacote ARP
    pacoteEthernet = Ethernet(nodeOrigem.nodeMac, ":FF", "ARP", PacoteARP) #cria pacoteEth
    envio(pacoteEthernet, topo)

    ttl_cont = 1
    while ttl_cont <= 8: #loop incremental do ttl de reqs ICMP_Echo_Request até receber ECHO_REPLY
        pacoteICMP = ICMP_Echo_Request()
        pacoteIp = IP(nodeOrigem.IpNodo, nodeDestino.IpNodo, "ICMP", pacoteICMP, ttl_cont)
        pacoteEthernet = Ethernet(nodeOrigem.nodeMac, nodeOrigem.nodeArptable[ipDestino], "IP", pacoteIp)
        reply = envio(pacoteEthernet, topo)
        if reply  == ICMPCode.ECHO_REPLY or reply == None:
            break
        ttl_cont += 1


topologia = sys.argv[1]
comando = sys.argv[2]
origem = sys.argv[3]
destino = sys.argv[4]

topo = lerArquivoTopologia(topologia)
nodoOrigem = [p for p in topo.nodes if p.nodeNome == origem][0] 
nodoDestino = [p for p in topo.nodes if p.nodeNome == destino][0]



if comando == "ping":
    ping(nodoOrigem, nodoDestino)
elif comando == "traceroute":
    traceroute(nodoOrigem, nodoDestino)