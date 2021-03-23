from app import app
from app.board import GameEngine
import logging
import random
from flask import render_template, request, redirect, url_for
from flask import g


# init, start the game engine and load the dictionary into memory
game = GameEngine()
the_dictionary = set()
with open("app/static/dictionary.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        the_dictionary.add(line.strip())
word_check = {"checked_word":None, "IsAWord":None}



## bonus points lookup 
bonus_lookup = {}
triple_word_tiles = [[0,0],[0,7],[0,14],[7,0],[7,14],[14,0],[14,7],[14,14]]
double_word_tiles = [[1,1],[1,13],[2,2],[2,12],[3,3],[3,11],[4,4],[4,10],[10,4],[10,10],[11,3],[11,11],[12,2],[12,12],[13,1],[13,13]]
double_letter_tiles = [[0,3],[0,11],[2,6],[2,8],[3,0],[3,7],[3,14],[6,2],[6,6],[6,8],[6,12],[7,3],[7,11],[8, 2],[8, 6],[8, 8],[8, 12],[11,1],[11,7],[11,14],[12,6],[12,8],[14,3],[14,11]]
triple_letter_tiles = [[1, 5],[1,9],[5,1],[5,5],[5,9],[5,13],[9,1],[9,5],[9,9],[9,13],[13,5],[13,9]]
center = [[7,7]]

for i in range(15):
    for j in range(15):
        if [i, j] in center:
            bonus_lookup[str(i) + '-' + str(j)] = '\u2605'
        elif [i, j] in triple_word_tiles:
              bonus_lookup[str(i) + '-' + str(j)] = 'TW'
        elif [i, j] in double_word_tiles:
              bonus_lookup[str(i) + '-' + str(j)] = 'DW'
        elif [i, j] in double_letter_tiles:
              bonus_lookup[str(i) + '-' + str(j)] = 'DL'
        elif [i, j] in triple_letter_tiles:
              bonus_lookup[str(i) + '-' + str(j)] = 'TL'
        else:
            bonus_lookup[str(i) + '-' + str(j)] = None







letter_points_lookup = {'E':1,'A':1,'I':1,'O':1, 'N': 1, 'R': 1, 'T':1,'L':1, 'S':1, 'U':1,
                    'D':2, 'G': 2, 'B':3, 'C':3, 'M':3, 'P':3, 'F':4, 'H':4, 'V':4, 'W':4, 'Y':4, 'K':5,
                    'J':8,'X': 8,'Q':10, 'Z':10, ' ':0}

app.logger.info("Rack 1 is " + str(game.rack1))
app.logger.info("Rack 2 is " + str(game.rack2))
app.logger.info("Bag is: " + str(game.bag))
app.logger.info("Elements left in bag is: " + str(game.tiles_left))


@app.route('/')
@app.route('/index')
def index():
    app.logger.info(str(word_check))
    
    return render_template('index.html', game=game, checked_word=word_check["checked_word"], IsAWord=word_check["IsAWord"], letter_points_lookup=letter_points_lookup, bonus_lookup=bonus_lookup)


@app.route('/reset')
def reset():
    game.reset()
    return redirect(url_for('index'))

@app.route('/replace')
def replace():
    rack = int(request.args.get('rack'))
    app.logger.info("Replacing rack {}".format(rack))
    game.replace_tiles(rack)
    return redirect(url_for('index'))

@app.route('/placetile', methods=['POST'])
def placetile():
    app.logger.info("Receiving post request")
    app.logger.info(str(request.headers))
    letter_to_place = request.json["letter"]
    square_id = request.json["squareid"]
    rack_class = request.json["rackclass"]
    app.logger.info("Placing letter: " + letter_to_place + " in " + square_id + " from rack position: " + rack_class)
    rack = int(rack_class.split(' ')[0].split(':')[1])
    rack_index = int(rack_class.split(' ')[1].split(':')[1])
    app.logger.info("Rack: {} Index: {}".format(rack, rack_index))
    app.logger.info("Calling remove_tie with rack={} and rack_index={}".format(rack, rack_index))
    app.logger.info("State of rack 1: " + str(game.rack1))
    app.logger.info("State of rack 2: " + str(game.rack2))

    game.remove_tile(rack, rack_index)

    app.logger.info("State of rack 1: " + str(game.rack1))
    app.logger.info("State of rack 2: " + str(game.rack2))


    split_square_id = square_id.split('[')
    row = int(split_square_id[1].replace(']',''))
    column = int(split_square_id[2].replace(']',''))
    if len(letter_to_place) > 1:
        raise ValueError("More than one letter has been provided")

    app.logger.info("Inserting " + letter_to_place + " at [" + str(row) + "][" + str(column)+"]")
    game.board.PlaceLetter(row, column, letter_to_place)
    return "Everything ok"


@app.route('/checkword', methods=['POST'])
def checkword():
    app.logger.info("checkword called")
    app.logger.info(str(request.headers))
    word_to_check = request.form.get("wordtocheck")
    app.logger.info("Checking word: " + word_to_check)
    word_check["checked_word"] = word_to_check
    if word_to_check.upper() in the_dictionary:
        word_check["IsAWord"] = True
        app.logger.info(word_to_check + " is a word")
        return redirect(url_for('index'))
    else: 
        word_check["IsAWord"] = False
        app.logger.info(word_to_check + " is not a word")
        return redirect(url_for('index'))