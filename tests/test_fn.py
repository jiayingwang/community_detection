import unittest
from simple_graph import Graph
from community_detection import FN

class TestFN(unittest.TestCase):
  
  def test_process(self):
    G = Graph({0:[1,2],1:[2]})
    fn = FN()
    communities = fn.process(G)
    self.assertEqual(communities, [[0,1,2]])
    G = Graph({1: {2, 4, 7}, 2: {1, 0, 4, 6}, 4: {1, 2, 10}, 7: {1, 3, 5, 6}, 0: {2, 3, 5}, 6: {2, 7, 11},
                   3: {0, 7}, 5: {0, 7, 11}, 10: {4, 11, 14, 13}, 11: {6, 5, 10}, 14: {10, 8, 9}, 13: {10},
                   8: {15, 14, 9}, 15: {8}, 9: {8, 14, 12}, 12: {9}})
    communities = fn.process(G)
    self.assertEqual(communities, [[1, 2, 4, 5, 6, 7, 11], [0, 3], [8, 9, 10, 12, 13, 14, 15]])

    G = Graph({0: [], 1: [], 2: []})
    communities = fn.process(G)
    self.assertEqual(communities, [[0], [1], [2]])

    G = Graph({0: {1}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}})
    communities = fn.process(G)
    self.assertEqual(communities, [[0, 1], [2], [3], [4], [5], [6], [7]])
  
if __name__ == '__main__':
  unittest.main()