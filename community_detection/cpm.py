import numpy as np
import networkx as nx
def get_percolated_cliques(G, k):
    cliques = list(frozenset(c) for c in nx.find_cliques(G) if len(c) >= k)  # 找出所有大于k的最大k-派系
    matrix = np.zeros((len(cliques), len(cliques)))  # 构造全0的重叠矩阵
    for i in range(len(cliques)):
        for j in range(len(cliques)):
            if i == j:  # 将对角线值大于等于k的值设为1，否则设0
                n = len(cliques[i])
                if n >= k:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
            else:  # 将非对角线值大于等于k-1的值设为1，否则设0
                n = len(cliques[i].intersection(cliques[j]))
                #intersection:返回两个集合中都包含的元素
                if n >= k - 1:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0

    l = list(range(len(cliques))) # l（社区号）用来记录每个派系的连接情况，连接的话值相同
    k = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1 and i != j:
                # 矩阵值等于1代表，行派系与列派系相连，让l中的行列派系社区号变一致
                l[j] = l[i]
                # print(l)
                # 让列派系与行派系社区号相同（划分为一个社区）
    q = []
    for i in l:
        if i not in q:  # 每个社区号只取一次
            q.append(i)
    for i in q:
        print(frozenset.union(*[cliques[j] for j in range(len(l)) if l[j] == i]))  # 每个派系的节点取并集获得社区节点
if __name__ == '__main__':
    G = nx.read_gml("E:/python\dolphins.gml", label="id")
    p = get_percolated_cliques(G,4)