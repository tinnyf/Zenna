from Merch.Merch import Merch


class DiceTower(Merch):

    def __init__(self):
        self.name = "Zatu Dice Tower"
        self.cost = 30
        self.query_str = 'DICE TOWER'
        super().__init__(self.name, self.cost, self.query_str)


    