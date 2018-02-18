

class Action:
    def __init__(self, id, label, description, costs, outputs, visibleCond=None, activeCond=None): # TODO wire up the conditionals
        self.id = id
        self.label = label
        self.description = description
        self.costs = costs
        self.outputs = outputs
        self.visCond = visibleCond
        pass

    @staticmethod
    def parse_action(jsonBlob):
        id = jsonBlob["gid"]
        label = jsonBlob["components"]["ui"]["label"]
        description = jsonBlob["components"]["ui"]["description"]
        cost = {}
        try:
            for line in jsonBlob["components"]["cost"]:
                cost[line["id"]] = line["amount"]
        except:
            cost = {}
        output = {}
        try:
            for line in jsonBlob["components"]["output"]:
                output[line["id"]] = line["amount"]
        except:
            output = {}
        visCond = []
        try:
            visCond = jsonBlob["components"]["lockout"]["visible"]
        except:
            pass

        return Action(id=id, label=label, description=description, costs=cost, outputs=output, visibleCond=visCond)