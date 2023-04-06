import os, pandas as pd, json

os.chdir('../data')

# ABCD rsfMRI and blood data files
cor02 = 'mrirscor02.txt'
ybd01 = 'abcd_ybd01.txt'
bet02 = 'abcd_betnet02.txt'

# Limited testing files
testCor = 'testCor.txt'
testBet = 'testBet.txt'


# Readlines in file
lines = []; ptScans = {}; i = 0;
with open (testBet, 'r') as file:
    for line in file:
        line = line.strip().split('\t')
        lines.append(line)

        # Track number of scans for each patient: baseline/2year
        if i > 1:
            if line[3][1:-1] not in ptScans: ptScans[line[3][1:-1]] = [line[9][1:-1]]
            else: ptScans[line[3][1:-1]].append(line[9][1:-1])
        i+=1

# Remove and store plain english row 
english = lines[1]
lines.remove(lines[1])

# Get headers and data in the form of {'header1': [patient1, patient2, patient3], 'correlation1': [corr1, corr2, corr3]}
headers = []; data = {}
for i in range(len(lines[0])):
    col = []
    for j in range(1, len(lines)):
        col.append(lines[j][i][1:-1])
    data[lines[0][i][1:-1]] = col
    headers.append(lines[0][i][1:-1])

# Create data frame with pretty labels, where index 0 is the first patient
df = pd.DataFrame(data)

# Headers containing a correlation matrix
abrCorrelations = headers[22:-2]
engCorrelations = english[22:-2]

# mtxLabels = ['ad', 'vs'] # list of abbreviated networks
# codeToEng = {'ad': 'auditory network', 'vs': 'visual network'} # dictionary showing conversion from abbreviated to plain english networks
# allCorr = {'rsfmri_c_ngd_ad_ngd_vs': '"Average correlation between auditory network and visual network"', 'rsfmri_c_ngd_vs_ngd_ad': '"Average correlation between visual network and auditory network"'} # dictionary showing conversion from abbreviated to plain english correlations
mtxLabels = []; codeToEng = dict(); allCorr = dict()
for i in range(0, len(engCorrelations), 1):
    if i % 13 == 0:         
        code =  abrCorrelations[i].split('_ngd_')[1];
        engNetwork = ' '.join(engCorrelations[i].split('and')[0].split(' ')[3:-1])
        mtxLabels.append(code)
        codeToEng[code] = engNetwork
    allCorr[abrCorrelations[i]] = engCorrelations[i]

patients = {};
for scan in range(len(df)):
    scanData = df.iloc[scan]
    subject = scanData['subjectkey']
    if len(ptScans[subject]) > 1:

        if subject not in patients:
            patients[subject] = {}



        currentScan = scanData['rsfmri_c_ngd_visitid'].split('_')[2]
        patients[subject][currentScan] = pd.DataFrame(index = mtxLabels, columns = mtxLabels)

        correlations = dict() 
        for cor in allCorr:
            splt = cor.split('_ngd_')
            correlations[(splt[1], splt[2])] = df.iloc[scan][cor]

        for cor in correlations:
            patients[subject][currentScan][cor[0]][cor[1]] = correlations[cor]




for patient in patients:
    for scan in patients[patient]:
        patients[patient][scan] = patients[patient][scan].to_dict(orient="records")

os.chdir('../working')

with open('output.json', 'w') as file:
    json.dump(patients, file, indent = 4)