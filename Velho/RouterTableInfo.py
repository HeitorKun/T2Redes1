class RouterTableInfo:
  def __init__(self, net_dest, prefix, nexthop, port):
    self.net_dest = net_dest
    self.prefix = prefix
    self.nexthop = nexthop
    self.port = port