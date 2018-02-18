import os
# noinspection PyUnresolvedReferences
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
        for root, dirs, files in os.walk('IdleEngine/data'): #note that this is an issue with PyCharm. TODO - fix
            for file in files:
                if ".json" in file:
                    with open(os.path.join(root, file), "r") as f:
                        jsonBlob = json_load_byteified(f)
                        if "type" not in jsonBlob:
                            # no type defined - fail
                            raise ValueError("No type definition for " + file)
                        type = jsonBlob["type"]
                        gid = jsonBlob["gid"]
                        if gid in self.ids:
                            # enforce unique gids
                            raise ValueError("An entity with this GID already exists: " + gid + " - duplicate found in: " + file)
                        if type == "action":
                            # actions - things the player can do
                            self.actions[gid] = (content.Action.parse_action(jsonBlob))
                            self.ids.append(gid)
                        elif type == "currency":
                            # currencies - things the player collects
                            self.currencies[gid] = (content.Currency.parse_currency(jsonBlob))
                            self.ids.append(gid)
                        else:
                            # something else?
                            raise ValueError(type + " is not a supported content type in " + file)

    def fetch_player(self, name):
        # given a playername, find or create a player object for them
        # probably should be a bit more robust here
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
        # assume that there is a GID, find where it lives
        if gid not in self.currencies and gid not in self.actions:
            # fail out if it doesn't exist
            return None
        else:
            try:
                return self.actions[gid]
            except:
                return self.currencies[gid]

    def execute(self, actionName, player):
        # execute a specific action by a player
        action = self.actions[actionName]
        try:
            # check that the player has the cost
            for cost in action.costs:
                if player.wallet[cost] < action.costs[cost]:
                    raise ValueError("Player does not have enough in their wallet for " + actionName)
        except ValueError, ve:
            print ve.message
            return False
        for cost in action.costs:
            # deduct the cost from player wallet
            player.wallet[cost] -= action.costs[cost]
        for reward in action.outputs:
            # add the output to player wallet
            player.wallet[reward] += action.outputs[reward]
        player.log_counter(actionName)
        return True