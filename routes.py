import json
import requests
from flask import Flask, redirect, url_for, request, render_template
from .game_state import Game, all_games

app = Flask(__name__)


# list all games
@app.route('/')
@app.route('/games')
def games():
    return render_template('games.html', games=all_games)


# start new game
@app.route('/games/', methods=['POST'])
def new_game():
    game_rules = request.form
    new_deck_json = requests.get(
        'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={}'
            .format(game_rules['deck_count'])
    ).text
    new_deck = json.loads(new_deck_json)

    # make new game and add it to the all_games store
    game_name = game_rules['game_name']
    game = Game(game_name, new_deck['deck_id'])
    if game_name not in all_games:
        all_games[game_name] = game

    msg = 'Game {} has been created!'.format(game_rules['game_name'])
    return render_template('games.html', games=all_games, message=msg)


# go to game with game_name
@app.route('/games/<game_name>')
def show_game(game_name):
    game = all_games[game_name]
    return render_template('game.html', game=game)


# deal new hand
@app.route('/games/<game_name>/deal')
def deal(game_name):
    return 'Game name {}'.format(game_name)


# stand
@app.route('/games/<game_name>/stand')
def stand(game_name):
    return 'Game name {}'.format(game_name)


# hit
@app.route('/games/<game_name>/hit')
def hit(game_name):
    return 'Game name {}'.format(game_name)


# double
@app.route('/games/<game_name>/double')
def double(game_name):
    return 'Game name {}'.format(game_name)


# split
@app.route('/games/<game_name>/split')
def split(game_name):
    return 'Game name {}'.format(game_name)
