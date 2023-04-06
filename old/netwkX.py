import networkx as nx, numpy as np, pandas as pd

corMat = [
    [0.3, -0.4, 0.02, 0.07],
    [-0.4, .11, 0.09, 0.6],
    [0.02, 0.09, 0.8, 0.99],
    [0.07, 0.6, 0.99, -0.5]
]

lbls = ['audi', 'cngo', 'cngp', 'dflt']

df = pd.DataFrame(corMat, columns=lbls, index=lbls)

npArr = np.array(corMat)

print(df)

