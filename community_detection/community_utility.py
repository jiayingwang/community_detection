from collections import defaultdict
from simple_graph import Graph
from elegant_io import eprint

class CommunityUtility:
  '''
      record history of community changes
      compute community edge weights dynamicly
  '''
  def __init__(self, G, verbose=False):
    self.G = self.origin_G = G
    self.history = []
    self.verbose = verbose

  def init_stats(self, coms=None):
    '''
      initial using graph G
      default each node is a community
    '''
    self.nc_map = {}
    self.com_edge_weights = defaultdict(int)
    self.total_vertex_edge_weights = {}
    for u in self.G.vertices:
      self.total_vertex_edge_weights[u] = self.G.total_edge_weight(u)
    self.total_edge_weight = self.G.total_edge_weight()
    if self.verbose:
      eprint(f'vertices: {len(self.G.vertices)}')
    if coms:
      for c, vertices in enumerate(coms):
        for n in vertices:
          self.nc_map[n] = c
          self.com_edge_weights[c] += self.total_vertex_edge_weights[n]
    else:
      for c, n in enumerate(self.G.vertices):
        self.nc_map[n] = c
        self.com_edge_weights[c] = self.total_vertex_edge_weights[n]

  def remove(self, n, c):
    '''
        remove a node n from community c
    '''
    self.nc_map[n] = None
    self.com_edge_weights[c] -= self.total_vertex_edge_weights[n]

  def insert(self, n, c):
    '''
        add a node n into community c
    '''
    self.nc_map[n] = c
    self.com_edge_weights[c] += self.total_vertex_edge_weights[n]

  def get_nb_com_weights(self, n):
    '''
        find a node n's neighbor communities and sum of edge weights
        the community contains n is also considered as a neighbor community of n
    '''
    nb_coms = defaultdict(int)
    n_c = self.nc_map[n]
    for u in self.G.neighbors(n):
      if u != n:
        u_c = self.nc_map[u]
        nb_coms[u_c] += self.G.edge_weight(n, u)
    for u in self.G.reverse_neighbors(n):
      if u != n:
        u_c = self.nc_map[u]
        nb_coms[u_c] += self.G.edge_weight(u, n)
    return nb_coms

  def get_communities(self, mode='current'):
    '''
        get communities (a list of vertices)
    '''
    if mode == 'current':
      # current status
      nc_map = self.nc_map
    elif mode == 'final':
      # final status
      nc_map = self.generate_final_nc_map()
    else:
      return NotImplementedError
    c_nlist = defaultdict(list)
    for n, c in nc_map.items():
      c_nlist[c].append(n)
    return list(c_nlist.values())

  def generate_final_nc_map(self):
    '''
        generate nc_map using history
    '''
    nc_map = {n: n for n in self.origin_G.vertices}
    # get the map relationship using history
    for n in nc_map:
      for i, step_nc_map in enumerate(self.history):
        if nc_map[n] not in step_nc_map:
          nc_map[n] = str(i) + '-' + str(nc_map[n])
          break
        else:
          nc_map[n] = step_nc_map[nc_map[n]]
    return nc_map

  def relabel_nc_map(self):
    '''
        relabel communities from 0 to n.
    '''
    com_labels = set(self.nc_map.values())
    if self.verbose:
      eprint(f'{len(com_labels)} communities detected')
    relabel_coms = {j: i for i, j in enumerate(com_labels)}
    for n in self.nc_map:
      self.nc_map[n] = relabel_coms[self.nc_map[n]]

  def add_history(self):
    '''
        record nc_map to history
    '''
    self.history.append(self.nc_map)

  def rebuild_graph(self):
    '''
        create a new graph to merge communities to vertices
    '''
    graph = Graph()
    for u, v in self.G.edges:
      u_c = self.nc_map[u]
      v_c = self.nc_map[v]
      weight = self.G.edge_weight(u, v)
      edge = graph.edge(u_c, v_c)
      if edge:
        edge.weight += weight
      else:
        graph.add_edge(u_c, v_c, weight=weight)
    self.G = graph

  def get_community_vertices(self, nc_map=None):
    if not nc_map:
      nc_map = self.nc_map
    com_vertices = defaultdict(list)
    for n, c in nc_map.items():
      com_vertices[c].append(n)
    return com_vertices

  def modularity(self):
    '''
      compute modularity Q
    '''
    total = 0
    inner_weights = defaultdict(int)
    for u, v in self.G.edges:
      u_c = self.nc_map[u]
      v_c = self.nc_map[v]
      if u_c == v_c:
        if self.G.undirected:
          inner_weights[v_c] += self.G.edge_weight(v, u)*2
        else:
          inner_weights[v_c] += self.G.edge_weight(v, u)
    q = 0
    com_vertices = self.get_community_vertices()
    for c, vertices in com_vertices.items():
      if self.verbose:
        eprint(str(c), same_line=True)
      inner_weight = inner_weights[c]
      total_weight = self.com_edge_weights[c]
      delta_q = inner_weight / self.total_edge_weight - (total_weight / self.total_edge_weight) ** 2 if self.total_edge_weight > 0 else 0
      q += delta_q
      if self.verbose:
        eprint(f'{str(c)} {vertices} {delta_q} {inner_weight} {total_weight}', same_line=False)
    return q

  def calculate_initial_Q(self):
      q = 0.0
      for n in self.G.vertices:
        q += - (self.total_vertex_edge_weights[n] / self.total_edge_weight)**2
      return q

  def calculate_delta_Q(self, n, old_c, c, old_weight, weight):
      t_i = self.total_vertex_edge_weights[n]
      return (weight-old_weight) / self.total_edge_weight - \
              2 * t_i ** 2 / self.total_edge_weight ** 2 + \
              2 * (self.com_edge_weights[old_c] - self.com_edge_weights[c]) * t_i / self.total_edge_weight ** 2

  def find_better_community(self, n):
      c = self.nc_map[n]
      nb_com_weights = self.get_nb_com_weights(n)
      w = nb_com_weights.get(c, 0)
      for new_c, new_w in nb_com_weights.items():
        if new_c == c:
          # skip its' own community
          continue
        delta_Q = self.calculate_delta_Q(n, c, new_c, w, new_w)
        if delta_Q > 0:
          return c, new_c, delta_Q
      return c, c, 0