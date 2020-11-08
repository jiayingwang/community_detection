# Introduction

The community-detection module contains basic functions for find communities in a graph. Internally, community-detection uses [simple-graph](https://github.com/jiayingwang/simple_graph) to hold the structure of a graph.

# Install
```python
pip install community-detection
```
or update
```python
pip install --upgrade community-detection
```

# Usage
```python
from simple_graph import Graph
from community_detection import FastUnfolding
G = Graph({0: [1, 2], 1: [2]})
fu = FastUnfolding()
communities = fu.process(G)
Q = fu.modularity(G, communities)
print(communities)
print('Q:', Q)
```
```shell
ouput: 
[[0, 1, 2]]
Q: 0.0
```

# License

community-detection is a free software. See the file LICENSE for the full text.

# Authors

![qrcode_for_wechat_official_account](https://wx3.sinaimg.cn/mw1024/bdb7558bly1gjo23b3jrmj207607674r.jpg)

