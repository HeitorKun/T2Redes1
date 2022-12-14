
#192.168.0.2
class IP:
    def __init__(self, ipStr: str, maskStr: str ):
        self.ipStr = ipStr
        self.maskStr = maskStr
        self.maskInt = int(self.maskStr)
        splitPointIPStr = self.ipStr.split(".")
        
        self.redeIPInBinaryStr = ""
        for ip in splitPointIPStr:
            self.redeIPInBinaryStr += bin(int(ip)).replace("0b", "").zfill(8)
        self.redeIPInBinaryStr = self.redeIPInBinaryStr[:self.maskInt]

        def __eq__(self, other):
            if not isinstance(other, IP):
                return False

            return self.ipStr == other.ipStr