from IP import IP
from MAC import MAC
from Nodo import Nodo
from Router import Router
from RouterTableInfo import RouterTableInfo
import Rede
class Reader:
  rede = Rede.redeGlobal
  nodes = []
  routers = [] 
  def read(self, name):
    with open(name) as f:
      format = 0
      for line in f.readlines():
        x = line.strip().split(',')
        if x[0] == "#NODE":
          format = 0
        elif x[0] == "#ROUTER":
          format = 1
        elif x[0] == "#ROUTERTABLE":
          format = 2
        else: 
          if format == 0:
            name = x[0]

            mac = MAC(x[1])

            ipStr = x[2][:-3]
            ipMaskStr = x[2][-2:]
            ip = IP(ipStr, ipMaskStr)

            gateway = x[3]

            node = Nodo(name, ip, mac, gateway)
            self.nodes.append(node)
            self.rede.adicionaNodo(node)
          elif format == 1:
            router = Router(x[0], x[1])
            for portN in range(1, int(router.numberOfPorts)+1):
              macN = 2 ** portN
              ipN = macN + 1

              ipStr = x[ipN][:-3]
              ipMaskStr = x[ipN][-2:]
              macStr = x[macN]
              
              auxIp = IP(ipStr, ipMaskStr)
              auxMac = MAC(macStr)
              router.addNewIPAndMac(auxIp, auxMac)
              
            self.routers.append(router)
            self.rede.adicionaRouter(router)
          else:
            routerIp = x[1][:-3]
            routerPrefix = x[1][-2:]
            routerTable = RouterTableInfo(routerIp, routerPrefix, x[2], x[3])
        
            index = int(x[0][1:]) - 1
            self.routers[index].updateNewRouterTable(routerTable)
