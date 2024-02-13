from Merch.Merch import Merch


class CardsPin(Merch):

    def __init__(self):
        self.name = "Cards Pin"
        self.cost = 10
        self.query_str = 'CARDS PIN'
        super().__init__(self.name, self.cost, self.query_str)


    