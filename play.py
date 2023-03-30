from helpers.game import Game
from helpers.visualGame import VisualGame
from helpers.player import Player, AIPlayer
from helpers.graph import Graph

import random

def play_game_terminal(game: Game):
    print("------------- New Game starts -------------")
    print("Player 0 goal is to go to nodes: ", game.V0)
    print("Player 1 goal is to go to nodes: ", game.V1)
    print("We start from node", game.s)

    res = game.start()
    print(game.result(res))

def play_game_visual(game : VisualGame):
    game.start()

def create_graph(filename, N):

    f = open(filename, 'w')
    f.write(str(N) + '\n')

    for i in range(N):
        temps = ""
        for j in range(N):
            temps += " "
            if i == j or random.random() < 0.7:
                temps += '0'
            else: 
                temps += str(random.randint(-1, 1))
        f.write(temps + '\n')
    


def load_graph(filename):

    with open(filename) as f:

        N = int(f.readline())
        E = list()
        i = 0
        for line in f:
            templine = list()
            templine = [int(x) for x in line.split()]
            for j in range(N):
                if templine[j] == 1:
                    E.append([i, j])
                if templine[j] == -1:
                    E.append([j, i])
            i += 1
                
        V0 = random.choices(range(N), k=2)
        V1 = random.choices(list(set(range(N)) - set(V0)), k= 2)
        
    return [N, E, V0, V1] 

def chooseStartingNode(V0, V1, N):
    taken = set(V0).union(set(V1))

    all = set(range(N))

    availiable = all - taken
    choice = random.choice(list(availiable))

    return choice


if __name__ == "__main__":

    #Initialize the graph
    filename = 'graphs/Adj_mat_2.txt'

    create_graph(filename, 20)

    [N, E, V0, V1]  = load_graph('graphs/Adj_mat_1.txt')
    
    G = Graph(N, E)
    s = chooseStartingNode(V0, V1, N)
    
    G.findneighs()

    #strategy = solve_game(G, V0, V1)
    players = [Player(0), AIPlayer(1)]
    
    #this is the game object Visual game to play with graphics, game to play in terminal
    game = VisualGame(s, V0, V1, G, players, node_height=30, node_width=30)
    #game = Game(s, V0, V1, G, players)

    print(players[1].strategy)
    
    #call the appropriate function to play a visual or terminal game
    play_game_visual(game)
    #play_game_terminal(game)

    