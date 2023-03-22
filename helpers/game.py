from helpers.graph import Graph
from helpers.player import Player

class Game:

    def __init__(self, s : int, V0 : int, V1 : int, graph : Graph, players: list[Player]):
        self.initialNode = s
        self.s = s
        self.V0 = V0
        self.V1 = V1
        self.graph = graph
        self.round = 1
        self.turn = 0
        self.players = players
        
        for p in self.players:
            p.game = self
        
    def start(self):
        self.graph.findneighs()
        while True:
            if self.s in self.V0:
                return 0
            if self.s in self.V1:
                return 10
            if self.graph.V[self.s].isterminal:
                return 5
            print(self.get_state())

            self.players[self.turn].play() 
        
            self.round += 1
            self.turn = (self.turn + 1) % 2

    def get_state(self):
        
        text = "----------- Round " + str(self.round) + " -------------------\nPlayer " + str(self.turn) + \
        "\'s turn to play!\nCurrently at node " + str(self.s)
        
        return text

    def result(self, res : int):
        results = {0 : "Player 0 wins!", 5 : "Draw!", 10 : "Player 1 wins!"}

        text = "--------------- End of game! ---------------------\nResult: " + results[res] + "\n"
        return text

        

