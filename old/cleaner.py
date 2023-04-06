import os, pandas as pd, json, time, numpy as np, pickle 
start = time.perf_counter()

equating = {
    'au': 'audi','ad': 'audi',
    'cgc': 'cngo','cerc': 'cngo',
    'ca': 'cngp','copa': 'cngp',
    'dt': 'dflt', 'df': 'dflt',
    'dla': 'dsla','dsa': 'dsla',
    'fo': 'fntp','fopa': 'fntp',
    'n': 'none','none': 'none',
    'rspltp': 'rstn','rst': 'rstn',
    'smh': 'smhn',
    'smm': 'smmn',
    'sa': 'saln',
    'vta': 'vtan', 
    'vs': 'visn',
}
cM = {
    'audi': 0,
    'cngo': 1,
    'cngp': 2,
    'dflt': 3,
    'dsla': 4,
    'fntp': 5,
    'none': 6,
    'rstn': 7,
    'smhn': 8,
    'smmn': 9,
    'saln': 10,
    'vtan': 11,
    'visn': 12,
    'crcxlh': 13,
    'thplh': 14,
    'cdelh': 15,
    'ptlh': 16,
    'pllh': 17,
    'bs': 18,
    'hplh': 19,
    'aglh': 20,
    'aalh': 21,
    'vtdclh': 22,
    'crcxrh': 23,
    'thprh': 24,
    'cderh': 25,
    'ptrh': 26,
    'plrh': 27,
    'hprh': 28,
    'agrh': 29,
    'aarh': 30,
    'vtdcrh': 31,
}

os.chdir('../data')

# Full files 
b = 'b.csv'; r = 'r.csv'
 
# Limited testing files
testCor = 'testCor.csv'; testBet = 'testBet.csv'

lines = []; lineID = []
with open (b, 'r') as betnet, open (r, 'r') as rscor:
    code = betnet.readline().strip().split(',')[22:-2] + rscor.readline().strip().split(',')[22:-2] # Encoded labels, first line
    english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',') # Plain english translation, second line

    for line1, line2 in zip(betnet, rscor): # INPUT FILES MUST BE SORTED BY: "rsfmri_c_ngd_visitid"	
        lineID.append(id)
        line1 = line1.strip().split(',')[22:-2]
        line2 = line2.strip().split(',')

        ## Extract any additional data here
        id = line2[3]
        study = line2[9]
        line2 = line2[22:-2]

        lines.append(line1 + line2)

# Psn for tracking followup or 2year, pos for tracking lines in the tabular data
psn  = dict(); pos = {}; index = 0 
for id in lineID:
    indices = [i for i in range(len(lineID)) if lineID[i] == id]
    if len(indices) > 1:
        psn[id] = indices
        pos[index] = lineID[index]
    index += 1

# Tabular of all data 
df = pd.DataFrame(columns=code, index=[str(p) + ' ' + str(pos[p]) for p in pos])
for i in pos:
    index = 0 
    for key in df:
        df.loc[str(i) + ' ' + pos[i], key] = lines[i][index]
        index += 1

patients = {}
for scan in df.iterrows():
    id = scan[0].split(' ')[1]; line = scan[0].split(' ')[0]
    matrix = [[0 for j in range(32)] for i in range(32)]

    for key in df:

        # If network to network correlation
        if '_c_' in key:
            i1 = cM[equating[key.split('_ngd_')[1]]]
            i2 = cM[equating[key.split('_ngd_')[2]]]
            val = df.loc[line + ' ' + id, key]

        # If network to anatomy correlation
        else:
            i1 = cM[equating[key.split('_')[3]]]
            i2 = cM[key.split('_')[-1]]
            val = df.loc[line + ' ' + id, key]

        # Mirror the correlation matrix
        matrix[i1][i2] = val
        matrix[i2][i1] = val

    # Logic for assuring scans end up in the right place
    if id not in patients: patients[id] = {"baseline": [], "2year": []}
    if int(line) > int(psn[id][0]): patients[id]['baseline'] = matrix
    else: patients[id]['2year'] = matrix

os.chdir('../working')
end = time.perf_counter()
print("Finished program. Now, writing data... Time: ", end - start)


start = time.perf_counter()
json.dump(patients, open('j.json', 'w'))
end = time.perf_counter()
print('JSON written... Time: ', end - start)

start = time.perf_counter()
with open('p.pickle', 'wb') as p: pickle.dump(patients, p)
end = time.perf_counter()
print('Pickle written... Time: ', end - start)












# 426.39074484400044 seconds, 429.336923492001 seconds, 429.9795402260006 seconds