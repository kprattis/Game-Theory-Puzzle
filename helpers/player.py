import random
import time

class Player:
    def __init__(self, id, game = None):
        self.id = id
        self.game = game

    def play(self):
        N = len(self.game.graph.V)
        move = -1
        validMoves = [o.id for o in self.game.graph.V[self.game.s].outneighs]

        while move not in range(0, N) or move not in validMoves:
            move = int(input("Choose next move, valid moves: " + str(validMoves) + "\n"  ) )

        self.game.s = move
        print("Player " + str(self.id) + " chose node " + str(self.game.s))

    def play_graphics(self):
        self.game.activePlayer = True
        return None

class AIPlayer(Player):
    def __init__(self, id, strategy = None, game = None):
        super().__init__(id, game)
        self.strategy = strategy

    def play(self):
        if self.strategy == None:
            move = random.choice([o.id for o in self.game.graph.V[self.game.s].outneighs])
        else:
            move = self.strategy[self.game.s]
        
        self.game.s = move
        print("Player " + str(self.id) + " chose node " + str(self.game.s))

    def play_graphics(self):
        if self.strategy == None:
            move = random.choice([o.id for o in self.game.graph.V[self.game.s].outneighs])
        else:
            move = self.strategy[self.game.s]
        
        self.game.s = move
        return "Player " + str(self.id) + " chose node " + str(self.game.s)