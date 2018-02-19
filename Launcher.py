from flask import Flask, render_template, request
from model.game import Game
import thread

app = Flask(__name__)
global game

@app.route("/game/<username>/act/<action>/")
def do_action(username, action):
    global game
    player = game.fetch_player(username)
    game.execute(action, player) # this is going to return False if it fails or True if not - TODO: Handle
    return show_main_ui(username)

@app.route("/game/<username>/automate/<automation>/")
def add_automation(username, automation):
    global game
    player = game.fetch_player(username)
    game.add_automation(automation, player)
    return show_main_ui(username)



@app.route("/login/", methods=['POST'])
def login():
    global game
    username = request.form['name']
    return show_main_ui(username)



@app.route("/game/<username>/")
def show_main_ui(username):
    #player += 1
    # retrieve player name from gamestate -- TODO make this properly session/passwordy
    global game
    player = game.fetch_player(username) # separate out fetch and create.
    player.player_checks(game)
    return render_template('game_ui.html', player=player, game=game)


@app.route("/")
def show_landing():
    return render_template('landing_page.html')


if __name__=="__main__":
    global game
    game = Game()
    game.load_content()
    thread.start_new_thread(game.gamemanager_tick, ())
    # this is almost certainly not thread-safe. ...probably only matters at scale?
    app.run(host='0.0.0.0')