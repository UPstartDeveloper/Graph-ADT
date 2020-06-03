# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

    One major difference is that **in trees**, you are sure that each node only has 1 parent node, which is to say that **one and only one vertex has an edge that "leads" to a given node**. However in graphs there is no such restriction. So when implementing BFS **on a graph** for certain problems, such as returning all the vertices a given distance away from a starting vertex, you need to account for the possibility **there may be multiple paths to get from one vertex to another**. That leads to interesting trade-offs in how we decide how to count the distance between two nodes, and if we care about the alternative paths.

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

    One application of Breadth-first search is in business strategy. For example if an ice cream truck driver is figuring out how to traverse all the streets in a neighborhood or a certain part of town, they might use BFS to plan a route such that they only drive through each street once.
