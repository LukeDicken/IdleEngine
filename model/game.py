import os
# noinspection PyUnresolvedReferences
from utility.json_byteify import json_load_byteified
import content
from player import Player
import time


class Game:

    def __init__(self):
        self.ids = []
        self.currencies = {}
        self.actions = {}
        self.automations = {}
        self.players = {}
        self.debug = True # toggles some additional output

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
                        elif type == "automation":
                            self.automations[gid] = content.Automation.parse_automation(jsonBlob)
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
        player.execute(actionName, self)

    def add_automation(self, automationName, player):
        player.add_automation(automationName, self)

    def gamemanager_tick(self):
        while(True):
            print("Tick")
            for player in self.players:
                self.players[player].automatic_execute(self)
            time.sleep(1) # simulator speed is 1s (+overhead). All times multiples of 1s