

class Player:
    def __init__(self):
        self.name = ""
        self.wallet = {} #actual wallet dict
        self.visibleWallet = []  # list of wallet keys that are visible this frame
        self.visibleActions = []
        self.enabledActions = {}
        self.counters = {}

    def log_counter(self, counter):
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
        p = Player()
        for currency in game.currencies:
            p.wallet[currency] = game.currencies[currency].initial
        return p

    def check_wallet_visibility(self, game):
        self.visibleWallet = []
        for currency in self.wallet:
            if self.is_currency_visible(game, currency):
                self.visibleWallet.append(currency)

    def is_currency_visible(self, game, currencyName):
        # check on visibility in the current context
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
        self.visibleActions = []
        for action in game.actions:
            if self.is_action_visible(game, action):
                self.visibleActions.append(action)

    def is_action_visible(self, game, action):
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
        self.enabledActions = {}
        for action in game.actions:
            self.enabledActions[action] = self.is_action_enabled(game, action)

    def is_action_enabled(self, game, action):
        act = game.actions[action]
        for cost in act.costs:
            if self.wallet[cost] < act.costs[cost]:
                return "disabled" # dirty - feed fwd to HTML
        return ""

    def player_tick(self, game):
        # called at the start of viewing a player
        # set up anything that might have changes that the template will need to access to
        self.check_wallet_visibility(game)
        self.check_action_visibility(game)
        self.check_action_enabled(game)
