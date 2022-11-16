
import sys

in_file = ''
command = ''
source  = ''
destiny = ''

def read_input():
    global in_file, command, source, destiny

    in_file = sys.argv[1]
    command = sys.argv[2]
    source = sys.argv[3]
    destiny = sys.argv[4]
    
read_input()

nodes = []
routers = []
routertable = []
with open(in_file, 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        if line == '#ROUTER':
            break
        nodes.append(line)
    nodes.remove('#NODE')
    for line in lines:
        if line in nodes:
            continue
        if line == '#ROUTERTABLE':
            break
        routers.append(line)
    routers.remove('#NODE')
    routers.remove('#ROUTER')
    for line in lines:
        if line in nodes or line in routers:
            continue
        routertable.append(line)
    routertable.remove('#NODE')
    routertable.remove('#ROUTER')
    routertable.remove('#ROUTERTABLE')


class Node():
    arp_table = {}
    def __init__(self, node_name, mac, ip_prefix, gateway, arp_table):
        self.node_name = node_name
        self.mac = mac
        self.ip_prefix = ip_prefix
        self.gateway = gateway
        self.arp_table = arp_table

    def update_arp_table(self, ip, mac):
        self.arp_table.update({ip:mac})

    def print_node(self):
        print(self.node_name, self.mac, self.ip_prefix, self.gateway, self.arp_table)
    
nodes = [n.split(',') for n in nodes]    
nodes = [Node(n[0],n[1],n[2],n[3], {}) for n in nodes]
# print('Nodes')
# for n in nodes:
#     print(n.node_name)


class Router():
    arp_table = {}
    def __init__(self, router_name, num_ports, mac_iprefix, arp_table):
        self.router_name = router_name
        self.num_ports = num_ports
        self.mac_iprefix = mac_iprefix
        self.arp_table = arp_table

    def update_arp_table(self, ip, mac):
        self.arp_table.update({ip:mac})
        
    def print_router(self):
        print(self.router_name, self.num_ports, self.mac_iprefix)

routers = [r.split(',') for r in routers]
i = 0

router = []
for i in range(len(routers)):
    mac_ip = []
    mac_ip.append(routers[i][2:])
    macs = []
    ips = []
    for mi in mac_ip:
        j = 0
        for j in range(len(mi)):
            if mi[j].__contains__(':'):
                macs.append(mi[j])
            else:
                ips.append(mi[j])
    mac_ip = [(mac,ip) for mac,ip in zip(macs, ips)]
    r = Router(routers[i][0],routers[i][1], mac_ip, {})
    router.append(r)

routers = router
        

    #print(routers)
# print('Routers')
# for r in routers:
#     r.print_router()


class Routertable():
    def __init__(self, router_name, net_dest_prefix, nexthop, port):
        self.router_name = router_name
        self.net_dest_prefix = net_dest_prefix
        self.nexthop = nexthop	
        self.port = port

    def print_routertable(self):
        print(self.router_name, self.net_dest_prefix, self.nexthop, self.port)

routertable = [rt.split(',') for rt in routertable]
routertable = [Routertable(rt[0],rt[1],rt[2],rt[3]) for rt in routertable]
# print('Routertable')
# for rt in routertable:
#     rt.print_routertable()


def icmp_echo_request(src, dst, ttl): #origem/destino
    src_ip = ''
    dst_ip = ''
    
    if source.startswith('n'): # se a origem é um nodo
        for n in nodes:
            if n.node_name == source:
                src_ip = n.ip_prefix.split('/')[0]
    
    if destiny.startswith('n'): # se o destino é um nodo
        for n in nodes:
            if n.node_name == destiny:
                dst_ip = n.ip_prefix.split('/')[0]
    
    package = f'{src} ->> {dst} : ICMP Echo Request<br/>src={src_ip} dst={dst_ip} ttl={ttl}'
    return package

# result = icmp_echo_request(source, destiny)
# print(result)

def icmp_echo_reply(src, dst, ttl):
    src_ip = ''
    dst_ip = ''

    if source.startswith('n'): # se a origem é um nodo
        for n in nodes:
            if n.node_name == source:
                src_ip = n.ip_prefix.split('/')[0]
    
    if destiny.startswith('n'): # se o destino é um nodo
        for n in nodes:
            if n.node_name == destiny:
                dst_ip = n.ip_prefix.split('/')[0]

    package = f'{src} ->> {dst} : ICMP Echo Reply<br/>src={dst_ip} dst={src_ip} ttl={ttl}'
    return package

def icmp_echo_time_exceeded(src, dst, lost, final_destiny, ttl):
    dst_ip = ''

    if source.startswith('n'): # se a origem é um nodo
        for n in nodes:
            if n.node_name == final_destiny:
                dst_ip = n.ip_prefix.split('/')[0]

    package = f'{src} ->> {dst} : ICMP Time Exceeded<br/>src={lost} dst={dst_ip} ttl={ttl}'
    return package

# arp table n1 - ip/mac
# n1 -> r1
# n1 pede o mac do r1
# atualiza tabela arp de n1 com ip e mac do r1

def arp_request(src, ip_dst, ip_src):
    package = f'Note over {src} : ARP Request<br/>Who has {ip_dst}? Tell {ip_src}'
    return package


def arp_reply(dst, src, ip_dst, mac_dst):
    package = f'{dst} ->> {src} : ARP Reply<br/>{ip_dst} is at {mac_dst}'
    return package

#funções que retornam o nodo ou o roteador

def get_router(x):
    if x.startswith('r'):
        for r in routers:
            if r.router_name == x:
                return r
    else:
        for r in routers:
            i = 0
            for i in range(len(r.mac_iprefix)):
                if r.mac_iprefix[i][1].__contains__(x):
                    return r.router_name

def get_node(x):
    for n in nodes:
        if n.node_name == x:
            return n

def is_the_same_network(x,y):
    src_net = []
    dst_net = []

    if x.startswith('r'):
        r = get_router(x)
        ips = r.mac_iprefix
        i = 0
        j = 0
        for i in range(len(ips)):
            aux = ips[i][1].split('/')
            mask = int(aux[1])/8
            net = aux[0].split('.')
            src = ''
            for j in range(len(net)):
                if j >= mask:
                    net[j] = '0'
                if j == len(net)-1:
                    src = src + net[j]
                else:
                    src = src + net[j] + '.'
            src_net.append(src)

    
    if y.startswith('r'):
        r = get_router(y)
        ips = r.mac_iprefix
        i = 0
        j = 0
        for i in range(len(ips)):
            aux = ips[i][1].split('/')
            mask = int(aux[1])/8
            net = aux[0].split('.')
            dst = ''
            for j in range(len(net)):
                if j >= mask:
                    net[j] = '0'
                if j == len(net)-1:
                    dst = dst + net[j]
                else:
                    dst = dst + net[j] + '.'
            dst_net.append(dst)

    if x.startswith('n'):
        n = get_node(x)
        aux = n.ip_prefix.split('/')
        mask = int(aux[1])/8
        net = aux[0].split('.')
        i = 0
        src = ''
        for i in range(len(net)):
            if i >= mask:
                net[i] = '0'
            if i == len(net)-1:
                src = src + net[i]
            else:
                src = src + net[i] + '.'
        src_net.append(src)
    
    if y.startswith('n'):
        n = get_node(y)
        aux = n.ip_prefix.split('/')
        mask = int(aux[1])/8
        net = aux[0].split('.')
        i = 0
        dst = ''
        for i in range(len(net)):
            if i >= mask:
                net[i] = '0'
            if i == len(net)-1:
                dst = dst + net[i]
            else:
                dst = dst + net[i] + '.'
        dst_net.append(dst)
                
    ocorrencia = 0
                
    #retorna mais de 1 se estão na mesma rede e 0 se não estão na mesma rede
    i = 0
    j = 0
    for i in range(len(src_net)):
        for j in range(len(dst_net)):
            if src_net[i] == dst_net[j]:
                ocorrencia += 1
    return ocorrencia

def get_getway(x):
    getway = []
    if x.startswith('n'):
        for n in nodes:
            if n.node_name == x:
                getway.append(n.gateway)
        for r in routers:
            j = 0
            for j in range(len(r.mac_iprefix)):
                if r.mac_iprefix[j][1].__contains__(getway[0]):
                    getway.append(r.router_name)
                    getway.append(r.mac_iprefix[j][0])

    if x.startswith('r'):
        ip_dst = ''
        name = ''
        mac = ''
        
        for r in routertable:
            if r.router_name == x and r.net_dest_prefix == '0.0.0.0/0':
                ip_dst = r.nexthop
        for r in routers:
            j = 0
            for j in range(len(r.mac_iprefix)):
                if r.mac_iprefix[j][1].__contains__(ip_dst):
                    name = r.router_name
                    mac = r.mac_iprefix[j][0]
        getway.append(ip_dst)
        getway.append(name)
        getway.append(mac)    

    return getway


def get_information(src, dst):
    ip_src = ''
    ip_dst = ''
    mac_dst = ''
    mac_src = ''
    info = []
    if src.startswith('n') and dst.startswith('n'):
        s = get_node(src)
        d = get_node(dst)
        ip_src = s.ip_prefix.split('/')[0]
        ip_dst = d.ip_prefix.split('/')[0]
        mac_dst = d.mac
        mac_src = s.mac
    if src.startswith('r') and dst.startswith('n'):
        s = get_router(src)
        d = get_node(dst)
        ip_dst = d.ip_prefix.split('/')[0]
        mac_dst = d.mac
        getway = get_getway(dst)
        ip_src = getway[0]
        mac_src = getway[2]
    if src.startswith('n') and dst.startswith('r'):
        s = get_node(src)
        d = get_router(dst)
        ip_src = s.ip_prefix.split('/')[0]
        mac_src = s.mac
        getway = get_getway(src)
        mac_dst = getway[2]
        ip_dst = getway[0]
    if src.startswith('r') and dst.startswith('r'):
        s = get_router(src)
        d = get_router(dst)
        getway = get_getway(src)
        mac_dst = getway[2]
        ip_dst = getway[0]
        i = 0
        for i in range(len(s.mac_iprefix)):
            aux = s.mac_iprefix[i][1].split('/')
            mask = int(int(aux[1])/8)
            net1 = ip_dst.split('.')
            net2 = aux[0].split('.')
            j = 0
            res1 = ''
            res2 = ''
            for j in range(len(net1)):
                if j >= mask:
                    net1[j] = '0'
                    net2[j] = '0'
                if j == len(net1)-1:
                    res1 = res1 + net1[j]
                    res2 = res2 + net2[j]
                else:
                    res1 = res1 + net1[j] + '.'
                    res2 = res2 + net2[j] + '.'
            if res1 == res2:
                ip_src = aux[0]
            for r in routers:
                z = 0
                for z in range(len(r.mac_iprefix)):
                    if r.mac_iprefix[z][1].__contains__(ip_src):
                        mac_src = r.mac_iprefix[z][0]

    info.append(ip_src)
    info.append(ip_dst)
    info.append(mac_dst)
    info.append(mac_src)
    return info

def update_arptable(name, ip, mac):
    if name.startswith('r'):
        for r in routers:
            if r.router_name == name:
                r.arp_table.update({ip:mac})
    if name.startswith('n'):
        for n in nodes:
            if n.node_name == name:
                n.arp_table.update({ip:mac})

def check_arptable(src, dst):
    ip_dst = []
    mac = ''
    if dst.startswith('r'): 
        for r in routers:
            if r.router_name == dst:
                i = 0
                for i in range(len(r.mac_iprefix)):
                    ip_dst.append(r.mac_iprefix[i][1].split('/')[0])

    if dst.startswith('n'): 
        for n in nodes:
            if n.node_name == dst:
                ip_dst.append(n.ip_prefix.split('/')[0])

    if src.startswith('r'):
        for r in routers:
            if r.router_name == src:
                for a in r.arp_table:
                    i = 0
                    for i in range(len(ip_dst)):
                        if a == ip_dst[i]:
                            mac = r.arp_table.get(a)

    if src.startswith('n'):
        for n in nodes:
            if n.node_name == src:
                for a in n.arp_table:
                    i = 0
                    for i in range(len(ip_dst)):
                        if a == ip_dst[i]:
                            mac = n.arp_table.get(a)

    return mac

def check_routertable(x, ip):
    ip_dst = ''
    if x.startswith('r'):
        for r in routertable:
            if r.router_name == x:
                aux = r.net_dest_prefix.split('/')
                mask = int(aux[1])/8
                net = aux[0].split('.')
                i = 0
                dst = ''
                for i in range(len(net)):
                    if i < mask:
                        dst = dst + net[i] + '.'
                if ip.__contains__(dst) and dst != '':
                    ip_dst = r.nexthop
    return ip_dst

def getnamewithip(ip):
    name = ''
    for n in nodes:
        if n.ip_prefix.__contains__(ip):
            name = n.node_name

    for r in routers:
        z = 0
        for z in range(len(r.mac_iprefix)):
            if r.mac_iprefix[z][1].__contains__(ip):
                name = r.router_name

    return name

def getmacsandips(src, dst, ip):
    mac_dst = ''
    mac_src = ''
    ip_src = ''
    info = []
    for r in routers:
        i = 0
        if i in range(len(r.mac_iprefix)):
            if r.router_name != dst:
                aux = r.mac_iprefix[i][1].split('/')
                mask = int(int(aux[1])/8)
                net1 = ip.split('.')
                net2 = aux[0].split('.')
                j = 0
                res1 = ''
                res2 = ''
                for j in range(len(net1)):
                    if j >= mask:
                        net1[j] = '0'
                        net2[j] = '0'
                    if j == len(net1)-1:
                        res1 = res1 + net1[j]
                        res2 = res2 + net2[j]
                    else:
                        res1 = res1 + net1[j] + '.'
                        res2 = res2 + net2[j] + '.'
                if res1 == res2:
                    ip_src = aux[0]
    for r in routers:
        j = 0
        for j in range(len(r.mac_iprefix)):
            if r.mac_iprefix[j][1].__contains__(ip):
                mac_dst = r.mac_iprefix[j][0]
            if r.mac_iprefix[j][1].__contains__(ip_src):
                mac_src = r.mac_iprefix[j][0]
    info.append(mac_dst)
    info.append(mac_src)
    info.append(ip_src)
    return info


def ping(x, y):
    src = x
    dst = y
    result = ''
    ttl_req = 8
    ttl_rep = 8
    ttl_exc = 8

    lost = ''
    name_lost = ''
    while(src != dst): 
        new_src = ''
        ip_lost = ''
        if ttl_req > 0:
            info = get_information(src, dst)
            ip_destiny = check_routertable(src, info[1])
            if is_the_same_network(src, dst) > 0:
                info = get_information(src, dst)
                ip_src = info[0]
                ip_dst = info[1]
                mac_dst = info[2]
                result += arp_request(src, ip_dst, ip_src) + '\n'
                update_arptable(dst, ip_src, info[3])
                result += arp_reply(dst, src, ip_dst, mac_dst) + '\n'
                update_arptable(src, ip_dst, mac_dst)
                result += icmp_echo_request(src,dst, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    info = get_information(dst, src)
                    ip_lost = info[0]
                    name_lost = dst
                    ttl_exc = 8
                new_src = dst
            elif ip_destiny == '': 
                getway = get_getway(src)
                name = getway[1]
                info = get_information(src, name)
                ip_src = info[0]
                ip_dst = info[1]
                mac_dst = info[2]
                result += arp_request(src, ip_dst, ip_src) + '\n'
                update_arptable(name, ip_src, info[3])
                result += arp_reply(name, src, ip_dst, mac_dst) + '\n'
                update_arptable(src, ip_dst, mac_dst)
                result += icmp_echo_request(src,name, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    info = get_information(name, src)
                    ip_lost = info[0]
                    name_lost = name
                    ttl_exc = 8
                new_src = name
            elif ip_destiny != '':
                name = getnamewithip(ip_destiny)
                macs = getmacsandips(src, name, ip_destiny)
                result += arp_request(src, ip_destiny, macs[2]) + '\n'
                update_arptable(name, macs[2], macs[1])
                result += arp_reply(name, src, ip_destiny, macs[0]) + '\n'
                update_arptable(src, ip_destiny, macs[0])
                result += icmp_echo_request(src,name, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    ip_lost = ip_destiny
                    name_lost = name
                    ttl_exc = 8
                new_src = name     
            src = new_src
            lost = ip_lost
            if ttl_rep <=0:
                src = name_lost
        else:
            if ttl_exc > 0:
                dst = x
                info = get_information(src, dst)
                ip_destiny = check_routertable(src, info[1])
                mac = check_arptable(src, dst)
                new_src = ''
                if mac != '':
                    result += icmp_echo_time_exceeded(src, dst, lost, x, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = dst
                elif ip_destiny != '':
                    name = getnamewithip(ip_destiny)
                    result += icmp_echo_time_exceeded(src, name, lost, x, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = name
                else:
                    getway = get_getway(src)
                    mac = check_arptable(src, getway[1])
                    if mac != '':
                        result += icmp_echo_time_exceeded(src, getway[1], lost, x, ttl_exc) + '\n'
                        ttl_exc -= 1
                        new_src = name
                src = new_src
            else:
                break

    dst = x
    lost = ''
    name_lost = ''

    while(src != dst and ttl_req > 0): 
        new_src = ''
        ip_lost = ''
        if ttl_rep > 0:
            mac = check_arptable(src, dst)
            if mac != '':
                result += icmp_echo_reply(src, dst, ttl_rep) + '\n'
                ttl_rep -= 1
                if (ttl_rep <= 0):
                    info = get_information(dst, src)
                    ip_lost = info[0]
                    name_lost = dst
                    ttl_exc = 8
                new_src = dst
            else:
                getway = get_getway(src)
                mac = check_arptable(src, getway[1])
                info = get_information(src, dst)
                ip_destiny = check_routertable(src, info[1])
                if mac != '':
                    result += icmp_echo_reply(src, getway[1], ttl_rep) + '\n'
                    ttl_rep -= 1
                    if (ttl_rep <= 0):
                        info = get_information(getway[1], src)
                        ip_lost = info[0]
                        name_lost = getway[1]
                        ttl_exc = 8
                    new_src = getway[1]
                elif ip_destiny != '':
                    name = getnamewithip(ip_destiny)
                    result += icmp_echo_reply(src, name, ttl_rep) + '\n'
                    ttl_rep -= 1
                    if (ttl_rep <= 0):
                        info = get_information(name, src)
                        ip_lost = info[0]
                        name_lost = name
                        ttl_exc = 8
                    new_src = name
                else:
                    getway = get_getway(src)
                    name = getway[1]
                    info = get_information(src, name)
                    ip_src = info[0]
                    ip_dst = info[1]
                    mac_dst = info[2]
                    result += arp_request(src, ip_dst, ip_src) + '\n'
                    update_arptable(name, ip_src, info[3])
                    result += arp_reply(name, src, ip_dst, mac_dst) + '\n'
                    update_arptable(src, ip_dst, mac_dst)
                    result += icmp_echo_reply(src,name, ttl_rep) + '\n'
                    ttl_rep -= 1
                    if (ttl_rep <= 0):
                        info = get_information(getway[1], src)
                        ip_lost = info[0]
                        name_lost = getway[1]
                        ttl_exc = 8
                    new_src = name
            src = new_src
            lost = ip_lost
            if ttl_rep <=0:
                src = name_lost
        else:
            if ttl_exc > 0:
                dst = y
                mac = check_arptable(src, dst)
                info = get_information(src, dst)
                ip_destiny = check_routertable(src, info[1])
                new_src = ''
                if mac != '':
                    result += icmp_echo_time_exceeded(src, dst, lost, y, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = dst
                elif ip_destiny != '':
                    name = getnamewithip(ip_destiny)
                    result += icmp_echo_time_exceeded(src, name, lost, x, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = name
                else:
                    getway = get_getway(src)
                    mac = check_arptable(src, getway[1])
                    if mac != '':
                        result += icmp_echo_time_exceeded(src, getway[1], lost, y, ttl_exc) + '\n'
                        ttl_exc -= 1
                        new_src = name
                src = new_src
            else:
                break
        
    return result

def traceroute(x, y):
    src = x
    dst = y
    result = ''
    ttl_req = 1
    last_ttlreq = 1
    ttl_rep = 8
    ttl_exc = 8

    lost = ''
    name_lost = ''
    while (src != y and ttl_exc > 0):
        new_src = ''
        new_dst = ''
        dst = y
        ip_lost = ''
        if ttl_req > 0:
            info = get_information(src, dst)
            ip_destiny = check_routertable(src, info[1])
            mac = check_arptable(src, dst)
            getway = get_getway(src)
            mac2 = check_arptable(src, getway[1])
            if is_the_same_network(src, dst) > 0:
                info = get_information(src, dst)
                ip_src = info[0]
                ip_dst = info[1]
                mac_dst = info[2]
                result += arp_request(src, ip_dst, ip_src) + '\n'
                update_arptable(dst, ip_src, info[3])
                result += arp_reply(dst, src, ip_dst, mac_dst) + '\n'
                update_arptable(src, ip_dst, mac_dst)
                result += icmp_echo_request(src,dst, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    info = get_information(dst, src)
                    ip_lost = info[0]
                    name_lost = dst
                    ttl_exc = 8
                new_src = dst
            elif mac == '' and mac2 == '' and ip_destiny == '': 
                getway = get_getway(src)
                name = getway[1]
                info = get_information(src, name)
                ip_src = info[0]
                ip_dst = info[1]
                mac_dst = info[2]
                result += arp_request(src, ip_dst, ip_src) + '\n'
                update_arptable(name, ip_src, info[3])
                result += arp_reply(name, src, ip_dst, mac_dst) + '\n'
                update_arptable(src, ip_dst, mac_dst)
                result += icmp_echo_request(src,name, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    ip_lost = info[1]
                    name_lost = name
                    ttl_exc = 8
                new_src = name
            elif mac == '' and mac2 != '':
                getway = get_getway(src)
                result += icmp_echo_request(src, getway[1], ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    info = get_information(getway[1], src)
                    ip_lost = info[0]
                    name_lost = getway[1]
                    ttl_exc = 8
                new_src = getway[1]
            elif mac != '':
                result += icmp_echo_request(src, dst, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    info = get_information(dst, src)
                    ip_lost = info[0]
                    name_lost = dst
                    ttl_exc = 8
                new_src = dst
            elif ip_destiny != '':
                name = getnamewithip(ip_destiny)
                macs = getmacsandips(src, name, ip_destiny)
                result += arp_request(src, ip_destiny, macs[2]) + '\n'
                update_arptable(name, macs[2], macs[1])
                result += arp_reply(name, src, ip_destiny, macs[0]) + '\n'
                update_arptable(src, ip_destiny, macs[0])
                result += icmp_echo_request(src,name, ttl_req) + '\n'
                ttl_req -= 1
                if (ttl_req <= 0):
                    ip_lost = ip_destiny
                    name_lost = name
                    ttl_exc = 8
                new_src = name
            src = new_src
            lost = ip_lost
            if ttl_req <= 0:
                src = name_lost
        else:
            if ttl_exc > 0:
                dst = x
                info = get_information(src, dst)
                ip_destiny = check_routertable(src, info[1])
                mac = check_arptable(src, dst)
                new_src = ''
                if mac != '':
                    result += icmp_echo_time_exceeded(src, dst, lost, x, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = dst
                elif ip_destiny != '':
                    name = getnamewithip(ip_destiny)
                    result += icmp_echo_time_exceeded(src, name, lost, x, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = name
                elif mac == '' and ip_destiny == '':
                    getway = get_getway(src)
                    mac = check_arptable(src, getway[1])
                    if mac != '':
                        result += icmp_echo_time_exceeded(src, getway[1], lost, x, ttl_exc) + '\n'
                        ttl_exc -= 1
                        new_src = getway[1]
                    else:
                        getway = get_getway(src)
                        name = getway[1]
                        info = get_information(src, name)
                        ip_src = info[0]
                        ip_dst = info[1]
                        mac_dst = info[2]
                        result += arp_request(src, ip_dst, ip_src) + '\n'
                        update_arptable(name, ip_src, info[3])
                        result += arp_reply(name, src, ip_dst, mac_dst) + '\n'
                        update_arptable(src, ip_dst, mac_dst)
                        lost = ip_src
                        result += icmp_echo_time_exceeded(src, name, ip_src, x, ttl_exc) + '\n'
                        new_src = name   
                        ttl_exc -= 1
                src = new_src
                if src == dst:
                    ttl_req = last_ttlreq + 1
                    last_ttlreq = ttl_req
            else:
                break


    dst = x
    lost = ''
    name_lost = ''

    while(src != dst and ttl_exc > 0): 
        new_src = ''
        ip_lost = ''
        if ttl_rep > 0:
            info = get_information(src, dst)
            ip_destiny = check_routertable(src, info[1])
            mac = check_arptable(src, dst)
            if mac != '':
                result += icmp_echo_reply(src, dst, ttl_rep) + '\n'
                ttl_rep -= 1
                if (ttl_rep <= 0):
                    info = get_information(dst, src)
                    ip_lost = info[0]
                    name_lost = dst
                    ttl_exc = 8
                new_src = dst
            elif mac == '' and ip_destiny == '':
                getway = get_getway(src)
                mac = check_arptable(src, getway[1])
                if mac != '':
                    result += icmp_echo_reply(src, getway[1], ttl_rep) + '\n'
                    ttl_rep -= 1
                    if (ttl_rep <= 0):
                        info = get_information(getway[1], src)
                        ip_lost = info[0]
                        name_lost = getway[1]
                        ttl_exc = 8
                    new_src = getway[1]
                else:
                    getway = get_getway(src)
                    name = getway[1]
                    info = get_information(src, name)
                    ip_src = info[0]
                    ip_dst = info[1]
                    mac_dst = info[2]
                    result += arp_request(src, ip_dst, ip_src) + '\n'
                    update_arptable(name, ip_src, info[3])
                    result += arp_reply(name, src, ip_dst, mac_dst) + '\n'
                    update_arptable(src, ip_dst, mac_dst)
                    result += icmp_echo_reply(src,name, ttl_rep) + '\n'
                    ttl_rep -= 1
                    if (ttl_rep <= 0):
                        info = get_information(getway[1], src)
                        ip_lost = info[0]
                        name_lost = getway[1]
                        ttl_exc = 8
                    new_src = name
            elif ip_destiny != '':
                name = getnamewithip(ip_destiny)
                result += icmp_echo_reply(src, name, ttl_rep) + '\n'
                ttl_rep -= 1
                if (ttl_rep <= 0):
                    info = get_information(name, src)
                    ip_lost = info[0]
                    name_lost = name
                    ttl_exc = 8
                new_src = name
            src = new_src
            lost = ip_lost
            if ttl_rep <=0:
                src = name_lost
        else:
            if ttl_exc > 0:
                dst = y
                info = get_information(src, dst)
                ip_destiny = check_routertable(src, info[1])
                mac = check_arptable(src, dst)
                new_src = ''
                if mac != '':
                    result += icmp_echo_time_exceeded(src, dst, lost, y, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = dst
                elif mac == '' and ip_destiny == '':
                    getway = get_getway(src)
                    mac = check_arptable(src, getway[1])
                    if mac != '':
                        result += icmp_echo_time_exceeded(src, getway[1], lost, y, ttl_exc) + '\n'
                        ttl_exc -= 1
                        new_src = getway[1]
                elif ip_destiny != '':
                    name = getnamewithip(ip_destiny)
                    result += icmp_echo_time_exceeded(src, name, lost, y, ttl_exc) + '\n'
                    ttl_exc -= 1
                    new_src = name
                src = new_src
            else:
                break

    return result

if command == "ping":
    result = ping(source, destiny)
elif command == "traceroute":
    result = traceroute(source, destiny)
print(result)
