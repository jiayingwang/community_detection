import unittest
from simple_graph import Graph 
from community_detection import FastUnfolding


class TestFastUnfolding(unittest.TestCase):

    def test_process(self):
        G = Graph({0: [1, 2], 1: [2]})
        fu = FastUnfolding()
        communities = fu.process(G)
        self.assertEqual(communities, [[0, 1, 2]])
        G = Graph({1: {2, 4, 7}, 2: {1, 0, 4, 6}, 4: {1, 2, 10}, 7: {1, 3, 5, 6}, 0: {2, 3, 5}, 6: {2, 7, 11}, 3: {0, 7}, 5: {0, 7, 11}, 10: {4, 11, 14, 13}, 11: {6, 5, 10}, 14: {10, 8, 9}, 13: {10}, 8: {15, 14, 9}, 15: {8}, 9: {8, 14, 12}, 12: {9}}, undirected=False)
        communities = fu.process(G)
        self.assertEqual(communities, [[1, 2, 4, 7, 0, 6, 3, 5], [10, 11, 13], [14, 8, 9, 15, 12]])

        G = Graph({0: [], 1: [], 2:[]})
        communities = fu.process(G)
        self.assertEqual(communities, [[0],[1], [2]])

        G = Graph({0: {1}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}})
        communities = fu.process(G)
        self.assertEqual(communities, [[0,1],[2],[3],[4],[5],[6],[7]])
        
    def test_modularity(self):
        G = Graph({0: [1, 2], 1: [2]})
        fu = FastUnfolding()
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
        G = Graph({1: {2, 4, 7}, 2: {1, 0, 4, 6}, 4: {1, 2, 10}, 7: {1, 3, 5, 6}, 0: {2, 3, 5}, 6: {2, 7, 11}, 3: {0, 7}, 5: {0, 7, 11}, 10: {4, 11, 14, 13}, 11: {6, 5, 10}, 14: {10, 8, 9}, 13: {10}, 8: {15, 14, 9}, 15: {8}, 9: {8, 14, 12}, 12: {9}}, undirected=False)
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.3998)
        
        # check graph with isolated nodes
        G = Graph({0: [], 1: [], 2:[]})
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
    
        G = Graph({0: {1}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}})
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
        
if __name__ == '__main__':
    unittest.main()
