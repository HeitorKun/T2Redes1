from Reader import Reader
from ARP import ARPRequest
from ICMP import ICMPEchoRequest
from IP import IP
# n1 = Nodo(ip = 123, mac = 234)

# n1.executaProtocoloDeRede(ARP(IP("12.12.3.123",12), n1.ip, "request"))
input = list(map(str, input().split()))
nome_arquivo_topologia = input[1]

reader = Reader()
reader.read(nome_arquivo_topologia)

if input[2] == "ping":
  print("ping execution to be prepared")
  src = reader.nodes[0]
  dst = reader.nodes[3]

  go = True

  while(go):
    rede = reader.rede
    current_node = src
    next_node = dst
    #Se current_node tem mac do next_node, pode mandar ICMP request
    if next_node.ip.ipStr in current_node.arpTable:
      icmpRequest = ICMPEchoRequest(current_node.ip, next_node.ip, current_node.mac, src.ip, dst.ip, ttl)
      rede.ICMPEchoRequestReceive(icmpRequest)
      go = False
    #Se current_node tem mac do gateway(roteador) pode mandar ICMP request
    elif current_node.gateway.ipStr in current_node.arpTable:
      icmpRequest = ICMPEchoRequest(current_node.ip, next_node.ip, current_node.mac)
      go = False
    #Se current_node nao tem mac do next_node ainda, tem que mandar ARP request
    else:
      # Se who esta na outra rede que o tell
      if next_node.ip.redeIPInBinaryStr != current_node.ip.redeIPInBinaryStr:
        new_next_node_ip = current_node.ip.ipStr[:-1] + "1"
        new_next_node = IP(new_next_node_ip, current_node.ip.maskStr)

        arprequest = ARPRequest(new_next_node, current_node.ip, current_node.mac)
        rede.ARPRequestReceive(arprequest)
      else:
        #Estao na mesma rede, entao soh manda direto
        arprequest = ARPRequest(next_node.ip, current_node.ip, current_node.mac)
        rede = reader.rede
        rede.ARPRequestReceive(arprequest)

    # for node in reader.nodes:
        #   print(node.name, node.arpTable)

        # for router in reader.routers:
        #   print(router.name, router.arpTable)
        print(src.arpTable)

elif input[2] == "traceroute":
  print("traceroute execution")
else:
  print("please inform ping or traceroute command")
  exit(0)



# print(reader.rede.dicionarioDeRedes)
# for key in reader.rede.dicionarioDeRedes.keys():
#   print("key: ", key, reader.rede.dicionarioDeRedes[key])
# arpRequest = ARPRequest(src.ip, dst.ip, src.mac)
# reader.nodes[0].arpRequest()