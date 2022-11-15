
n1 = Nodo(ip = 123, mac = 234)

n1.executaProtocoloDeRede(ARP(IP("12.12.3.123",12), n1.ip, "request"))