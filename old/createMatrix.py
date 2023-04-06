import os, pandas as pd, json, time
start = time.perf_counter()

equating = {
    'au': 'audi','ad': 'audi','cgc': 'cngo','cerc': 'cngo','ca': 'cngp','copa': 'cngp','dt': 'dflt',
    'df': 'dflt','dla': 'dsla','dsa': 'dsla','fo': 'fntp','fopa': 'fntp','n': 'none','none': 'none',
    'rspltp': 'rstn','rst': 'rstn','smh': 'smhn','smm': 'smmn','sa': 'saln','vta': 'vtan', 'vs': 'visn',
}

os.chdir('../data')

# Full files 
b = 'b.csv'
r = 'r.csv'

# Limited testing files
testCor = 'testCor.csv'
testBet = 'testBet.csv'

lines = []; lineID = []
with open (b, 'r') as betnet, open (r, 'r') as rscor:
    code = betnet.readline().strip().split(',')[22:-2] + rscor.readline().strip().split(',')[22:-2] # Encoded labels
    english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',') # Plain english translation

    for line1, line2 in zip(betnet, rscor): # INPUT FILES MUST BE SORTED BY: "rsfmri_c_ngd_visitid"	
        line1 = line1.strip().split(',')[22:-2]
        line2 = line2.strip().split(',')

        ## Extract any additional data here
        id = line2[3]
        study = line2[9]
        line2 = line2[22:-2]

        lines.append(line1 + line2)
        lineID.append(id)


psn  = dict(); pos = {}; index = 0 
for id in lineID:
    indices = [i for i in range(len(lineID)) if lineID[i] == id]
    if len(indices) > 1:
        psn[id] = indices
        pos[index] = lineID[index]
    index += 1



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


patients = dict()
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


    if id not in patients: patients[id] = {'baseline': [], '2year': []}

    # If we are in the second scan, set it to the first (2year alphabetically comes before baseline)
    if int(line) > int(psn[id][0]): patients[id]['baseline'] = corMatrix
    else: patients[id]['2year'] = corMatrix

for pnt in patients:
    for scan in patients[pnt]: 
        patients[pnt][scan] = patients[pnt][scan]#.to_dict()


# print('CreateMatrix complete. Length: ', len(patients))

# os.chdir('../working')
# with open ('output.txt', 'w') as file:
#     json.dump(patients, file, indent = 4)

# end = time.perf_counter()
# print('Time: ', end - start, 'seconds') # Runtime: Runtime: 1521.1622371570002 seconds, 1431.9932293459997 seconds

# for i in patients:
#     print(i)




#### PICKLE FILE? ####









## Next Steps:




"""

Patients -> Graph Object -> How do you know which patients
Every matrix becomes a graph 


Basline: Q1, Q2, Q3, Q4
2 Year: Q1, Q2, Q3, Q4

Gen graphs: Betweeness centrality
Each graph has betweeness centrality

Does it change over time 

Repeated measures ANOVA 

Export to R?
Scikit for ANOVA

Ways to compare correlation matrices are betweenness centrality, etc.

What is tons of stuff?

Run ML algs, predict what there brain looks like, 
behavioral resting state associated studies, correlate correlation matrices with behavioral measure like anxiety

Predict HBA1C: Connectome predictive modeling 
 - Could predict BMI 
 - Todd Constable: Predict BMI in adults 
 - Emily Finn 

 - Compare RS to task data 


 - Simplest Machine Learning Alg Project: Classification, can we predict a group
 - Forward analysis and backwards analysis measure -> groups, grous -> measures 
 - Training dataset and test dataset 
 - SciKitLearn for ML 

 - 
 - 
 - LAB MEETING MONDAY: GIVE DESCRIPTION OF WHAT I'VE DONE, NEXT STEPS


 - Colleague at CU Denver: 1hr RS, hyperglyemic clamp 
 - Calculate synchroncity between brain 
 - GH: Insulin Brain: Waveforms
 - Descriptive tie in, patterns emerge, 
 

"""








