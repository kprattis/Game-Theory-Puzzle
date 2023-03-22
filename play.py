from helpers.game import Game
from helpers.visualGame import VisualGame
from helpers.player import *
from helpers.graph import Graph

def play_game_terminal(game: Game):
    print("------------- New Game starts -------------")
    print("Player 0 goal is to go to nodes: ", game.V0)
    print("Player 1 goal is to go to nodes: ", game.V1)
    print("We start from node", game.s)

    res = game.start()
    print(game.result(res))

def play_game_visual(game : VisualGame):
    game.start()

if __name__ == "__main__":

    #Initialize the graph
    N = 7
    E = [[2, 0], [3, 1], [3, 2], [2, 4], [5, 3], [6, 5], [4, 5]]
    G = Graph(N, E)

    V0 = [0]
    V1 = [1]
    s = 6

    G.findneighs()

    #strategy = solve_game(G, V0, V1)
    players = [Player(0), AIPlayer(1)]

    #this is the game object
    game = VisualGame(s, V0, V1, G, players)

    play_game_visual(game)

    