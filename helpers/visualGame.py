
from helpers.game import Game
import tkinter as tk
import networkx as nx
import time
import queue

root = tk.Tk()
canvas = tk.Canvas(root)
label =tk.Label(root, text="")

SHORTWAIT = 0.8
LONGWAIT = 1.8

class VisualGame(Game):
    def __init__(self, s: int, V0: int, V1: int, graph, players, W = 1000, H = 500, node_width = 30, node_height = 25):
        super().__init__(s, V0, V1, graph, players)

        canvas.configure(width=W, height=H)

        # Create the canvas and add it to the window
        canvas.pack()

        self.startingNode = s

        self.node_width = node_width
        self.node_height = node_height
        self.W = W
        self.H = H

        self.activePlayer = False

        self.node_ids = dict()

        self.drawGraph()

        # Bind the click event to the node labels
        for node_id, label_id in self.node_ids.values():
            canvas.tag_bind(node_id, "<Button-1>", self.clickHandler)
            canvas.tag_bind(label_id, "<Button-1>", self.clickHandler)


        #Colors
        self.colors = [{"main" : "white", "current" : "green", "near" : "light green"}] * len(self.graph.V)
        for v0 in self.V0:
            self.colors[v0] = {"main" : "cyan", "current" : "purple", "near" : "light blue"}
        for v1 in self.V1:
            self.colors[v1] = {"main" : "salmon", "current" : "purple", "near" : "pink"}

        #Text
        root.title("Graph Game")

        self.colorGraph()

        # Create a label widget with some text
        txt = "New Game!!\n Player 0 has to go to nodes " + str(self.V0) + "to win.\n" + "Player 1 has to go to nodes " + str(self.V1) + " to win.\n" + "Currently at node " + str(self.s) +  "\nPlayer " + str(self.turn) + "\'s turn to move."

        label.config(text = txt)

        # Add the label to the window
        label.pack()

        #add restart button
        self.restart_button = tk.Button(root, text="Restart", command=self.restart)
        


    def control(self):
        txt = self.get_state()
        end = False
        if self.s in self.V0:
                txt = self.result(0)
                end = True
        elif self.s in self.V1:
                txt = self.result(10)
                end = True
        elif self.graph.V[self.s].isterminal:
                txt = self.result(5)
                end = True
        
        self.showText(txt)
        self.colorGraph()
        canvas.update()

        if not end:
            text = self.players[self.turn].play_graphics()
            if text != None:
                self.turn = (self.turn + 1 ) % 2
                self.round += 1
                time.sleep(LONGWAIT)
                self.showText(text)
                time.sleep(SHORTWAIT)
                self.control()

    def start(self, showStrategy = True):
        
        if showStrategy:
            for p in self.players:
                if p.type == "AI":
                    self.interactiveStrategy()
                    break
        self.restart_button.pack()
        self.restart_button.config(text = "Restart")
        canvas.update()
        self.control()
        root.mainloop()
        
            
    
    def drawGraph(self, scale = 0.8):
        # Define the size of each node

        GR = nx.DiGraph()
        GR.add_edges_from([(e.start.id, e.end.id) for e in self.graph.E])

        # Calculate the node positions using the spring layout algorithm
        pos = nx.spectral_layout(GR)

        m = min([ num for v in pos.values() for num in v])

        if m < 0:
            for i in range(len(pos)):
                for j in range(2):
                    pos[i][j] -= m

        M = max([ num for v in pos.values() for num in v])

        if M > 1:
            for i in range(len(pos)):
                for j in range(2):
                    pos[i][j] /= M

        for i in range(len(pos)):
                for j in range(2):
                    pos[i][j] *= scale
        
        # Draw the edges on the canvas
        for edge in GR.edges():
            dx = pos[edge[0]][0] - pos[edge[1]][0]
            dy = pos[edge[0]][1] - pos[edge[1]][1]
            length = (dx**2 + dy**2)**0.5

            # Shorten the vector by a fraction
            shorten_factor = 0.5  # adjust this value as needed
            dx *= (1 - shorten_factor) * self.node_width / length
            dy *= (1 - shorten_factor) * self.node_height / length

            canvas.create_line(
                pos[edge[0]][0] * self.W + self.node_width * 1.5,
                pos[edge[0]][1] * self.H + self.node_height * 1.5,
                
                pos[edge[1]][0] * self.W + self.node_width * 1.5 + dx,
                pos[edge[1]][1] * self.H + self.node_height * 1.5 + dy,
                arrow=tk.LAST
            )

        # Draw the nodes on the canvas
        for node in GR.nodes():
            if node in self.V0:
                node_id = canvas.create_rectangle(
                    pos[node][0] * self.W + self.node_width,
                    pos[node][1] * self.H + self.node_height,
                    pos[node][0] * self.W + self.node_width * 2,
                    pos[node][1] * self.H + self.node_height * 2,
                    fill="salmon",
                )
            elif node in self.V1:
                node_id = canvas.create_rectangle(
                    pos[node][0] * self.W + self.node_width,
                    pos[node][1] * self.H + self.node_height,
                    pos[node][0] * self.W + self.node_width * 2,
                    pos[node][1] * self.H + self.node_height * 2,
                    fill="cyan",
                )
            elif node == self.s:
                node_id = canvas.create_oval(
                    pos[node][0] * self.W + self.node_width,
                    pos[node][1] * self.H + self.node_height,
                    pos[node][0] * self.W + self.node_width * 2,
                    pos[node][1] * self.H + self.node_height * 2,
                    fill="green",

                )
            else:
                node_id = canvas.create_oval(
                    pos[node][0] * self.W + self.node_width,
                    pos[node][1] * self.H + self.node_height,
                    pos[node][0] * self.W + self.node_width * 2,
                    pos[node][1] * self.H + self.node_height * 2,
                    fill="white",

                )
            # Add a tag to the oval
            canvas.itemconfig(node_id, tags=("node", str(node)))

            label_id = canvas.create_text(
                pos[node][0] * self.W + self.node_width * 1.5,
                pos[node][1] * self.H + self.node_height * 1.5 ,
                text="0, 0",
                font=("Arial", 10, 'bold'),
                fill="black"
            )

            # Add a tag to the text
            canvas.itemconfig(label_id,tags=("text", str(node)))

            self.node_ids[node] = [node_id, label_id]

    def colorGraph(self):
        neighs = [n.id for n in self.graph.V[self.s].outneighs]
        for node in self.graph.V:
            idx = node.id
            if idx == self.s:
                state = "current"
            elif idx in neighs:
                state = "near"
            else:
                state = "main"
            canvas.itemconfig(self.node_ids[idx][0], fill=self.colors[idx][state])

    def showText(self, p):
        label.config(text = p)
        canvas.update()

    def clickHandler(self, event):
        if self.activePlayer:
            clicked_id = event.widget.find_withtag(tk.CURRENT)[0]
            
            # Check if the clicked object is the text or the oval
            tags = event.widget.gettags(clicked_id)

            if "text" in tags:
                # If the text was clicked, get the ID of the associated oval
                node_idOnCanvas = clicked_id - 1
            else:
                # Otherwise, assume the oval was clicked
                node_idOnCanvas = clicked_id

            node_id = [k for k, v in self.node_ids.items() if v[0] == node_idOnCanvas][0]

            if node_id in [n.id for n in self.graph.V[self.s].outneighs]:
                self.s = node_id
                self.activePlayer = False
                self.round += 1
                self.turn = (self.turn + 1) % 2
                self.showText("Player " + str(self.turn) + " chose node " + str(self.s))
                time.sleep(SHORTWAIT)
                self.control()
            else:
                self.showText("Please choose a valid move")
            
        

    def restart(self):
        self.s = self.startingNode
        self.turn = 0
        self.round = 1
        self.control()
            
    def interactiveStrategy(self):
        
        Qupdate = queue.Queue()
        self.restart_button.config(text = "Start Game")
        self.showText("Initializing the score for the terminal nodes V0, V1\n")
        for node in self.graph.V:
            node.min = 0
            node.max = 0
            if node.belongsInV0:
                node.min = 1
                node.max = -1
                canvas.itemconfig(self.node_ids[node.id][1], text = "1, -1")
                for pred in node.inneighs:
                    if not pred.belongsInV0 and not pred.belongsInV1:
                        Qupdate.put(pred)
                time.sleep(1)
                canvas.update()

            elif node.belongsInV1:
                node.min = -1
                node.max = 1
                canvas.itemconfig(self.node_ids[node.id][1], text = "-1, 1")
                for pred in node.inneighs:
                    if not pred.belongsInV0 and not pred.belongsInV1:
                        Qupdate.put(pred)

                time.sleep(1)
                canvas.update()

        self.showText("End of initialization for the terminal nodes V0, V1\n")

        while not Qupdate.empty():
            
            time.sleep(1)
            self.showText("Queue = " + str([n.id for n in Qupdate.queue]))
        
            cur_node = Qupdate.get()
            self.s = cur_node.id
            time.sleep(1)
            self.colorGraph()
            self.showText("Currently updating score for node: " + str(cur_node.id))


            min_val = 2
            max_val = 2

            for child in cur_node.outneighs:
                if child.max < min_val:
                    min_val = child.max
                if child.min < max_val:
                    max_val = child.min

            if cur_node.min != -min_val or cur_node.max != -max_val:
                
                self.graph.V[cur_node.id].min = -min_val
                self.graph.V[cur_node.id].max = -max_val
                
                time.sleep(1)
                canvas.itemconfig(self.node_ids[cur_node.id][1], text = str(-min_val) + ", " + str(-max_val))
                self.showText("Score updated for node: " + str(cur_node.id))


                for pred in cur_node.inneighs:
                    if not (pred.belongsInV0 or pred.belongsInV1) and pred not in Qupdate.queue:
                        Qupdate.put(pred)

        self.s = self.initialNode