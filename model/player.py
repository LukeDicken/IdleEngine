

class Player:
    def __init__(self):
        self.name = ""
        self.wallet = {} #actual wallet dict
        self.visibleWallet = []  # list of wallet keys that are visible this frame
        self.visibleActions = []
        self.enabledActions = {}
        self.counters = {}

    def log_counter(self, counter):
        # counters are strictly increasing
        # counters are not pre-defined
        # anything can be a counter, any counter name can be checked
        if counter in self.counters:
            self.counters[counter] += 1
        else:
            self.counters[counter] = 1

    def get_counter(self, counter):
        try:
            return self.counters[counter]
        except KeyError:
            return 0

    @staticmethod
    def new_player_setup(game):
        # creation of a new player
        # static for when we want to un-pickle a player
        p = Player()
        for currency in game.currencies:
            p.wallet[currency] = game.currencies[currency].initial
        return p

    def check_wallet_visibility(self, game):
        # which resources are currently visible to the player?
        # bit of a cludgey hack that the flask template has limited code eval opportunity - needs stuff in lookups
        self.visibleWallet = []
        for currency in self.wallet:
            if self.is_currency_visible(game, currency):
                self.visibleWallet.append(currency)

    def is_currency_visible(self, game, currencyName):
        # check on visibility of a specific currency in the current context
        cur = game.currencies[currencyName]
        # TODO - also check counters
        for cond in cur.visCond:
            if cond['locktype'] == 'counter':
                count = self.get_counter(cond['id'])
                required = cond['amount']
                if count < required:
                    return False
            else:
                raise ValueError("Locktypes other than counter are not currently supported - in " + cond)
        return True

    def check_action_visibility(self, game):
        # action visibility - which buttons are shown?
        self.visibleActions = []
        for action in game.actions:
            if self.is_action_visible(game, action):
                self.visibleActions.append(action)

    def is_action_visible(self, game, action):
        # check for a specific button
        act = game.actions[action]
        for cond in act.visCond:
            if cond['locktype'] == 'counter':
                count = self.get_counter(cond['id'])
                required = cond['amount']
                if count < required:
                    return False
            else:
                raise ValueError("Locktypes other than counter are not currently supported - in " + cond)
        return True

    def check_action_enabled(self, game):
        # are actions enabled or disabled?
        self.enabledActions = {}
        for action in game.actions:
            self.enabledActions[action] = self.is_action_enabled(game, action)

    def is_action_enabled(self, game, action):
        # is this specific action enabled?
        act = game.actions[action]
        for cost in act.costs:
            if self.wallet[cost] < act.costs[cost]:
                return "disabled" # dirty - feed fwd to HTML
        return ""

    def player_tick(self, game):
        # called at the start of viewing a player
        # set up anything that might have changes that the template will need to access
        self.check_wallet_visibility(game)
        self.check_action_visibility(game)
        self.check_action_enabled(game)
