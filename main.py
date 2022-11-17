from Reader import Reader
from ARP import ARPRequest
from ICMP import ICMPEchoRequest
from IP import IP
from Nodo import Nodo
from Router import Router

input = list(map(str, input().split()))
nome_arquivo_topologia = input[1]

reader = Reader()
reader.read(nome_arquivo_topologia)

if input[2] == "ping":
  src = reader.nodes[0]
  dst = reader.nodes[3]

  go = True
  current_node = src
  next_node = dst
  gateway = True
  while(go):
    rede = reader.rede
    ttl = 8
    #Se current_node tem mac do next_node, pode mandar ICMP request
    if next_node.ip.ipStr in current_node.arpTable and not gateway:
      
      icmpRequest = ICMPEchoRequest(current_node.ip, next_node.ip, current_node.mac, src.ip, dst.ip, ttl)
      if rede.ICMPEchoRequestReceive(icmpRequest) == 99:
        # time exceeded
        go = False
      elif rede.ICMPEchoRequestReceive(icmpRequest) == 0:
        go = False
      else:
        current_node = next_node
      go = False
    #Se current_node tem mac do gateway(roteador) pode mandar ICMP request
    elif current_node.gateway.ipStr in current_node.arpTable and gateway:
      icmpRequest = ICMPEchoRequest(current_node.ip, next_node.ip, current_node.mac, src.ip, dst.ip, ttl)
      if rede.ICMPEchoRequestReceive(icmpRequest) == 99:
        print(" error time exceeded")
        go = False
      else:
        for r in rede.dicionarioDeRedes[current_node.ip.redeIPInBinaryStr]:
          if isinstance(r, Router):
            for rt in r.routerTableInfos:
              rtIp = rt.net_dest[:-2]
              if  rtIp == dst.ip.ipStr[:-2]:
                if rt.nexthop == "0.0.0.0":
                  ip = rtIp+".1"
                  mac = r.ports[ip]
                  current_node = Nodo(r.name, IP(ip, str(r.mask)), mac, current_node.gateway)
                  go = False
                  
    #Se current_node nao tem mac do next_node ainda, tem que mandar ARP request
    else:
      # Se who esta na outra rede que o tell
      if next_node.ip.redeIPInBinaryStr != current_node.ip.redeIPInBinaryStr:
        new_next_node_ip = current_node.ip.ipStr[:-1] + "1"
        new_next_node = IP(new_next_node_ip, current_node.ip.maskStr)

        arprequest = ARPRequest(new_next_node, current_node.ip, current_node.mac)
        rede.ARPRequestReceive(arprequest)
        gateway = True
      else:
        #Estao na mesma rede, entao soh manda direto
        arprequest = ARPRequest(next_node.ip, current_node.ip, current_node.mac)
        rede = reader.rede
        rede.ARPRequestReceive(arprequest)
        gateway = False
        
elif input[2] == "traceroute":
  print("traceroute execution")
else:
  print("please inform ping or traceroute command")
  exit(0)
