from Merch.Merch import Merch


class DiceTray(Merch):

    def __init__(self):
        self.name = "Zatu Dice Tray"
        self.cost = 20
        self.query_str = 'DICE TRAY'
        super().__init__(self.name, self.cost, self.query_str)


