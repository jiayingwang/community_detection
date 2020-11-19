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
        self.total_edge_weight = self.G.total_edge_weight()
        if self.verbose:
            eprint(f'nodes: {len(self.G.nodes)}')
        if coms:
            for c, nodes in enumerate(coms):
                for n in nodes:
                    self.nc_map[n] = c
                    self.com_edge_weights[c] += self.G.total_edge_weight(n)
        else:
            for c, n in enumerate(self.G.nodes):
                self.nc_map[n] = c
                self.com_edge_weights[c] = self.G.total_edge_weight(n)
            
    def remove(self, n, c):
        '''
            remove a node n from community c
        '''
        self.nc_map[n] = None
        self.com_edge_weights[c] -= self.G.total_edge_weight(n)
        
    def insert(self, n, c):
        '''
            add a node n into community c
        '''
        self.nc_map[n] = c
        self.com_edge_weights[c] += self.G.total_edge_weight(n)
    
    def get_nb_com_weights(self, n):
        '''
            find a node n's neighbor communities and sum of edge weights
            a neighbor community can be the community contains n
        '''
        nb_coms = defaultdict(int)
        n_c = self.nc_map[n]
        for u in self.G.neighbors(n):
            if u != n:
                u_c = self.nc_map[u]
                nb_coms[u_c] += self.G.edge_weight(n, u) + self.G.edge_weight(u, n)
        return nb_coms
    
    def get_communities(self, mode='current'):
        '''
            get communities (a list of nodes)
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
        nc_map = {n: n for n in self.origin_G.nodes}
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
            create a new graph to merge communities to nodes
        '''
        graph = Graph()
        for u, v, w in self.G.edge_weights:
            u_c = self.nc_map[u]
            v_c = self.nc_map[v]
            weight = w
            if graph.has_edge(u_c, v_c):
                weight += graph.edge_weight(u_c, v_c)
            graph.add_edge(u_c, v_c, weight)
        self.G = graph
    
    def get_community_nodes(self, nc_map=None):
        if not nc_map:
            nc_map = self.nc_map
        com_nodes = defaultdict(list)
        for n, c in nc_map.items():
            com_nodes[c].append(n)
        return com_nodes
    
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
                if self.G._symmetric:
                    inner_weights[u_c] += self.G.edge_weight(u, v)*2
                else:
                    inner_weights[u_c] += self.G.edge_weight(u, v)
        q = 0
        com_nodes = self.get_community_nodes()
        for c, nodes in com_nodes.items():
            eprint(str(c), same_line=True)
            inner_weight = inner_weights[c]
            total_weight = self.com_edge_weights[c]
            q += inner_weight / self.total_edge_weight - (total_weight / self.total_edge_weight) ** 2
        return q
    
    def calculate_initial_Q(self):
        q = 0
        for n in self.G.nodes:
            q += - (self.G.total_edge_weight(n) / self.total_edge_weight)**2
        return q
    
    def calculate_delta_Q(self, n, old_c, c, old_weight, weight):
        t_i = self.G.total_edge_weight(n)
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
            for n in self.com_utils.G.nodes:
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
        com_utils = CommunityUtility(G)
        com_utils.init_stats(coms)
        return float(f'{com_utils.modularity():.4f}')