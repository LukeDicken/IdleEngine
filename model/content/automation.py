
class Automation:
    def __init__(self, gid, label, description, costs, automation, visibleCond):
        self.id = gid
        self.label = label
        self.description = description
        self.costs = costs
        self.automation = automation
        self.visCond = visibleCond
        pass

    @staticmethod
    def parse_automation(jsonBlob):
        id = jsonBlob["gid"]
        label = jsonBlob["components"]["ui"]["label"]
        description = jsonBlob["components"]["ui"]["description"]
        cost = {}
        try:
            for line in jsonBlob["components"]["cost"]:
                cost[line["id"]] = line["amount"]
        except:
            cost = {}
        # output = {}
        # try:
        #     for line in jsonBlob["components"]["output"]:
        #         output[line["id"]] = line["amount"]
        # except:
        #     output = {}
        automation = []
        try:
            automation = jsonBlob["components"]["automation"]
        except:
            automation = []
        visCond = []
        try:
            visCond = jsonBlob["components"]["lockout"]["visible"]
        except:
            pass

        return Automation(gid=id, label=label, description=description, costs=cost, automation=automation, visibleCond=visCond)