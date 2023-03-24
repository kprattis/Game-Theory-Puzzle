import random
import time
import queue
from helpers.graph import Node, Graph

class Player:
    def __init__(self, id, game = None):
        self.id = id
        self.game = game
        self.type = 'Random'

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
    def __init__(self, id, game = None, strategy= None):
        super().__init__(id, game)
        self.strategy = strategy
        self.type = 'AI'

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
    
    def compute_strategy(self):
        strategy = [None]*len(self.game.graph.V)
        Qupdate = queue.Queue()

        for node in self.game.graph.V:
            if node.belongsInV0:
                node.min = 1
                node.max = -1
                for pred in node.inneighs:
                    if not pred.belongsInV0 and not pred.belongsInV1:
                        Qupdate.put(pred)
            elif node.belongsInV1:
                node.min = -1
                node.max = 1
                for pred in node.inneighs:
                    if not pred.belongsInV0 and not pred.belongsInV1:
                        Qupdate.put(pred)


        while not Qupdate.empty():
            cur_node = Qupdate.get()
            min_val = 2
            max_val = 2

            for child in cur_node.outneighs:
                if child.max < min_val:
                    min_val = child.max
                if child.min < max_val:
                    max_val = child.min

            

            if cur_node.min != -min_val or cur_node.max != -max_val:
                self.game.graph.V[cur_node.id].min = -min_val
                self.game.graph.V[cur_node.id].max = -max_val
            
                for pred in cur_node.inneighs:
                    if not (pred.belongsInV0 or pred.belongsInV1) and pred not in Qupdate.queue:
                        Qupdate.put(pred)
   

        
        for node in self.game.graph.V:
            best_score = -2
            best = -1

            worst_score = -2
            worst = -1

            for neigh in node.outneighs:
                if neigh.min > best_score:
                    best_score = neigh.min
                    best = neigh.id
                if neigh.max > worst_score:
                    worst_score = neigh.max
                    worst = neigh.id
            strategy[node.id] = [best, worst]

            print(node.id, best_score, worst_score)

        self.strategy = strategy
        return strategy