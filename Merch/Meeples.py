from Merch.Merch import Merch


class ZedMeeples(Merch):

    def __init__(self):
        self.name = "Zed Meeples"
        self.cost = 10
        self.query_str = 'ZED MEEPLES'
        super().__init__(self.name, self.cost, self.query_str)


