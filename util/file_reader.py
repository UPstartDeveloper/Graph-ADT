from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """
    # Open the file
    with open(filename) as f:
        # read in all lines from the file, without the '\n' characters
        lines = [line[:-1] for line in f.readlines()]
        # Use the first line (D/G) to create a directed/undirected graph
        directed_char = lines[0]
        # raise a ValueError if needed
        if not (directed_char == 'G' or directed_char == 'D'):
            raise ValueError('This graph has an invalid type') 
        is_directed = (directed_char == 'D')
        graph = Graph(is_directed)
        # Use the second line to add the vertices to the graph
        vertex_ids = lines[1].split(',')
        for id in vertex_ids:
            graph.add_vertex(id)
        # Use the 3rd+ line to add the edges to the graph
        for index, line in enumerate(lines):
            if index >= 2:
                # get ids of the vertices
                ids = line[1:4].split(',')
                # add an edge from the first vertex to the second
                vertex1, vertex2 = ids[0], ids[1]
                graph.add_edge(vertex1, vertex2)
        # Return the Graph
        return graph

if __name__ == '__main__':
    filename = 'test.txt'
    graph = read_graph_from_file(filename)

    print(graph)