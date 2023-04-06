import os, pandas as pd, json

equating = {
    'au': 'audi',
    'ad': 'audi',
    'cgc': 'cngo',
    'cerc': 'cngo',
    'ca': 'cngp',
    'copa': 'cngp',
    'dt': 'dflt',
    'df': 'dflt',
    'dla': 'dsla',
    'dsa': 'dsla',
    'fo': 'fntp',
    'fopa': 'fntp',
    'n': 'none',
    'none': 'none', 
    'rspltp': 'rstn',
    'rst': 'rstn',
    'smh': 'smhn',
    # Equal in both
    'smm': 'smmn',
    # Equal in both
    'sa': 'saln',
    # Equal in both
    'vta': 'vtan', 
    # Equal in both
    'vs': 'visn',
    # Equal in both
}

os.chdir('../data')

# Limited testing files
testCor = 'testCor.csv'
testBet = 'testBet.csv'

# Lines will be data only, ptScans = {'pt1': ['1scan', '2scan']}, idByLine = [id1, id2, id3]
lines = []; ptScans = {}; idByLine = []
with open (testBet, 'r') as betnet, open (testCor, 'r') as rscor:
    betHeader = betnet.readline().strip().split(','); rsHeader = rscor.readline().strip().split(',')
    code = betHeader[22:-2] + rsHeader[22:-2]
    english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',')
    for line1, line2 in zip(betnet, rscor):
        line1 = line1.strip().split(',')[22:-2]
        line2 = line2.strip().split(',')

        ## Extract any additional data here
        id = line2[3]
        study = line2[9]
        line2 = line2[22:-2]

        lines.append(line1 + line2)

        # Track number of fMRIs
        if id not in ptScans: ptScans[id] = [study]
        else: ptScans[id].append(study)
        idByLine.append(id)



print(idByLine)

# Attach integers to IDs, if there is more than one scan
pos = {}; locs = {}
for i in range(len(idByLine)):
    if idByLine.count(idByLine[i]) > 1:
        pos[i] = idByLine[i]

        element = idByLine[i]
        indices = [i for i in range(len(idByLine)) if idByLine[i] == element]
        locs[idByLine[i]] = indices


print(pos)
print(locs)

# Tabular data containing only those who completed
df = pd.DataFrame(columns=code, index=[str(p) + ' ' + str(pos[p]) for p in pos])
for i in pos:
    index = 0 
    for key in df:
        df.loc[str(i) + ' ' + pos[i], key] = lines[i][index]
        index += 1

# Labels for correlation matrices
lbls = []
for lbl in df:
    if '_c_' in lbl: 
        if equating[lbl.split('_')[-1]] not in lbls: lbls.append(equating[lbl.split('_')[-1]])
    else: 
        if lbl.split('_')[-1] not in lbls: lbls.append(lbl.split('_')[-1])



for pt in df.iterrows():
    line = pt[0].split(' ')[0]
    id = pt[0].split(' ')[1]

    # Correlations: (first, second) = correlation
    correlations = dict()
    for key in df:

        # If network to network 
        if '_c_' in key:
            correlations[equating[key.split('_ngd_')[1]], equating[key.split('_ngd_')[2]]] = df.loc[pt[0], key]

        # If network to anatomy
        else:
            correlations[equating[key.split('_')[3]], key.split('_')[-1]] = df.loc[pt[0], key]

    corMatrix = pd.DataFrame(columns=lbls, index=lbls)

    # Mirror the matrix
    for cor in correlations:
        corMatrix.loc[cor[0], cor[1]] = correlations[cor]
        corMatrix.loc[cor[1], cor[0]] = correlations[cor]


        

