import os, pickle, numpy as np

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
    'audi': 0, 'cngo': 1, 'cngp': 2, 'dflt': 3, 'dsla': 4, 'fntp': 5, 'none': 6, 'rstn': 7,
    'smhn': 8, 'smmn': 9, 'saln': 10, 'vtan': 11, 'visn': 12, 'crcxlh': 13, 'thplh': 14, 'cdelh': 15,
    'ptlh': 16, 'pllh': 17, 'bs': 18, 'hplh': 19, 'aglh': 20, 'aalh': 21, 'vtdclh': 22, 'crcxrh': 23,
    'thprh': 24, 'cderh': 25, 'ptrh': 26, 'plrh': 27, 'hprh': 28, 'agrh': 29, 'aarh': 30, 'vtdcrh': 31
}

os.chdir('../data')

### Blood Data ### 
patients = {};  
with open('ybd.csv', 'r') as bldData:
    bldCode = bldData.readline().strip().split('\t')
    bldEnglish = bldData.readline().strip().split('\t')

    for line in bldData:
        line = line.strip().split('\t'); id = line[3].strip('"'); hba1c = line[37]

        if hba1c != "\"\"": 
            patients[id] = { 'hba1c': float(line[37].strip('"')), 'quintile': -1, 'scans': 0, 'baseline': [], '2year': [] }



# Calculate and place patients in quintiles, assign numeric in patient dictionary
hba1c_values = [patient_info['hba1c'] for patient_info in patients.values()]
hba1c_values.sort()
quintile1, quintile2, quintile3, quintile4 = np.percentile(hba1c_values, [20, 40, 60, 80])

# Edit quintil element in each patients dictionary by above rules
for id, ptData in patients.items():
    hba1c = ptData["hba1c"]

    if hba1c <= quintile1: patients[id]['quintile'] = 1
    elif hba1c <= quintile2: patients[id]['quintile'] = 2
    elif hba1c <= quintile3: patients[id]['quintile'] = 3
    elif hba1c <= quintile4: patients[id]['quintile'] = 4
    else: patients[id]['quintile'] = 5

### fMRI Data ###
# Full files 
b = 'betnet.csv'; r = 'mriRScor.csv';
 
# Limited files for testing
testCor = 'testCor.csv'; testBet = 'testBet.csv'; twoScans = {}
with open (b, 'r') as betnet, open (r, 'r') as rscor:
    ntwkCode = betnet.readline().strip().split(',')[22:-2]; anatCode = rscor.readline().strip().split(',')[22:-2] # Encoded labels, first line
    english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',') # Plain english translation, second line

    for line1, line2 in zip(betnet, rscor): # INPUT FILES MUST BE SORTED BY: "rsfmri_c_ngd_visitid"	
        line2 = line2.strip().split(',')
        id = line2[3]

        # If patient has an HbA1C measurement
        if id in patients:

            matrix = [[float('nan') for j in range(32)] for i in range(32)]
            line1 = line1.strip().split(',')[22:-2]

            ## Extract any additional data here (meds, other bloodwork, etc.) ## 
            scan = line2[9].split('_')[-1] # Splits to baseline or 2year
            line2 = line2[22:-2] # Removes non-fMRI data

            # Network to network correlations 
            test4blank = 0
            for i in range(len(line1)):
                (junk, i1, i2) = ntwkCode[i].split('_ngd_')
                matrix[cM[equating[i1]]][cM[equating[i2]]] = line1[i]
                matrix[cM[equating[i2]]][cM[equating[i1]]] = line1[i]
                if line1[i] == '': test4blank += 1; 
            
            # Get rid of blank fMRIs
            if test4blank >= 169: 
                patients.pop(id)
                continue
            for i in range(len(line2)):
                (j1, j2, j3, i1, j4, i2) = anatCode[i].split('_')
                matrix[cM[equating[i1]]][cM[i2]] = line2[i]
                matrix[cM[i2]][cM[equating[i1]]] = line2[i]

            patients[id][scan] = matrix
            patients[id]['scans'] += 1

            if patients[id]['scans'] == 2:
                twoScans[id] = patients[id]

print("Data cleaned successfully!")
os.chdir('../working')
with open('data.pickle', 'wb') as p: pickle.dump(twoScans, p)