import os, pickle

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

patients = {}; validPts = []
with open (b, 'r') as betnet, open (r, 'r') as rscor:
    ntwkCode = betnet.readline().strip().split(',')[22:-2]; anatCode = rscor.readline().strip().split(',')[22:-2] # Encoded labels, first line
    english = betnet.readline().strip().split(',') + rscor.readline().strip().split(',') # Plain english translation, second line

    for line1, line2 in zip(betnet, rscor): # INPUT FILES MUST BE SORTED BY: "rsfmri_c_ngd_visitid"	
        matrix = [[0 for j in range(32)] for i in range(32)]
        line1 = line1.strip().split(',')[22:-2]
        line2 = line2.strip().split(',')

        ## Extract any additional data here ##
        id = line2[3]; study = line2[9].split('_')[-1]
        line2 = line2[22:-2]

        # Network to network correlations 
        for i in range(len(line1)):
            (junk, i1, i2) = ntwkCode[i].split('_ngd_')
            matrix[cM[equating[i1]]][cM[equating[i2]]] = line1[i]
            matrix[cM[equating[i2]]][cM[equating[i1]]] = line1[i]

        # Network to anatomical correlations
        for i in range(len(line2)):
            (j1, j2, j3, i1, j4, i2) = anatCode[i].split('_')
            matrix[cM[equating[i1]]][cM[i2]] = line2[i]
            matrix[cM[i2]][cM[equating[i1]]] = line2[i]

        if id not in patients:
            patients[id] = {'studies': 0}

        patients[id][study] = matrix
        patients[id]['studies'] += 1

        if patients[id]['studies'] == 2:
            validPts.append(id)

withM = 0; withoutM = 0; nonValidH = 0
with open('abcd_ybd01.csv', 'r') as bldData:
    bldCode = bldData.readline().strip().split('\t')
    bldEnglish = bldData.readline().strip().split('\t')

    for line in bldData:
        line = line.strip().split('\t')

        if line[3][1:-1] in validPts and line [37] != "\"\"":
            print(line[3][1:-1], line[37], line[3][1:-1] in validPts, line[37] == "\"\"")
            withM += 1
        else:
            withoutM +=1

        if line [37] != "\"\"": nonValidH +=1

print(withM, withoutM, nonValidH)









os.chdir('../working')
with open('patients.pickle', 'wb') as file:
    pickle.dump(patients, file)