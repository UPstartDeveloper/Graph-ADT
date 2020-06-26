from graphs.graph import Graph, Vertex
from collections import deque

class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        '''
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        '''
        self.id = vertex_id
        self.neighbors_dict = {} # id -> (obj, weight)
        # super(Vertex, self).__init__(vertex_id)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        """neighbor_id = vertex_obj.__id
        self.__neighbors_dict[neighbor_id] = (vertex_obj, weight)"""
        if vertex_obj.get_id() in self.neighbors_dict.keys():
            return # it's already a neighbor

        self.neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        neighbor_ids = [
            neighbor for neighbor, weight 
            in list(self.neighbors_dict.values())
        ]
        return neighbor_ids

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        '''
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        '''
        self.vertex_dict = {} # id -> object
        self.is_directed = is_directed
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
        self.vertex_dict[vertex_id] = new_vertex
        return new_vertex

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # make sure the vertices are included in the graph
        all_ids = list(self.vertex_dict.keys())
        if (vertex_id1 not in all_ids) or (vertex_id2 not in all_ids):
            raise ValueError('One or both vertices not found.')
        # store pointers to the vertices in memory
        vertex1, vertex2 = (
            self.vertex_dict[vertex_id1],
            self.vertex_dict[vertex_id2]
        )
        # add the edge between vertex 1 and 2
        vertex1.add_neighbor(vertex2, weight)
        # if undirected, add the same edge the reverse as well
        if self.is_directed is False:
            vertex2.add_neighbor(vertex1, weight)

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
        queue.append(self.vertex_dict[start_id])
        # list of edges
        edges = list()
        # execute BFS
        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            neighbor_weights = list(current_vertex_obj.neighbors_dict.values())
            for neighbor, weight in neighbor_weights:
                # form the possible element to add to the list
                weight_edge = (weight, current_vertex_id, neighbor.id)
                reverse_weight_edge = (weight, neighbor.id, current_vertex_id)
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
        start_id = list(self.vertex_dict.keys())[0]
        edges = self.sort_edges(start_id)
        # Use dictionary 'parent_map' to map vertex -> its "parent". 
        # Initialized so that each vertex is its own parent.
        parent_map = dict()
        for vertex_obj in self.vertex_dict.values():
            parent_map[vertex_obj.id] = vertex_obj.id
        # Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)
        mst_edges = list()
        # Build the MST - loop until we have # edges = # vertices - 1
        while len(mst_edges) < len(self.vertex_dict) - 1:
            # get the smallest edge
            next_edge = edges[0]
            # determine if the edge can be added (must be in different sets)
            weight, vertex1_id, vertex2_id = next_edge
            if (self.find(parent_map, vertex1_id) == self.find(parent_map, vertex2_id)) is False:
                # rearrange the edge
                mst_edge = (vertex1_id, vertex2_id, weight)
                mst_edges.append(mst_edge)
                # remove it from the list of possible edges
                edges.remove(next_edge)

        # Return the solution list
        # print(f"Kruskal's Results: {mst_edges}")
        return sorted(mst_edges)
    
    '''Prim's Algorithm'''

    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.

        Assume that the graph is connected.
        """
        # initialize all vertex distances to INFINITY away
        vertex_to_weight = dict()
        for vertex_obj in self.vertex_dict.values():
            vertex_to_weight[vertex_obj] = float('inf')
        # Choose one vertex and set its weight to 0
        start_vertex = list(vertex_to_weight.keys())[0]
        vertex_to_weight[start_vertex] = 0
        # Calculate total weight of MST
        weight = 0
        while len(list(vertex_to_weight.items())) > 0:
            # A Get the minimum-weighted remaining vertex
            min_distance = min(list(vertex_to_weight.values()))
            min_vertex = None
            for vertex_obj, weight in vertex_to_weight.items():
                if weight == min_distance:
                    min_vertex = vertex_obj
            # remove it from the dictionary
            del vertex_to_weight[min_vertex]
            # add its weight to the total MST weight
            print(f'Min dist: {vertex_to_weight}')
            weight += min_distance
            # B: Update that vertex's neighbors
            print(vertex_to_weight)
            for neighbor, weight in min_vertex.neighbors_dict.values():
                if neighbor in vertex_to_weight:
                    current_distance = vertex_to_weight[neighbor]
                    # Update ONLY to reduce the weight of the distance
                    if weight < current_distance:
                        vertex_to_weight[neighbor] = weight
        # Return total weight of MST
        return weight

    '''Shortest Path Finding'''

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight
        of the shortest path from a start vertex 
        to a destination.
        """
        # A: initialize all vertex distances to INFINITY away
        vertex_to_weight = dict()
        for vertex_obj in self.vertex_dict.values():
            vertex_to_weight[vertex_obj] = float('inf')

        # B: Calculate the Path Weight, from starting vertex
        path_weight = 0
        # Choose one vertex and set its weight to 0
        start_vertex = self.vertex_dict[start_id]
        vertex_to_weight[start_vertex] = 0
        while len(list(vertex_to_weight.items())) > 0:
            # Get the minimum-distance remaining vertex
            min_distance = min(list(vertex_to_weight.values()))
            # print(f'Min dist: {min_distance}')
            min_vertex = None
            # remove it from the dictionary
            for vertex in vertex_to_weight:
                if vertex_to_weight[vertex] == min_distance:
                    min_vertex = vertex
                    # print(f'Vertex: {vertex}')
            del vertex_to_weight[vertex]
            # If target found, return its distance
            path_weight += min_distance
            if min_vertex.id == target_id:
                return path_weight 
            # B: Update that vertex's neighbors
            neighbor_weights = (
                list(min_vertex.neighbors_dict.values())
            )
            for neighbor, weight in neighbor_weights:
                if neighbor in vertex_to_weight:
                    current_distance = vertex_to_weight[neighbor]
                    # Update ONLY to reduce the weight of the distance
                    if weight < current_distance:
                        vertex_to_weight[neighbor] = weight

        # target vertex NOT FOUND
        return None

    def floyd_warshall(self):
        """Returns an adjaceny matrix of all-pairs shortest paths in the
           graph.
        
        """
        # list of all vertex ids
        all_vertex_ids = list(self.vertex_dict.keys())
        # init the distances dict
        dist = dict()
        for id in all_vertex_ids:
            dict_for_top_level = dict()
            for id2 in all_vertex_ids:
                dict_for_top_level[id2] = float('inf')
            dist[id] = dict_for_top_level
        # update the default distances (v -> v is 0)
        for id in all_vertex_ids:
            dist[id][id] = 0
        # update the distances based on edge weights (v1 -> v2)
        for id in all_vertex_ids:
            vertex_obj = self.vertex_dict[id]
            for id2 in all_vertex_ids:
                if id != id2:
                    # get the edge weight
                    pass
        # build the distances
        for k in all_vertex_ids:
            for i in all_vertex_ids:
                for j in all_vertex_ids:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist