from math import inf
import copy

class CommunityUtility:
  def __init__(self, G, verbose=False):
    self.C = copy.deepcopy(G)
    for i in self.C.vertices:
      u = self.C.vertex(i)
      u.inner_vertices = {i}
      u.inner_weight = .0
      u.total_weight = self.C.total_edge_weight(i)
    self.total_edge_weight = self.C.total_edge_weight()

  def calculate_Q(self):
    q = .0
    if not self.total_edge_weight:
      return q
    for i in self.C.vertices:
      u = self.C.vertex(i)
      q += u.inner_weight/self.total_edge_weight - (u.total_weight/self.total_edge_weight)**2
    return q

  def calculate_delta_Q(self, i, j):
    return (self.C.edge_weight(i, j) + self.C.edge_weight(j, i) - \
            2*self.C.vertex(i).total_weight * self.C.vertex(j).total_weight / self.total_edge_weight) / self.total_edge_weight


  def merge_communities(self, i, j):
    '''
        merge community i, j to one community
    '''
    u = self.C.vertex(i)
    v = self.C.vertex(j)
    # merge vertices from j to i
    u.inner_vertices |= v.inner_vertices
    # merge edge from j to i
    # all edges betweeen i, j will be inner edges
    u.inner_weight += self.C.edge_weight(i, j) + self.C.edge_weight(j, i)
    self.C.remove_edge(i, j)
    self.C.remove_edge(j, i)

    # all the other edges of j will merge to i
    for n in self.C.neighbors(j):
        self.C.add_edge_weight(i, n, self.C.edge_weight(j, n))
    # if C is not directed, the reverse edge should also be considered
    if not self.C.undirected:
      for n in self.C.reverse_neighbors(j):
        self.C.add_edge_weight(n, i, self.C.edge_weight(n, j))
    # merge total weight
    u.total_weight += v.total_weight

    # remove j
    self.C.remove_vertex(j)

  def find_best_communities_to_merge(self):
    best = -inf
    winner = None
    for i in self.C.vertices:
      for j in self.C.neighbors(i):
        delta_Q = self.calculate_delta_Q(i, j)
        if delta_Q > best:
          best = delta_Q
          winner = (i, j)
    if winner:
      self.merge_communities(winner[0], winner[1])
    return best

  def get_communities(self):
    return [list(self.C.vertex(i).inner_vertices) for i in self.C.vertices]
                

class FN:
  def __init__(self, verbose=False):
    self._verbose = verbose

  def process(self, G):
    self.com_utils = CommunityUtility(G, verbose=self._verbose)
    best_Q = Q = self.com_utils.calculate_Q()
    communities = self.com_utils.get_communities()
    step = len(G.vertices)-1
    for i in range(step):
      delta_Q = self.com_utils.find_best_communities_to_merge()
      Q += delta_Q
      if Q > best_Q:
        communities = self.com_utils.get_communities()
      if Q == -inf:
        break
    return communities
