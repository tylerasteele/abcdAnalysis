import os, pandas as pd



os.chdir('../data')
bet02 = 'abcd_betnet02.txt'
file = 'abcd_betnet02.txt'
file2 = 'mrirscor02.txt'

lines = []; ptScans = {}; i = 0
with open (file2, 'r') as file:
    for line in file:
        line = line.strip().split('\t')
        lines.append(line)

        if i > 1:
            if line[3] not in ptScans: ptScans[line[3]] = [line[9]]
            else: ptScans[line[3]].append(line[9])
        i+=1

print(len(ptScans))

twoScans = 0; oneScan = 0
for p in ptScans:
    if len(ptScans[p]) == 2:
        twoScans+=1
    else: oneScan +=1

# 18991 11614 7375 4239
# 18991 11614 7375 4239
print(i, len(ptScans), twoScans, oneScan)


