from Reader import Reader
from ARP import ARPRequest
from ARP import ARPReply
# n1 = Nodo(ip = 123, mac = 234)

# n1.executaProtocoloDeRede(ARP(IP("12.12.3.123",12), n1.ip, "request"))

reader = Reader()
reader.read("topologia.txt")



src = reader.nodes[0]
dst = reader.nodes[1]

arprequest = ARPRequest(dst.ip, src.ip, src.mac)
rede = reader.rede
rede.ARPRequestReceive(arprequest)

for node in reader.nodes:
  print(node.name, node.arpTable)

for router in reader.routers:
  print(router.arpTable)
# print(reader.rede.dicionarioDeRedes)
# for key in reader.rede.dicionarioDeRedes.keys():
#   print("key: ", key, reader.rede.dicionarioDeRedes[key])
# arpRequest = ARPRequest(src.ip, dst.ip, src.mac)
# reader.nodes[0].arpRequest()