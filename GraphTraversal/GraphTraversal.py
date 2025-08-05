import tkinter as tk
from tkinter import ttk, font
from GraphTraversal.GraphDS import graphnode, graphedge
from GraphTraversal.GraphData import get_graph_and_edges
from queue import PriorityQueue

NODE_WIDTH = 20
TARGET_NODE = graphnode("H", 650, 350, NODE_WIDTH)

# Placed in seperate file to avoid visual clutter
Graph, Edges = get_graph_and_edges(TARGET_NODE, NODE_WIDTH)

def create_title_label(canvas:tk.Canvas, title:str):
    canvas.update_idletasks()
    titleFont = font.Font(family="Arial", size=20)
    lbl = tk.Label(canvas, text=title, font=titleFont)
    xVal = (canvas.winfo_width() - titleFont.measure(title)) * 0.5
    lbl.place(x=xVal, y=10)

def create_button_node(canvas:tk.Canvas, node:graphnode, AlgoType:str, backcolor="lightgray", forecolor="black"):
    button = tk.Button(canvas, text=node.name, background=backcolor, foreground=forecolor, command=lambda: PerformSearch(canvas, node, Graph, AlgoType))
    button.place(x=node.x, y=node.y, width=NODE_WIDTH, height=NODE_WIDTH)

def draw_labelled_edge(canvas:tk.Canvas, edge:graphedge, half_node_width:int, linecolor="black", labelbg="red", isThickLine=False) -> graphedge:
    fromX, fromY = edge.pointA.x + half_node_width, edge.pointA.y + half_node_width
    toX, toY = edge.pointB.x + half_node_width, edge.pointB.y + half_node_width
    if isThickLine:
        canvas.create_line(fromX, fromY, toX, toY, fill=linecolor, width=3)
    else:
        canvas.create_line(fromX, fromY, toX, toY, fill=linecolor)
    
    labelX = (toX + fromX) / 2
    labelY = (toY + fromY) / 2
    lblFont = font.Font(family="Arial", size=8)
    label = tk.Label(canvas, text=str(edge.distance), background=labelbg, foreground="white", font=lblFont)
    label.update_idletasks()
    xOffset = lblFont.measure(str(edge.distance)) * 0.5
    yOffset = lblFont["size"]
    label.place(x=labelX-xOffset, y=labelY-yOffset)
    return edge

def create_graph(canvas:tk.Canvas, Algotype:str):  
    canvas.delete("all")
    drawn_edges = []

    for node in Graph.values():
        if node.name == "H":
            create_button_node(canvas, node, Algotype, "#00bb00", "white")
        else:
            create_button_node(canvas, node, Algotype)
        
        # Draw all undrawn edges with distance labels
        HALF_NODE_WIDTH = NODE_WIDTH // 2
        for edge in node.adjacent:
            if edge not in drawn_edges:
                drawn_edges.append(draw_labelled_edge(canvas, edge, HALF_NODE_WIDTH))

# Same algorithm is able to perform both GreedyBFS and A* as the only difference is the heuristic function
# The type parameter dictates whether we will use A* or not
def PerformSearch(canvas:tk.Canvas, start_node:graphnode, Graph:dict[str, graphnode], AlgoType:str) -> None:
    create_graph(canvas,AlgoType)
    # Calculate SLD for all nodes
    sld = { key: node.get_sld(TARGET_NODE) for key, node in Graph.items() }
    frontier = PriorityQueue()
    frontier.put((sld[start_node.name], start_node))
    parent = {start_node: None}
    cost_from_start = {start_node:0}
    explored_edges = []
    goal_not_found = True
    
    while not frontier.empty() and goal_not_found:
        current = frontier.get()[1]
        # Goal Check. If found, backtract to start to show distance
        if current.name == TARGET_NODE.name:
            goal_not_found = False
            path = []
            node = current
            drawn_edge = ""
            while node != None:
                if len(drawn_edge) < 2:
                    drawn_edge = node.name + drawn_edge
                else:
                    drawn_edge = node.name + drawn_edge[0]                    
                if len(drawn_edge) == 2:
                    # Sometimes edge name may appear reversed
                    to_draw = drawn_edge if drawn_edge[0] < drawn_edge[1] else drawn_edge[::-1]
                    draw_labelled_edge(canvas, Edges[to_draw], NODE_WIDTH // 2, "#00bb00", "#00bb00", True)
                path.append(node.name)
                node = parent[node]
            break
        for adjacent in filter(lambda x: x not in explored_edges, current.adjacent):
            explored_edges.append(adjacent)
            neighbour = adjacent.pointB if current is adjacent.pointA else adjacent.pointA
            distance = adjacent.distance
            priority = sld[neighbour.name]
            new_cost = cost_from_start[current] + distance                              
            if AlgoType == "A*":
                priority += new_cost
            if neighbour not in cost_from_start or (AlgoType == "A*" and new_cost < cost_from_start[neighbour]):
                cost_from_start[neighbour] = new_cost
                parent[neighbour] = current
                frontier.put((priority, neighbour))                                


def GreedyBFS(frame:ttk.Frame) -> None:
    ClearFrame(frame)
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack()
    create_title_label(canvas, "Informed GreedyBFS")
    create_graph(canvas, "GreedyBFS")

def AStar(frame:ttk.Frame) -> None:
    ClearFrame(frame)
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack()
    create_title_label(canvas, "Informed A*")
    create_graph(canvas, "A*")

def ClearFrame(frame:ttk.Frame):
    for widget in frame.winfo_children():
        widget.destroy()