import random
from collections import defaultdict
from elegant_io import eprint

'''
  paper: <Near linear time algorithm to detect community structures in large-scale networks>
'''

class LPA():
  
  def __init__(self, verbose=False):
    self._verbose = verbose
    
  def process(self, G, max_iter=100):
    self._G = G
    self._n = len(self._G.vertices)
    self._max_iter = max_iter
    
    for i in self._G.vertices:
      self._G.vertex(i).label = i
    iter_time = 0

    while(not self.can_stop() and iter_time < self._max_iter):
      self.update_label()
      iter_time += 1
    return self.get_communities()

  def can_stop(self):
    for i in self._G.vertices:
      label = self._G.vertex(i).label
      max_labels = self.get_max_neighbor_label(i)
      if(max_labels and label not in max_labels):
        return False
    return True

  def get_max_neighbor_label(self, u):
    if not self._G.degree(u):
      return []
    label_count = defaultdict(int)
    for v in self._G.neighbors(u):
      label_count[self._G.vertex(v).label] += 1
    max_count = max(label_count.values())
    return [label for label, count in label_count.items() if count == max_count]

  def update_label(self):
    visit_sequence = random.sample(self._G.vertices, len(self._G.vertices))
    for i in visit_sequence:
      u = self._G.vertex(i)
      label = u.label
      max_labels = self.get_max_neighbor_label(i)
      if(max_labels and label not in max_labels):
        u.label = random.choice(max_labels)
  
  def get_communities(self):
    communities = defaultdict(list)

    for i in self._G.vertices:
      communities[self._G.vertex(i).label].append(i)
    return list(communities.values())
  
  def __repr__(self):
    return 'LPA'
