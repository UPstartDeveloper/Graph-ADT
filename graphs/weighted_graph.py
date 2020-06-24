from graphs.graph import Graph, Vertex

class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        '''
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        '''
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> (obj, weight)
        # super(Vertex, self).__init__(vertex_id)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        neighbor_id = vertex_obj.__id
        self.__neighbors_dict[neighbor_id] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        neighbor_ids = [
            neighbor.__id for neighbor, weight 
            in list(self.__neighbors_dict.values())
        ]
        return neighbor_ids

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        neighbors_with_weights = [
            (neighbor.__id, weight) for neighbor, weight 
            in list(self.__neighbors_dict.values())
        ]
        return neighbors_with_weights


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        '''
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        '''
        self.__vertex_dict = {} # id -> object
        self.__is_directed = is_directed
        # super().__init__(is_directed)

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        new_vertex = WeightedVertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # make sure the vertices are included in the graph
        all_ids = list(self.__vertex_dict.keys())
        if (vertex_id1 not in all_ids) or (vertex_id2 not in all_ids):
            raise ValueError('One or both vertices not found.')
        # store pointers to the vertices in memory
        vertex1, vertex2 = (
            self.__vertex_dict[vertex_id1],
            self.__vertex_dict[vertex_id2]
        )
        # add the edge between vertex 1 and 2
        vertex1.add_neighbor((vertex2, weight))
        # if undirected, add the same edge the reverse as well
        if self.__is_directed is False:
            vertex2.add_neighbor((vertex1, weight))
