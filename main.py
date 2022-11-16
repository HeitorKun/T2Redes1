from Reader import Reader
from ARP import ARPRequest
from ARP import ARPReply
# n1 = Nodo(ip = 123, mac = 234)

# n1.executaProtocoloDeRede(ARP(IP("12.12.3.123",12), n1.ip, "request"))

reader = Reader()
reader.read("topologia.txt")

for node in reader.nodes:
  print(node.name)

for router in reader.routers:
  print(router.name)

src = reader.nodes[0]
dst = reader.nodes[1]

# print(reader.rede.dicionarioDeRedes)
for key in reader.rede.dicionarioDeRedes.keys():
  print("key: ", key, reader.rede.dicionarioDeRedes[key])
# arpRequest = ARPRequest(src.ip, dst.ip, src.mac)
# reader.nodes[0].arpRequest()