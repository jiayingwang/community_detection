import random 
from collections import defaultdict
from elegant_io import eprint

'''
  paper: <Mixture models and exploratory analysis in networks>
'''

class EM():

  def __init__(self, verbose=False):
    self._verbose = verbose

  def e_step(self, q):
    for i in self._G.vertices:
      # q[i][r] is prob of vertex i belong to community g
      q[i] = []
      norm = 0.0
      for g in range(self._k):
        # pi[g] is the prob of g
        x = self._pi[g]
        for j in self._G.neighbors(i):
          x *= self._theta[g][j]
        q[i].append(x)
        norm += x
      if norm:
        for g in range(self._k):
          q[i][g] /= norm
      else:
        # if there are no output link, i should be equal prob for each group
        for g in range(self._k):
          q[i][g] = 1/self._k

  def m_step(self, q):
    for g in range(self._k):
      sum1 = 0.0
      sum3 = 0.0
      for i in self._G.vertices:
        sum1 += q[i][g]
        sum2 = 0.0
        for j in self._G.neighbors(i):
          sum2 += q[j][g]
        self._theta[g][i] = sum2  # update theta
        sum3 += q[i][g]*self._G.degree(i)
      self._pi[g] = sum1/self._n  # update pi
      if sum3:
        for i in self._G.vertices:
          self._theta[g][i] /= sum3 # norm
      else:
        for i in self._G.vertices:
          self._theta[g][i] = 1/self._n

  def process(self, G, k, max_iter = 100):
    '''
      G: graph
      k: want to get k communities
    '''
    self._G = G
    self._n = len(self._G.vertices)
    self._k = k
    self._pi = {}
    self._theta = []
    self._max_iter = max_iter
    # initial pi
    X = [1.0+random.random() for i in range(self._k)]
    norm = sum(X)
    self._pi = [x/norm for x in X]

    # initial theta
    for i in range(self._k):
      Y = {j:1.0+random.random() for j in self._G.vertices}
      norm = sum(Y.values())
      self._theta.append({y:Y[y]/norm for y in Y})

    # iteration to refine q
    q_old = {}
    for iter_time in range(self._max_iter):
      q = {}
      # E-step
      self.e_step(q)
      # M-step
      self.m_step(q)

      # early terminate
      if(iter_time != 0):
        deltasq = 0.0
        for i in self._G.vertices:
          for g in range(self._k):
            deltasq += (q_old[i][g]-q[i][g])**2
        if self._verbose:
          eprint(f'delta: {deltasq}', same_line=True)
        if(deltasq < 0.05):
          break

      # update q_old
      q_old = {}
      for i in self._G.vertices:
        q_old[i] = []
        for g in range(self._k):
          q_old[i].append(q[i][g])

    # compute communites
    communities = defaultdict(list)
    for i in self._G.vertices:
      c_id = 0
      cur_max = q[i][0]
      for j in range(1,self._k):
        if q[i][j] > cur_max:
          cur_max = q[i][j]
          c_id = j
      communities[c_id].append(i)
    return list(communities.values())
  
  def __repr__(self):
    return 'EM'