import unittest
from graphs.weighted_graph import WeightedVertex, WeightedGraph


class TestWeightedGraph(unittest.TestCase):
    def test_add_vertex(self):
        """A WeightedGraph object is a composition (has-a relationship) 
           of one or multiple WeightedVertex objects.
        
        """
        # example id of a vertex
        vertex_id = 'A'
        # test instantiation of weighted directed graph
        d_graph = WeightedGraph()
        self.assertEqual(len(list(d_graph.__vertex_dict.items())), 0)
        self.assertTrue(d_graph.__is_directed)
        # test adding a vertex
        d_graph.add_vertex(vertex_id)
        self.assertEqual(len(list(d_graph.__vertex_dict.items())), 1)
        vertex_added = d_graph.__vertex_dict[vertex_id]
        self.assertTrue(isinstance(vertex_added, WeightedVertex))
        self.assertEqual(vertex_added.__id, vertex_id)

if __name__ == "__main__":
    unittest.main()