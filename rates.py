from clients import CMKTClient, SatoshiClient, PaxfulClient

class Route:
    def __init__(self, steps=[]):
        self.path = steps[:]

    def add_step(self, node):
        self.path.append(node)

    def __str__(self):
        node_names = [node.name for node in self.path]
        return ' => '.join(node_names)

    def calc_out(self, inpt):
        prev = inpt
        for node in self.path:
            prev = node.calc_out(prev)
        return prev

    def calc_rate(self, inpt):
        out = self.calc_out(inpt)
        rate = out/inpt
        return rate

    def analyze(self):
        print(self)
        inputs = [100]
        for i in inputs:
            rate = self.calc_rate(i)
            print(f'para {i} usd queda a un rate de {rate}')
        print()

class Node:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Banxa(Node):
    def __init__(self):
        super().__init__('Banxa')

    def calc_out(self, inpt):
        btc = 0.0000808690
        return btc*inpt*0.98

class CryptoMkt(Node):
    def __init__(self):
        super().__init__('CryptoMkt')
        self.client = CMKTClient()

    def calc_out(self, inpt):
        cotizacion = self.client.get_price()
        retiro =  0.009 + 0.0068
        return inpt*cotizacion*(1-retiro)

class Satoshi(Node):
    def __init__(self):
        super().__init__('Satoshi')

    def calc_out(self, inpt):
        coti = 1427824.91
        return inpt*coti*(1-0.01)

class Paxful(Node):
    def __init__(self):
        super().__init__('Paxful')
        self.client = PaxfulClient()

    def calc_out(self, inpt):
        cotizacion_btc = self.client.get_price()
        return inpt / cotizacion_btc


banxa = Banxa()
mkt = CryptoMkt()
satoshi = Satoshi()
paxful = Paxful()

routes = [
    Route([banxa, mkt]),
    Route([banxa, satoshi]),
    # Route([crypto, mkt]),
    # Route([crypto, satoshi]),
    Route([paxful, mkt]),
    Route([paxful, satoshi]),
]

for route in routes:
    route.analyze()
