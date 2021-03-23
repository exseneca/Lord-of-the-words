import random
import logging 
from app import app

class Tile:
    def __init__(self, bonus=None):
        self.bonus = bonus
        self.value = None
# we need a list or a way to work out the bonus tiles. 

class Board:
    def __init__(self):
        self.tiles = [[Tile() for c in range(15)] for r in range(15)]
# how to we represent this - maybe just row

            
    def GetBoardLayout(self):
        output_string = ""
        output_string+="* "*17
        output_string+='\n'  
        for row in self.tiles:
            row_string = [(tile.value or '-') for tile in row]
            output_string = output_string + "*" + ' '.join(row_string) + "*" + '\n' 
        return output_string +  "* "*17 + '\n'

    def PlaceLetter(self, row, column, letter):
        if len(letter) > 1:
            print("Please only use valid letter")
        self.tiles[row][column].value = letter

class GameEngine():
    def __init__(self):
        self.board = Board()
        self.rack1 = [None for i in range(7)]
        self.rack2 = [None for i in range(7)]
        self.bag = {'E':12,'A':9,'I':9,'O':8, 'N': 6, 'R': 6, 'T':6,'L':4, 'S':4, 'U':4,
                    'D':4, 'G': 3, 'B':2, 'C':2, 'M':2, 'P':2, 'F':2, 'H':2, 'V':2, 'W':2, 'Y':2, 'K':1,
                    'J':1,'X': 1,'Q':1, 'Z':1, ' ':2} # we need to add blanks at some point
        self.tiles_left = 100
        for i in range(7):
            self.add_letter_to(1,i)
            self.add_letter_to(2,i)

    def reset(self):
        self.__init__()

    def replace_tiles(self, racknumber):
        app.logger.info("State of rack 1: " + str(self.rack1))
        app.logger.info("State of rack 2: " + str(self.rack2))
        if racknumber not in [1,2]:
            raise ValueError("Rack number must be in [1,2], the rack number is {}".format(racknumber))
        if racknumber == 1:
            for i in range(7):
                if self.rack1[i] is None:
                    self.add_letter_to(1,i)
        else:
            for i in range(7):
                if self.rack2[i] is None:
                    self.add_letter_to(2,i)

        app.logger.info("State of rack 1: " + str(self.rack1))
        app.logger.info("State of rack 2: " + str(self.rack2))

       
    def remove_tile(self, racknumber, index):
        if racknumber not in [1, 2]:
            raise ValueError("Rack number must be in [1,2]")
        if racknumber == 1:
            self.rack1[index] = None
        else:
            self.rack2[index] = None

    def add_letter_to(self, racknumber, index):
        if racknumber not in [1,2]:
            raise ValueError("Rack number must be in [1,2]")
        if self.tiles_left == 0:
            raise ValueError("There are no tiles left in the bag")
    
# create a randomiser for the tiles. We need to pick 7 letters for each person. 
# for each element in 
        rand_number = random.randint(1, self.tiles_left)
        app.logger.info("We've picked the rand")
        letters = list(self.bag.keys())
        letter_sum = 0
        selected_letter = ""
        for letter in letters:
            letter_sum += self.bag[letter]
            if letter_sum > rand_number:
                selected_letter = letter
                break
        self.tiles_left-=1
        self.bag[selected_letter]-=1
        app.logger.info("Selected Letter: " + selected_letter)

        if racknumber == 1:
            self.rack1[index] = selected_letter
            app.logger.info("Updated rack 1: " + str(self.rack1))
        else:
            self.rack2[index] =selected_letter
            app.logger.info("Updated rack 2: " + str(self.rack2))


