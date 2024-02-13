from Merch.Merch import Merch


class Dice(Merch):

    def __init__(self):
        self.name = "Zatu Dice"
        self.cost = 10
        self.query_str = 'ZATU DICE'
        super().__init__(self.name, self.cost, self.query_str)


    