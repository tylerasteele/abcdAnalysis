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

        # Convert the Graph to a DiGraph
        H = G.to_directed()

        # Calculate the weighted degree centrality
        centrality = nx.degree_centrality(H)

        stats[id][scan] = {
            #### Per Node ####
            'degreeCentrality': centrality,

            # Other centrality measures...
        }
