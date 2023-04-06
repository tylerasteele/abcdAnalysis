import pickle, os, networkx as nx, numpy as np, matplotlib.pyplot as plt, math, community


cM = {0: 'audi', 1: 'cngo', 2: 'cngp', 3: 'dflt', 4: 'dsla', 5: 'fntp', 6: 'none', 7: 
      'rstn', 8: 'smhn', 9: 'smmn', 10: 'saln', 11: 'vtan', 12: 'visn', 13: 'crcxlh', 14: 'thplh', 15: 
      'cdelh', 16: 'ptlh', 17: 'pllh', 18: 'bs', 19: 'hplh', 20: 'aglh', 21: 'aalh', 22: 'vtdclh', 23: 
      'crcxrh', 24: 'thprh', 25: 'cderh', 26: 'ptrh', 27: 'plrh', 28: 'hprh', 29: 'agrh', 30: 'aarh', 31: 'vtdcrh'}


# matplotlib.use('Agg')
os.chdir('../working')

with open('data.pickle', 'rb') as file:
    patients = pickle.load(file)

### Test for blanks ###
# for id in patients:
#     for scan in ['baseline', '2year']:
#         blanks = 0
#         for i in patients[id][scan]:
#             for j in i:
#                 if j == '':
#                     blanks+=1
#                     print(id, blanks)

### Patients ###
# Full patient example: 
# Many missing (1 at 183 ''s): NDAR_INV9CR0L7A7 
# Few missing(Rest at 64 ''s): NDAR_INVNVZ6Y707, NDAR_INVA25H3MCK, NDAR_INV8YPT1XL0, NDAR_INV2T7FRKV1
# stats, missingData = {}, {}
# for id in patients:
#     stats[id] = { 'quintile': patients[id]['quintile'] }
#     for scan in ['2year', 'baseline']:
#         G = nx.Graph(); tabularTrck = 0
#         for i, row in enumerate(patients[id][scan]):
#             for j, weight in enumerate(row):
#                 if weight != weight: continue
#                 elif weight == '': missingData[id] = {'missingDataPoints': (missingData.get(id, {}).get('missingDataPoints', 0)) + 1, 'indices': (missingData.get(id, {}).get('indices', [])) + [tabularTrck]}
#                 else: G.add_edge(cM[i], cM[j], weight = float(weight))
#                 tabularTrck+=1

#         # Per node measurements
#         # stats[id]['degreeCentrality'], stats[id]['betweennessCentrality'], stats[id]['edgeBetCentrality'] = nx.degree_centrality(G), nx.betweenness_centrality(G), nx.edge_betweenness_centrality(G)





ids = ['NDAR_INVZKP2G8H4', 'NDAR_INVNVZ6Y707']; scan = 'baseline'; missingData = {}; stats = {}
for id in ids:
    stats[id] = { 'quintile': patients[id]['quintile'] }
    stats[id]['2year'], stats[id]['baseline'] = {}, {}
    for scan in ['2year', 'baseline']:
        G = nx.Graph(); tabularTrck = 0; arrayBuilder = []

        matrix = [[float('nan') for j in range(32)] for i in range(32)]

        for i, row in enumerate(patients[id][scan]):


            for j, weight in enumerate(row):
                if weight != weight: continue
                elif weight == '': missingData[id] = {'missingDataPoints': (missingData.get(id, {}).get('missingDataPoints', 0)) + 1, 'indices': (missingData.get(id, {}).get('indices', [])) + [tabularTrck]}

                
                else: 
                    G.add_edge(cM[i], cM[j], weight = float(weight))
                    matrix[i][j] = float(weight)

                tabularTrck+=1
        stats[id][scan]['degreeCentrality'] = nx.degree_centrality(G) # I don't believe this is useful
        stats[id][scan]['eigenvectorCentrality'] = nx.eigenvector_centrality_numpy(G, weight='weight')              #Lanczos algorithm as eig alternate?
        stats[id][scan]['katzCentrality'] = nx.katz_centrality_numpy(G, weight='weight')
        stats[id][scan]['edgeBetweennessCentrality'] = nx.edge_betweenness_centrality(G, weight='weight')
        stats[id][scan] = { 'nodeStrengthCentrality' : {node: sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]) for node in G.nodes()} }



print(stats['NDAR_INVZKP2G8H4']['2year'])


        ### Node Level ###
        #stats[id]['degreeCentrality'] = nx.degree_centrality(G) # I don't believe this is useful
        #stats[id]['betweennessCentrality'] = nx.betweenness_centrality(G, weight='weight')
        #stats[id]['edgeBetCentrality'] = nx.edge_betweenness_centrality(G, weight='weight')

        # print(stats, '\n\n')

        ### Graph Level ###
        ### Between Graphs Level ###


        # n1 = {}
        # for node in G.nodes():
        #     n1[node] = sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)])



        # n2 = {node: sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]) for node in G.nodes()}


        #n3 = {node: sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]) for node in G.nodes()}
        


        # Bing
        # n4 = {node: sum([G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]) for node in G.nodes()}
        # stats[id]['strengthCentrality'] = n4






        ############# Testing #############      # I think weighted degree centrality will be more useful for a correlation matrix
        #stats[id]['weightedDegreeCentrality'] = nx.degree_centrality(G)                                  ### WEIGHTED DEGREE CENTRALITY
        #stats[id]['strengthCentrality'] = nx.algorithms.centrality.strength_centrality(G)                ### STRENGTH CENTRALITY





        #stats[id]['pagerankCentrality'] = nx.pagerank(G, weight='weight', tol=0.001)
        #stats[id]['closenessCentrality'] = nx.closeness_centrality(G, distance='weight')
        #stats[id]['clusteringCoefficient'] = nx.average_clustering(G, weight='weight')
        # stats[id]['shortestPaths'] = []
        
        # for v in G.nodes():
        #     shortest_paths = nx.single_source_dijkstra_path(G, v, weight='weight')
        #     for key in shortest_paths:
        #         shortest_paths[key] = len(shortest_paths[key]) - 1
        #     stats[id]['shortestPaths'].append(shortest_paths)


        # pagerank nx.pagerank(G, alpha=0.85)

        #stats[id]['clusteringCoefficient'] = nx.clustering(G, weight='weight')

# print(stats)        












# NDAR_INV8HX2TBDP
# print(G.edges(data=True))


# avgClustering = nx.average_clustering(G)
# allPairsNodeCntvy = nx.all_pairs_node_connectivity(G)
# graph_edit_distance = nx.optimize_graph_edit_distance(G, G)

# Per graph
# strongConnectivity = nx.is_strongly_connected(G) - Not measureable in +
# weakConnectivity = nx.is_weakly_connected(G)
# smallWorldness = nx.algorithms.smallworld.sigma(G)
# smallWorldness = nx.smallworld(G)
# avgClustering = nx.average_clustering(G)

# Between graphs
#graph_edit_distance
#simrank_similarity
#Modularity
#louvain_communities
#Per module
#betweenness centrality subset
#edge_betweenness_centrality subset






# degree_centrality = nx.degree_centrality(G)
# betweenness_centrality = nx.betweenness_centrality(G)
# edge_betweenness_centrality = nx.edge_betweenness_centrality(G)

# # Step 3: Calculate per-graph measures
# strongly_connected = nx.is_strongly_connected(G)
# weakly_connected = nx.is_weakly_connected(G)
# small_worldness = nx.algorithms.smallworld.sigma(G)
# avg_clustering = nx.average_clustering(G)0-=0
# all_pairs_node_connectivity = nx.all_pairs_node_connectivity(G)

# # Step 4: Calculate between-graph measures
# other_graphs = {}  # Dictionary of other graphs to compare with G
# graph_edit_distance = nx.algorithms.similarity.graph_edit_distance(G, other_graphs)
# simrank_similarity = nx.algorithms.similarity.simrank_similarity(G, other_graphs)
# modularity = nx.algorithms.community.modularity(G, [c for c in nx.algorithms.community.greedy_modularity_communities(G)])
# louvain_communities = nx.algorithms.community.modularity(G, [c for c in nx.algorithms.community.greedy_modularity_communities(G)])
# for c in louvain_communities:
#     for node in c:
#         G.nodes[node]['community'] = c
# betweenness_centrality_subset = nx.betweenness_centrality(G, subset=louvain_communities[0])
# edge_betweenness_centrality_subset = nx.edge_betweenness_centrality(G, subset=louvain_communities[0])









# for id in patients:

#     for scan in ['baseline', '2year']:


#         G = nx.Graph()

#         for i, row in enumerate(patients[id][scan]):
#             for j, weight in enumerate(row):
#                 if i != j:  # Exclude self-loops (correlations with itself)
#                     G.add_edge(i, j, weight=weight)

#         print(G.edges(data=True))

#         patients[id]['graph' + scan] = G



# G=nx.Graph()
# for i, row in enumerate(patients['NDAR_INVRNG7B964']['baseline']):
#     for j, weight in enumerate(row):
#         G.add_edge(cM[i], cM[j], weight=weight)

# print(G.edges(data=True))


# # print edges
# print("Edges:")
# for u, v, weight in G.edges.data('weight'):
#     print(f"({u}, {v}, {weight})")


# print(patients)


# Create a graph from the correlation matrix


# Draw the graph
 #Draw the graph











# print(patients['NDAR_INVVM3YZHHG'])