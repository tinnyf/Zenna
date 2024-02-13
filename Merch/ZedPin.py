from Merch.Merch import Merch


class ZedPin(Merch):

    def __init__(self):
        self.name = "Zed Pin"
        self.cost = 10
        self.query_str = 'ZED PIN'
        super().__init__(self.name, self.cost, self.query_str)


    