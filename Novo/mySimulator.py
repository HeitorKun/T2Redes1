# arpTable é matriz onde as linhas tem 2 valores, primeira[0] é ip a segunda[1] é mac
# router table é matriz onde as linhas são [0] = ip, [1] = nextHop(IP, mas se for só zero ele está na rede), [2] = porta 


class entity():
    def __init__(self, ip, mac, arpTable = [], routerTable = []):
        self.ip = ip
        self.mac = mac
        self.arpTable = arpTable



redes = []
#isso esta fora da classe
def portaDeRedeEntrada(entidade , protocol):
    # testar se é arp ou icmp
    
