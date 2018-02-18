from flask import Flask, render_template
from model.game import Game

app = Flask(__name__)
global game

@app.route("/game/<username>/act/<action>/")
def do_action(username, action):
    global game
    player = game.fetch_player(username)
    game.execute(action, player) # this is going to return False if it fails or True if not - TODO: Handle
    return show_main_ui(username)


@app.route("/game/<username>")
def show_main_ui(username):
    #player += 1
    # retrieve player name from gamestate -- TODO make this properly session/passwordy
    global game
    player = game.fetch_player(username)
    player.player_tick(game)
    return render_template('game_ui.html', player=player, game=game)


@app.route("/")
def show_landing():
    return render_template('landing_page.html')


if __name__=="__main__":
    global game
    game = Game()
    game.load_content()
    # for c in game.currencies:
    #     print c.name
    # print game.actions
    app.run(host='0.0.0.0')