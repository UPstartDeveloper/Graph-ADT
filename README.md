# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

### HW 1

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

    One major difference is that **in trees**, you are sure that each node only has 1 parent node, which is to say that **one and only one vertex has an edge that "leads" to a given node**. However in graphs there is no such restriction. So when implementing BFS **on a graph** for certain problems, such as returning all the vertices a given distance away from a starting vertex, you need to account for the possibility **there may be multiple paths to get from one vertex to another**. That leads to interesting trade-offs in how we decide how to count the distance between two nodes, and if we care about the alternative paths.

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

    One application of Breadth-first search is in business strategy. For example if an ice cream truck driver is figuring out how to traverse all the streets in a neighborhood or a certain part of town, they might use BFS to plan a route such that they only drive through each street once.

### HW 2

1. Compare and contrast Breadth-first Search and Depth-first Search by providing one similarity and one difference.

    One *difference* is that BFS is typically implemented using a queue, while DFS typically uses a stack. One *similarity* is that both BFS and DFS are used to return all the vertices in a graph, and therefore the runtime of these algorithms will at best be ```O(V + E)```, where ```V = number of vertices``` and ```E = the number of edges```.

2. Explain why a Depth-first Search traversal does not necessarily find the shortest path between two vertices. What is one such example of a graph where a DFS search would not find the shortest path?

    Depth-first search doesn't necessarily find the shortest path between two vertices, because within the stack there's no way to compare the differents distances between taking two paths like in BFS; because you are only focused on one path at a time. An example where this may happen is the graph below:

    ![Graph with multiple paths between origin and destination.](https://i.postimg.cc/WbBz5VVP/Screen-Shot-2020-06-12-at-12-29-21-PM.png)

    Considering the graph above, if you wanted to find a path between A and E, DFS would not necessarily find the shortest path. A DFS implementation may return either the path ```[A, B, E]``` or ```[A, C, D, E]```.

3. Explain why we cannot perform a topological sort on a graph containing a cycle.

    We cannot perform a topological sort on a cyclical graph because in a cycle, it is unclear how to define the sorting order. For Kahn's Algorithm as an example, there wouldn't be any vertex with an in-degree of zero. Alternatively with DFS you could choose a starting vertex randomly as always, but then that vertex would always be the beginning of the order. Therefore the order would be meaningless, because the function would return something different each time it executes. 