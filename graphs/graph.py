from collections import deque

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        neighbor_id = vertex_obj.__id
        self.__neighbors_dict[neighbor_id] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        new_vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = new_vertex
        return new_vertex

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # store both vertex 1 and vertex 2 in a variable
        vertex_1, vertex_2 = (
            self.__vertex_dict[vertex_id1], 
            self.__vertex_dict[vertex_id2]
        )
        # make the vertex 2 a neighbor of vertex 1
        vertex_1.add_neighbor(vertex_2)
        # if the graph is undirected, make the edge go both ways
        if self.__is_directed is False:
            vertex_2.add_neighbor(vertex_1)

    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        In this implementation, if a vertex has multiple paths that differ in distance
        from the starting vertex, then only the shortest distance is used to determine if
        should be returned or not.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        # check to make sure we have a valid start_id
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")
        # Store the starting vertex in a variable 
        starting_vertex_obj = self.get_vertex(start_id)

        # Keep a count of steps taken from start so far
        steps = -1

        # Keep a dict of Vertex ids, mapped to their distances from the start
        vertex_distances = dict()

        # queue of vertices to visit next
        queue = deque() 
        queue.append(starting_vertex_obj)

        # Perform a BFS, for only up to the nodes that lie up to
        # a "target_distance" away from the start (only shortest path considered)
        while steps < target_distance:
            # init a list of neighbors to process after this iteration
            neighbors = list()
            # Dequeue all the vertices in the queue
            while len(queue) > 0:
                current_vertex_obj = queue.popleft()
                current_vertex_id = current_vertex_obj.get_id()
                # add the current vertex to the dict
                if current_vertex_id not in vertex_distances:
                    vertex_distances[current_vertex_id] = steps + 1
                # Keep track of vertices to process on next iteration
                neighbors.extend(current_vertex_obj.get_neighbors())
            # enqueue the vertices to visit on the next iteration
            for neighbor in neighbors:
                queue.append(neighbor)
            # Increment the steps taken so far
            steps += 1
        
        # Return the ids of the vertices a target distance away
        return [
            vertex_id for vertex_id in vertex_distances if
            vertex_distances[vertex_id] == target_distance
        ]

    def is_bipartite(self):
        """Return True if the graph is bipartite, False otherwise."""
        # init a queue
        queue = deque()
        # keep track of objects seen so far
        seen = set()
        # keep track of groups in dict
        vertex_groups = dict()
        # pick a random vertex to start
        start_id = list(self.__vertex_dict.keys())[0]
        # enqueue the starting vertex, and assign it a group
        queue.append((self.__vertex_dict[start_id], 0))
        vertex_groups[start_id] = 0
        # perform BFS
        while queue:
            # process the vertex at the front of the queue
            current_vertex_obj, current_group_num = queue.pop()
            # print(f'Current group num: {current_vertex_obj, current_group_num}')
            current_vertex_id = current_vertex_obj.get_id()
            seen.add(current_vertex_id)
            # enqueue the neighbors, and assign them a group
            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                # if you hit a vertex that has a number already,
                # AND which different from what's allowed, return FALSE
                neighbor_id = neighbor.get_id()
                # print(vertex_groups)
                if neighbor_id in vertex_groups.keys():
                    neighbor_group_num = vertex_groups[neighbor.get_id()]
                    if neighbor_group_num == current_group_num:
                        # print(vertex_groups)
                        # print(f"{neighbor_id} has the worong group num: {neighbor_group_num}")
                        return False
                # enqueue neighbors and assign groups: 
                # neighbors should be of different groups
                elif neighbor.get_id() not in seen:
                    group_to_assign = 1 if current_group_num == 0 else 0
                    # print(f'group_to_assign: {neighbor_id, group_to_assign}')
                    vertex_groups[neighbor_id] = group_to_assign
                    queue.appendleft((neighbor, group_to_assign))
        return True
    """
    def find_connected_components(self):
        '''Return a 2D list of connected components.
           Each of the inner lists contains vertex ids.
           A connected component of a graph is a set
           of vertices for which there is a path between any pair of vertices.

        '''
        # set for all previous seen vertices
        seen = set()
        # pick the start vertex of the traversal
        start_id = list(self.__vertex_dict.keys())[0]
        start_vertex =  self.__vertex_dict[start_id]
        # loop over all vertices in graph
        queue = deque()
        # add the start vertex to the queue and set
        queue.append(start_vertex)
        seen.add(start_vertex)
        # execute BFS - init list for connected components
        connected_comp = []
        while queue:
            # dequeue a vertex
            current_vertex = queue.pop()
            # enqueue the neighbors to keep th BFS going
            neighbors = current_vertex.get_neighbors()
            queue.extend([n for n in neighbors if n not in seen])
            # look at its neighbors to see if it's a connected component
            for neighbor in neighbors:
                # if not a connected component, then break out
                if set(neighbor.get_neighbors()) != set(neighbors):
                    break
            # if you made it here, looks like we have a connected component
            connected_comp.append(neighbors)
        # return the connected components
        return connected_comp
    """

    def dfs_for_cycles(self, start_vertex, visited):
        """This is recursive. Don't forget it!"""
        # visit this vertex
        visited.add(start_vertex)
        neighbors = start_vertex.get_neighbors()
        # if cycle is found
        if len(neighbors) > 1 and set(neighbors) <= visited:
             return True
        for neighbor in neighbors:
            if neighbor not in visited:
                self.dfs_for_cycles(neighbor, visited)
        # return True


    def contains_cycle(self, start_vertex=None, visited=None):
        """Returns True if the Graph contains a cycle."""
        # pick vertex to start with randomly 
        if start_vertex is None:
            start_id = list(self.__vertex_dict.keys())[0]
            start_vertex =  self.__vertex_dict[start_id]
        # init a visited set
        if visited is None:
            visited = set()
        # pass these two vars above into dfs()
        is_cycle = self.dfs_for_cycles(start_vertex, visited)
        print(f'Is it a Cycle: {is_cycle}')
        # final return value
        return (is_cycle == True)
        """
        # on first call, init the start_vertex
        if start_vertex is None:
            start_id = list(self.__vertex_dict.keys())[0]
            start_vertex =  self.__vertex_dict[start_id]
        # visit this vertex
        visited.add(start_vertex)
        for neighbor in start_vertex.get_neighbors():
            if neighbor not in visited:
                self.contains_cycle(neighbor, visited)
            else:
                return True
        # if no cycle found, but more connected components to search
        pass
        # after all vertices are visited
        return False
        """

# Trace for Contains Cycles method:
# visited = current_path
# start_vertex = A
# [A, B]

# neighbors 
# [B, C]

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        # Make a stack containing only the start node
        start_vertex =  self.__vertex_dict[start_id]
        stack = [start_id]
        # Init 'distances' dictionary with the start node at distance 0
        distances = {start_id: stack.copy()}
        # While the stack is not empty
        while len(stack) > 0:
            # Pop a node from the stack.
            node = self.__vertex_dict[stack.pop()]
            # For each of the node’s neighbors:
            for neighbor in node.get_neighbors():
                neighbor_id = neighbor.get_id()
                # If the neighbor has already been visited, skip it.
                if neighbor_id not in distances:
                    # 'Visit' the neighbor - add to stack and distances
                    stack.append(neighbor_id)
                    distance_to_neighbor = distances[node.get_id()].copy()
                    distance_to_neighbor.append(neighbor_id)
                    distances[neighbor_id] = distance_to_neighbor
        # Look up the target node in distances
        return distances[target_id]

    def topological_sort(self):
        """Return a list of vertex ids in topological order."""
        # Create a stack to hold the vertices
        solution_stack = list()
        # set of visited vertices; only DFS on vertices not visited yet
        visited = set()
        # For each unvisited vertex, execute a DFS from that vertex
        for vertex in self.__vertex_dict.values():
            if vertex not in visited:
                visited, solution_stack = (
                    self.dfs(vertex, solution_stack, visited)
                )
        # Reverse the contents of the stack
        solution = list()
        for i in range(len(self.__vertex_dict)):
            solution.append(solution_stack.pop().get_id())
        return solution
        
    def dfs(self, vertex, solution_stack, visited):
        """This is recursive. Don't forget it!"""
        neighbors = vertex.get_neighbors()
        visited.add(vertex)
        # visit neighbors
        for neighbor in neighbors:
            if neighbor not in visited:
                self.dfs(neighbor, solution_stack, visited)
        # visit this vertex
        solution_stack.append(vertex)
        return visited, solution_stack
