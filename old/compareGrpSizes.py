import os, pickle, statistics, itertools, pandas as pd, numpy as np

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
# b = 'b.csv'; r = 'r.csv'
 
# # Limited testing files
# testCor = 'testCor.csv'; testBet = 'testBet.csv'

# patients = {}; validPts = []
# with open (b, 'r') as betnet, open (r, 'r') as rscor:
#     ntwkCode = betnet.readline().strip().split(',')[22:-2]; anatCode = rscor.readline().strip().split(',')[22:-2] # Encoded labels, first line
#     english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',') # Plain english translation, second line

#     for line1, line2 in zip(betnet, rscor): # INPUT FILES MUST BE SORTED BY: "rsfmri_c_ngd_visitid"	
#         matrix = [[0 for j in range(32)] for i in range(32)]
#         line1 = line1.strip().split(',')[22:-2]
#         line2 = line2.strip().split(',')

#         ## Extract any additional data here ##
#         id = line2[3]; study = line2[9].split('_')[-1]
#         line2 = line2[22:-2]

#         # Network to network correlations 
#         for i in range(len(line1)):
#             (junk, i1, i2) = ntwkCode[i].split('_ngd_')
#             matrix[cM[equating[i1]]][cM[equating[i2]]] = line1[i]
#             matrix[cM[equating[i2]]][cM[equating[i1]]] = line1[i]

#         # Network to anatomical correlations
#         for i in range(len(line2)):
#             (j1, j2, j3, i1, j4, i2) = anatCode[i].split('_')
#             matrix[cM[equating[i1]]][cM[i2]] = line2[i]
#             matrix[cM[i2]][cM[equating[i1]]] = line2[i]

#         if id not in patients:
#             patients[id] = {'studies': 0}

#         patients[id][study] = matrix
#         patients[id]['studies'] += 1

#         if patients[id]['studies'] == 2:
#             validPts.append(id)

patients = {};  vals = {}; hbs = []
with open('abcd_ybd01.csv', 'r') as bldData:
    bldCode = bldData.readline().strip().split('\t')
    bldEnglish = bldData.readline().strip().split('\t')

    for line in bldData:
        line = line.strip().split('\t')
        id = line[3]; hba1c = line[37]

        if hba1c != "\"\"": 
            hbs.append(float(line[37].strip('"')))
            vals[id] = hba1c
            patients[id] = { 'HbA1C': hba1c }


hba1c_values = [float(patient_info['HbA1C'].strip('"')) for patient_info in patients.values()]

print(hba1c_values)

# ind = 0
# for i in patients:
#     print(patients[i], hba1c_values[ind])
#     ind +=1


# Calculate quartiles
q1, q2, q3 = np.percentile(hba1c_values, [25, 50, 75])

# Assign patients to quartiles
quartiles = {f"Q{i}": [] for i in range(1, 5)}

for patient_id, patient_info in patients.items():
    hba1c = float(patient_info['HbA1C'].strip('"'))

    if hba1c < q1:
        quartile = "Q1"
    elif hba1c < q2:
        quartile = "Q2"
    elif hba1c < q3:
        quartile = "Q3"
    else:
        quartile = "Q4"

    quartiles[quartile].append({patient_id: patient_info})

print( len(quartiles['Q1']), len(quartiles['Q2']), len(quartiles['Q3']), len(quartiles['Q4']), 'Quartile values: ', q1, q2, q3)



hba1c_values = [float(patient_data["HbA1C"].strip('"')) for patient_data in patients.values()]
hba1c_values.sort()

tertile1, tertile2 = np.percentile(hba1c_values, [100/3, 200/3])

group1, group2, group3 = [], [], []

for patient_id, patient_data in patients.items():
    hba1c = float(patient_data["HbA1C"].strip('"'))

    if hba1c <= tertile1:
        group1.append({patient_id: patient_data})
    elif hba1c <= tertile2:
        group2.append({patient_id: patient_data})
    else:
        group3.append({patient_id: patient_data})

print(f"Tertile 1: {len(group1)} Tertile 2: {len(group2)} Tertile 3: {len(group3)}")
print('Tertile values: ', tertile1, tertile2)





hba1c_values = [float(patient_data["HbA1C"].strip('"')) for patient_data in patients.values()]
hba1c_values.sort()

quintile1, quintile2, quintile3, quintile4 = np.percentile(hba1c_values, [20, 40, 60, 80])

group1, group2, group3, group4, group5 = [], [], [], [], []

for patient_id, patient_data in patients.items():
    hba1c = float(patient_data["HbA1C"].strip('"'))

    if hba1c <= quintile1:
        group1.append({patient_id: patient_data})
    elif hba1c <= quintile2:
        group2.append({patient_id: patient_data})
    elif hba1c <= quintile3:
        group3.append({patient_id: patient_data})
    elif hba1c <= quintile4:
        group4.append({patient_id: patient_data})
    else:
        group5.append({patient_id: patient_data})


hba1c_values = [float(patient_data["HbA1C"].strip('"')) for patient_data in patients.values()]
hba1c_values.sort()

sextile1, sextile2, sextile3, sextile4, sextile5 = np.percentile(hba1c_values, [100/6*i for i in range(1, 6)])

group1, group2, group3, group4, group5, group6 = [], [], [], [], [], []

for patient_id, patient_data in patients.items():
    hba1c = float(patient_data["HbA1C"].strip('"'))

    if hba1c <= sextile1:
        group1.append({patient_id: patient_data})
    elif hba1c <= sextile2:
        group2.append({patient_id: patient_data})
    elif hba1c <= sextile3:
        group3.append({patient_id: patient_data})
    elif hba1c <= sextile4:
        group4.append({patient_id: patient_data})
    elif hba1c <= sextile5:
        group5.append({patient_id: patient_data})
    else:
        group6.append({patient_id: patient_data})

print(f"Sextile 1: {len(group1)} Sextile 2: {len(group2)} Sextile 3: {len(group3)} Sextile 4: {len(group4)} Sextile 5: {len(group5)} Sextile 6: {len(group6)}")
print("Sextile values: ", sextile1, sextile2, sextile3, sextile4, sextile5)


hba1c_values = [float(patient_data["HbA1C"].strip('"')) for patient_data in patients.values()]
hba1c_values.sort()

septile1, septile2, septile3, septile4, septile5, septile6 = np.percentile(hba1c_values, [100/7*i for i in range(1, 7)])

group1, group2, group3, group4, group5, group6, group7 = [], [], [], [], [], [], []

for patient_id, patient_data in patients.items():
    hba1c = float(patient_data["HbA1C"].strip('"'))

    if hba1c <= septile1:
        group1.append({patient_id: patient_data})
    elif hba1c <= septile2:
        group2.append({patient_id: patient_data})
    elif hba1c <= septile3:
        group3.append({patient_id: patient_data})
    elif hba1c <= septile4:
        group4.append({patient_id: patient_data})
    elif hba1c <= septile5:
        group5.append({patient_id: patient_data})
    elif hba1c <= septile6:
        group6.append({patient_id: patient_data})
    else:
        group7.append({patient_id: patient_data})

print(f"Septile 1: {len(group1)} Septile 2: {len(group2)} Septile 3: {len(group3)} Septile 4: {len(group4)} Septile 5: {len(group5)} Septile 6: {len(group6)} Septile 7: {len(group7)}")
print('Septile Values: ', septile1, septile2, septile3, septile4, septile5, septile6)















# print("Quartiles:")
# for key, value in quartiles.items():
#     print(f"{key}: {value}")




# # Create a dictionary of {string: float}
# data = {'a': 3, 'b': 1, 'c': 4, 'd': 1, 'e': 5, 'f': 9, 'g': 2, 'h': 6, 'i': 5, 'j': 3, 'k': 5}

# # Extract the values and store them in a list
# values = list(data.values())

# # Calculate the quartiles using the statistics module
# q1 = statistics.median_low(values)
# q2 = statistics.median(values)
# q3 = statistics.median_high(values)

# print("Q1:", q1)
# print("Q2 (median):", q2)
# print("Q3:", q3)

# os.chdir('../working')
# with open('patients.pickle', 'wb') as file:
#     pickle.dump(patients, file)