from math import inf
import copy
from community_detection.community_utility import CommunityUtility

'''
  paper: <Community structure in social and biological networks>
'''

class GN:
    
  def __init__(self, verbose=False):
    self._verbose = verbose

  def modularity(self, G, coms):
    com_utils = CommunityUtility(G, verbose=self._verbose)
    com_utils.init_stats(coms)
    return float(f'{com_utils.modularity():.4f}')

  def process(self, G):
    self._G_cloned = G
    self._G = copy.deepcopy(G)
    self._communities = self._G.connected_components
    self._max_Q = self.modularity(self._G_cloned, self._communities)
    if self._verbose:
      print('initial Q:', self._max_Q)
    while len(self._G.edges) != 0:
      edge = max(self._G.edge_betweenness().items(),key=lambda item:item[1])[0]
      if self._verbose:
        print('remove edge:', edge)
      self._G.remove_edge(edge[0], edge[1])
      components = self._G.connected_components
      if len(components) != len(self._communities):
        cur_Q = self.modularity(self._G_cloned, components)
        if self._verbose:
          print("Q:", cur_Q, self._max_Q)
        if cur_Q > self._max_Q:
          self._max_Q = cur_Q
          self._communities = components
    return self._communities