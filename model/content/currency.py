

class Currency:

    def __init__(self, name, description, min, max, initial, visCond=[]):
        self.name = name
        self.description = description
        self.min = min
        self.max = max
        self.initial = initial
        self.visCond = visCond




    @staticmethod
    def parse_currency(json):
        name = json["components"]["ui"]["name"]
        description = json["components"]["ui"]["description"]
        initial = json["components"]["wallet"]["initialvalue"]
        min = json["components"]["wallet"]["minvalue"]
        max = json["components"]["wallet"]["maxvalue"]
        visCond = []
        try:
            visCond = json["components"]["lockout"]["visible"]
        except:
            pass
        return Currency(name, description, min, max, initial, visCond)
