from graphs.graph import Graph, Vertex
from collections import deque

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

    '''Kruskal's Algorithm'''

    def sort_edges(self, start_id):
        """
        Traverse the graph using breadth-first search.
        Outputs a list of all edges in the graph,
        sorted by weight.
        """
        # set for denoting the previously visited vertices
        seen = set()
        seen.add(start_id)
        # queue for visiting vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))
        # list of edges
        edges = list()
        # execute BFS
        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            neighbor_weights = list(current_vertex_obj.__neighbors_dict.values())
            for neighbor, weight in neighbor_weights:
                # form the possible element to add to the list
                weight_edge = (weight, current_vertex_id, neighbor.__id)
                reverse_weight_edge = (weight, neighbor.__id, current_vertex_id)
                # add if it's not already inside
                if weight_edge not in edges and reverse_weight_edge not in edges:
                    edges.append(weight_edge)

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)
        # now need to sort
        edges.sort()
        # everything processed
        return edges

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root


    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # Create a list of all edges in the graph, sort them by weight 
        edges = self.sort_edges()
        # Use dictionary 'parent_map' to map vertex -> its "parent". 
        # Initialized so that each vertex is its own parent.
        parent_map = dict()
        for vertex_obj in self.__vertex_dict.values():
            parent_map[vertex_obj.__id] = vertex_obj.__id
        # Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)
        mst_edges = list()
        # Build the MST - loop until we have # edges = # vertices - 1
        while len(mst_edges) < len(self.__vertex_dict) - 1:
            # get the smallest edge
            next_edge = edges[0]
            # determine if the edge can be added (must be in different sets)
            weight, vertex1, vertex2 = next_edge
            if (self.find(parent_map, vertex1.__id) == self.find(parent_map, vertex2.__id)) is False:
                mst_edges.append(next_edge)
                edges.remove(next_edge)

        # Return the solution list
        return mst_edges
