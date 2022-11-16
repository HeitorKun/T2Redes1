from IP import IP
from MAC import MAC
from NetworkEntities import *
from RouterTableInfo import RouterTableInfo
class Reader:
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
          elif format == 1:
            router = Router(x[0], x[1])
            for portN in range(1, int(router.num_ports)+1):
              macN = 2 ** portN
              ipN = macN + 1

              ipStr = x[ipN][:-3]
              macStr = x[macN]
              
              router.addNewIPAndMac(ipStr, macStr)
              
            self.routers.append(router)
          else:
            routerIp = x[1][:-3]
            routerPrefix = x[1][-2:]
            routerTable = RouterTableInfo(routerIp, routerPrefix, x[2], x[3])
        
            index = int(x[0][1:]) - 1
            self.routers[index].updateNewRouterTable(routerTable)
