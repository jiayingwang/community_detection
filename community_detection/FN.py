from math import inf
import copy
from community_detection.community_utility import CommunityUtility
from simple_graph import Graph


class FN:

    def __init__(self, verbose=False):
        self._verbose = verbose

    def modularity(self, G, coms):
        com_utils = CommunityUtility(G, verbose=self._verbose)
        com_utils.init_stats(coms)
        return float(f'{com_utils.modularity():.4f}')

    def process(self, G):
        self._G_cloned = G
        self._G = copy.deepcopy(G)
        self.edges = [n for n in self._G_cloned.edges]
        self._G_cloned.remove_edges(self.edges)
        self.temp_q = {}
        self.temp_e = {}
        self._max_Q = self.modularity(self._G, [list(c) for c in list(self._G_cloned.connected_components)])
        self._option_Q = {}
        while len(self._G_cloned.edges) != len(self._G.edges):
            for e in self.edges:
                self.merge_community(e[0], e[1])

            self._G_cloned.add_edge(self.temp_e[max(self.temp_e)][0], self.temp_e[max(self.temp_e)][1])
            self._max_Q = self.modularity(self._G, self.temp_q[max(self.temp_q)])
            self.edges.remove(tuple(self.temp_e[max(self.temp_e)]))
            self._option_Q[self._max_Q] = self.temp_q[max(self.temp_q)]
            self.temp_e.clear()
            self.temp_q.clear()
        return self._option_Q[max(self._option_Q)]

    def merge_community(self, n1, n2):
        self._G_cloned.add_edge(n1, n2)
        components = [list(c) for c in list(self._G_cloned.connected_components)]
        self.temp_q[self.modularity(self._G, components) - self._max_Q] = components
        self.temp_e[self.modularity(self._G, components) - self._max_Q] = [n1, n2]
        self._G_cloned.remove_edge(n1, n2)
