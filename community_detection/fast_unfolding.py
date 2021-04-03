from elegant_io import eprint
from .community_utility import CommunityUtility

'''
  paper: <Fast unfolding of communities in large networks>
'''

class FastUnfolding:

  def __init__(self, verbose=False):
    self.verbose = verbose

  def process(self, G):
    self.G = G
    self.finished = False
    self.step = 0
    self.com_utils = CommunityUtility(self.G, verbose=self.verbose)
    while not self.finished:
      self.one_step()
    if self.verbose:
      eprint('Done')
    return self.com_utils.get_communities(mode='final')

  def one_step(self):
    '''
      one step of fast unfolding (2 stages)
      1 move each node to a neighbor community to increase modularity
      until no more moves
      2 create a new graph to merge community to node
    '''
    self.step += 1
    if self.verbose:
      eprint(f"step: {self.step}")
    modified = False
    improved = True
    # stage 1
    self.com_utils.init_stats()
    if self.verbose:
      Q = self.com_utils.calculate_initial_Q()
      eprint(f'Q: {Q:.4}', same_line=True)

    while improved:
      improved = False
      for n in self.com_utils.G.vertices:
        old_c, new_c, delta_Q = self.com_utils.find_better_community(n)
        if old_c != new_c:
          self.com_utils.remove(n, old_c)
          self.com_utils.insert(n, new_c)
          improved = True
          modified = True
          if self.verbose:
            Q += delta_Q
            eprint(f'Q: {Q:.4} by change community ({old_c} -> {new_c}) of node {n}', same_line=True)

    # stage 2
    if modified:
      self.com_utils.relabel_nc_map()
      self.com_utils.add_history()
      self.com_utils.rebuild_graph()

    else:
      self.finished = True

  def modularity(self, G, coms):
    com_utils = CommunityUtility(G, verbose=self.verbose)
    com_utils.init_stats(coms)
    return float(f'{com_utils.modularity():.4f}')

  def __repr__(self):
    return 'Fast Unfolding'