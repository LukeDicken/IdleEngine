import os
from utility.json_byteify import json_load_byteified
import content
from player import Player


class Game:

    def __init__(self):
        self.ids = []
        self.currencies = {}
        self.actions = {}
        self.players = {}

    def load_content(self):
        # open all json files
        for root, dirs, files in os.walk('data'):
            for file in files:
                if ".json" in file:
                    with open(os.path.join(root, file), "r") as f:
                        jsonBlob = json_load_byteified(f)
                        if "type" not in jsonBlob:
                            raise ValueError("No type definition for " + file)
                        type = jsonBlob["type"]
                        gid = jsonBlob["gid"]
                        if gid in self.ids:
                            raise ValueError("An entity with this GID already exists: " + gid + " - duplicate found in: " + file)
                        if type == "action":
                            self.actions[gid] = (content.Action.parse_action(jsonBlob))
                            self.ids.append(gid)
                        elif type == "currency":
                            self.currencies[gid] = (content.Currency.parse_currency(jsonBlob))
                            self.ids.append(gid)
                        else:
                            raise ValueError(type + " is not a supported content type in " + file)

    def fetch_player(self, name):
        try:
            # get the player if it exists
            player = self.players[name]
        except KeyError:
            # if it doesn't exist, make it from the template
            self.players[name] = Player.new_player_setup(self)
            self.players[name].name = name
            player = self.players[name]
        return player

    def lookup_by_gid(self, gid):
        if gid not in self.currencies and gid not in self.actions:
            return None
        else:
            try:
                return self.actions[gid]
            except:
                return self.currencies[gid]

    def execute(self, actionName, player):
        # check that the player has the cost
        # deduct the cost from player wallet
        # add the output to player wallet
        action = self.actions[actionName]
        try:
            for cost in action.costs:
                if player.wallet[cost] < action.costs[cost]:
                    raise ValueError("Player does not have enough in their wallet for " + actionName)
        except ValueError, ve:
            print ve.message
            return False
        for cost in action.costs:
            player.wallet[cost] -= action.costs[cost]
        for reward in action.outputs:
            player.wallet[reward] += action.outputs[reward]
        player.log_counter(actionName)
        return True
