import pickle, os, networkx as nx, numpy as np, matplotlib.pyplot as plt, math

ids = ['NDAR_INVZKP2G8H4', 'NDAR_INVNVZ6Y707']
scans = ['2year', 'baseline']
cM = {0: 'audi', 1: 'cngo', 2: 'cngp', 3: 'dflt', 4: 'dsla', 5: 'fntp', 6: 'none', 7: 
      'rstn', 8: 'smhn', 9: 'smmn', 10: 'saln', 11: 'vtan', 12: 'visn', 13: 'crcxlh', 14: 'thplh', 15: 
      'cdelh', 16: 'ptlh', 17: 'pllh', 18: 'bs', 19: 'hplh', 20: 'aglh', 21: 'aalh', 22: 'vtdclh', 23: 
      'crcxrh', 24: 'thprh', 25: 'cderh', 26: 'ptrh', 27: 'plrh', 28: 'hprh', 29: 'agrh', 30: 'aarh', 31: 'vtdcrh'}



os.chdir('../working')

with open('data.pickle', 'rb') as file:
    patients = pickle.load(file)


missingData = {}
stats = {}

for id in ids:
    stats[id] = {'quintile': patients[id]['quintile']}
    for scan in scans:
        G = nx.Graph()
        tabularTrck = 0
  
        matrix = [[float('nan') for j in range(32)] for i in range(32)]

        for i, row in enumerate(patients[id][scan]):
            for j, weight in enumerate(row):
                if weight != weight:
                    continue
                elif weight == '':
                    missingData[id] = {'missingDataPoints': (missingData.get(id, {}).get('missingDataPoints', 0)) + 1,
                                       'indices': (missingData.get(id, {}).get('indices', [])) + [tabularTrck]}
                else:
                    G.add_edge(cM[i], cM[j], weight=float(weight))
                    matrix[i][j] = float(weight)

                tabularTrck += 1

        for u, v, data in G.edges(data=True):
            print(f"Weight of edge ({u}, {v}): {data['weight']}")            

            
        stats[id][scan] = {


            #### Per Node ####
            'degreeCentrality': nx.degree_centrality(G, weight='weight'),
            'betweennessCentrality': nx.betweenness_centrality(G, weight='weight'),
            'edgeBetweennessCentrality': nx.edge_betweenness_centrality(G, weight='weight'),
        
            

            #### Per Graph #### 
            #### Between Graphs ####
        
            #### Testing ####
            'eigenvectorCentrality': nx.eigenvector_centrality_numpy(G, weight='weight'),
            'katzCentrality': nx.katz_centrality_numpy(G, weight='weight'),
            'nodeStrengthCentrality': {node: sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]) for node in G.nodes()},
            #'closenessCentrality': nx.closeness_centrality(G, distance='weight') # Requries positive numbers
            #'averageClustering': nx.smallworld(G, weight='weight')
            #'allPairsNodeConnectivity': nx.all_pair
            }


print(stats['NDAR_INVZKP2G8H4']['2year']['degreeCentrality'])

"""
Per Node
degree centrality
betweenness centrality
edge_betweenness_centrality

Per graph
strong connectivity
weak connectivity
small worldiness
Average clustering
All pairs node connectivity

Between graphs
graph_edit_distance
simrank_similarity
Modularity
louvain_communities
Per module
betweenness centrality subset
edge_betweenness_centrality subset"""

    # Degree centrality: the number of edges connected to a node
    # Betweenness centrality: the extent to which a node is a bridge between other nodes
    # Closeness centrality: the inverse of the sum of shortest path distances from a node to all other nodes in the network
    # Clustering coefficient: the proportion of a node's neighbors that are also neighbors of each other
    # Network modularity: the degree to which a network can be divided into smaller groups or modules with high internal connectivity and low external connectivity
    # Community detection algorithms: methods for identifying groups of nodes with similar connectivity patterns
    # Network resilience: the ability of a network to maintain its function despite disruptions or damage


