import random
import networkx as nx
import collections


class LPA():
    def __init__(self,G,max_iter=20):
        self.G = G
        self.n = len(G.nodes)
        self.max_iter = max_iter

    def deal_node(self):
        for i in range(self.n):
            self.G.nodes[i]['label'] = i
        iter_time = 0

        while(not self.scan_stop() and iter_time<self.max_iter ):
            self.update_label()
            iter_time += 1
        return self.get_communities()

    def scan_stop(self):
        for i in range(self.n):
            node = self.G.nodes[i]
            label = node['label']
            max_label = self.get_max_neighbor_label(i)
            if(label not in max_label):
                return False
        return True

    def get_max_neighbor_label(self,node_index):
        m = collections.defaultdict(int)
        for neighbor_index in self.G.neighbors(node_index):
            neighbor_label = self.G.nodes[neighbor_index]['label']
            m[neighbor_label] += 1
        max_v = max(m.values())
        return [item[0] for item in m.items() if item[1] == max_v]
    def update_label(self):
        visit_sequence = random.sample(self.G.nodes(),len(self.G.nodes))

        for i in visit_sequence:
            node = self.G.nodes[i]
            label = node['label']
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                newlabels = random.choice(max_labels)
                node['label'] = newlabels
    def get_communities(self):
        communities = collections.defaultdict(lambda :list())

        for node in self.G.nodes(True):
            label = node[1]['label']
            communities[label].append(node[0])
        return communities.values()
if __name__ == "__main__":
    G = nx.Graph({0:[1,2],1:[2]})

    algorithm = LPA(G)
    communities = algorithm.deal_node()
    for communities in communities:
        print(communities)
