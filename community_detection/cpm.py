'''
    paper : <Uncovering the overlapping community structure of complex networks in nature and society>
'''

from collections import defaultdict

class CPM:
    
  def __init__(self, verbose=False):
    self._verbose = verbose

  def process(self, G, k=4):
    # find all cliques which size > k
    cliques = [c for c in G.max_cliques if len(c) >= k]
    vid_cid = defaultdict(set)
    for i,c in enumerate(cliques):
      for v in c:
        vid_cid[v].add(i)

    # build clique neighbor
    clique_neighbor = defaultdict(set)
    remained = set()
    for i, c1 in enumerate(cliques):
      remained.add(i)
      s1 = set(c1)
      candidate_neighbors = set()
      for v in c1:
        candidate_neighbors.update(vid_cid[v])
      candidate_neighbors = [x for x in candidate_neighbors if x > i]
      for j in candidate_neighbors:
        c2 = cliques[j]
        s2 = set(c2)
        if len(s1 & s2) >= min(len(s1),len(s2)) -1:
          clique_neighbor[i].add(j)
          clique_neighbor[j].add(i)
    communities = []

    # compute communities
    for i,c in enumerate(cliques):
      if i in remained:
        communities.append(set(c))
        neighbors = list(clique_neighbor[i])
        while len(neighbors) != 0:
          n = neighbors.pop()
          if n in remained:
            communities[-1].update(cliques[n])
            remained.remove(n)
            for nn in clique_neighbor[n]:
              if nn in remained:
                neighbors.append(nn)
    return [list(community) for community in communities]
