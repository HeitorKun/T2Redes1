class MAC:
    def __init__(self, macStr: str):
        self.macStr = macStr


    def __eq__(self, other):
        if not isinstance(other, MAC):
            return False

        return self.macStr == other.macStr