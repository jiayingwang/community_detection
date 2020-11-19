import unittest
from simple_graph import Graph 
from community_detection import FastUnfolding


class TestFastUnfolding(unittest.TestCase):

    def test_process(self):
        G = Graph({0: [1, 2], 1: [2]})
        fu = FastUnfolding()
        communities = fu.process(G)
        self.assertEqual(communities, [[0, 1, 2]])
        G = Graph({1: {2: 1, 4: 1, 7: 1}, 2: {1: 1, 0: 1, 4: 1, 6: 1}, 4: {1: 1, 2: 1, 10: 1}, 7: {1: 1, 3: 1, 5: 1, 6: 1}, 0: {2: 1, 3: 1, 5: 1}, 6: {2: 1, 7: 1, 11: 1}, 3: {0: 1, 7: 1}, 5: {0: 1, 7: 1, 11: 1}, 10: {4: 1, 11: 1, 14: 1, 13: 1}, 11: {6: 1, 5: 1, 10: 1}, 14: {10: 1, 8: 1, 9: 1}, 13: {10: 1}, 8: {15: 1, 14: 1, 9: 1}, 15: {8: 1}, 9: {8: 1, 14: 1, 12: 1}, 12: {9: 1}}, symmetric=False)
        communities = fu.process(G)
        self.assertEqual(communities, [[1, 2, 4, 7, 0, 6, 3, 5], [10, 11, 13], [14, 8, 9, 15, 12]])

        G = Graph({0: [], 1: [], 2:[]})
        fu = FastUnfolding()
        communities = fu.process(G)
        self.assertEqual(communities, [[0],[1], [2]])

        G = Graph({0: {1:1}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}})
        fu = FastUnfolding()
        communities = fu.process(G)
        self.assertEqual(communities, [[0,1],[2],[3],[4],[5],[6],[7]])
        
    def test_modularity(self):
        G = Graph({0: [1, 2], 1: [2]})
        fu = FastUnfolding()
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
        G = Graph({1: {2: 1, 4: 1, 7: 1}, 2: {1: 1, 0: 1, 4: 1, 6: 1}, 4: {1: 1, 2: 1, 10: 1}, 7: {1: 1, 3: 1, 5: 1, 6: 1}, 0: {2: 1, 3: 1, 5: 1}, 6: {2: 1, 7: 1, 11: 1}, 3: {0: 1, 7: 1}, 5: {0: 1, 7: 1, 11: 1}, 10: {4: 1, 11: 1, 14: 1, 13: 1}, 11: {6: 1, 5: 1, 10: 1}, 14: {10: 1, 8: 1, 9: 1}, 13: {10: 1}, 8: {15: 1, 14: 1, 9: 1}, 15: {8: 1}, 9: {8: 1, 14: 1, 12: 1}, 12: {9: 1}}, symmetric=False)
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.3998)
        
        # check graph with isolated nodes
        G = Graph({0: [], 1: [], 2:[]})
        fu = FastUnfolding()
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
    
        G = Graph({0: {1:1}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}})
        fu = FastUnfolding()
        communities = fu.process(G)
        Q = fu.modularity(G, communities)
        self.assertEqual(Q, 0.0)
        
if __name__ == '__main__':
    unittest.main()
