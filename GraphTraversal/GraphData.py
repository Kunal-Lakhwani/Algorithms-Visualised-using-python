from GraphTraversal.GraphDS import graphnode, graphedge

def get_graph_and_edges(TARGET_NODE:graphnode, NODE_WIDTH:int) -> tuple[dict[str, graphnode], dict[str, graphedge]]:
    Graph = {
        "A": graphnode("A", 150, 400, NODE_WIDTH),
        "B": graphnode("B", 250, 150, NODE_WIDTH),
        "C": graphnode("C", 200, 500, NODE_WIDTH),
        "D": graphnode("D", 450, 450, NODE_WIDTH),
        "E": graphnode("E", 600, 230, NODE_WIDTH),
        "F": graphnode("F", 700, 200, NODE_WIDTH),
        "G": graphnode("G", 900, 300, NODE_WIDTH),
        "H": TARGET_NODE,
    }
    # Dict of edges:
    Edges = {
        "AB": graphedge(Graph["A"], Graph["B"], 130),
        "AC": graphedge(Graph["A"], Graph["C"], 20),
        "BC": graphedge(Graph["B"], Graph["C"], 50),
        "BD": graphedge(Graph["B"], Graph["D"], 90),
        "CD": graphedge(Graph["C"], Graph["D"], 150),
        "DE": graphedge(Graph["D"], Graph["E"], 100),
        "DH": graphedge(Graph["D"], Graph["H"], 300),
        "EF": graphedge(Graph["E"], Graph["F"], 20),
        "FG": graphedge(Graph["F"], Graph["G"], 60),
        "FH": graphedge(Graph["F"], Graph["H"], 100),
        "GH": graphedge(Graph["G"], Graph["H"], 20)
    }

    # Assign edges to adjacency lists of nodes
    # Adjacent A = [AB, AC]
    Graph["A"].adjacent = [Edges["AB"], Edges["AC"]]
    # Adjacent B = [AB, BC, BD]
    Graph["B"].adjacent = [Edges["AB"],Edges["BC"], Edges["BD"]]
    # Adjacent C = [AC, BC, CD]
    Graph["C"].adjacent = [Edges["AC"],Edges["BC"], Edges["CD"]]
    # Adjacent D = [BD, CD, DE, DH]
    Graph["D"].adjacent = [Edges["BD"], Edges["CD"], Edges["DE"], Edges["DH"]]
    # Adjacent E = [DE, EF]
    Graph["E"].adjacent = [Edges["DE"], Edges["EF"]]
    # Adjacent F = [EF, FG, FH]
    Graph["F"].adjacent = [Edges["EF"], Edges["FG"], Edges["FH"]]
    # Adjacent G = [FG, GH]
    Graph["G"].adjacent = [Edges["FG"], Edges["GH"]]
    # Adjacent H = [DH, FH, GH]
    Graph["H"].adjacent = [Edges["DH"], Edges["FH"], Edges["GH"]]

    return (Graph, Edges)