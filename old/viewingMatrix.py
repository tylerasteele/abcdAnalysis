lbls = []
for i in range(len(ntwkCode)):
    if ntwkCode[i].split('_ngd_')[1] not in lbls:
        lbls.append(ntwkCode[i].split('_ngd_')[1])

for i in range(len(anatCode)):
    if anatCode[i].split('_')[-1] not in lbls:
        lbls.append(anatCode[i].split('_')[-1])

df = pd.DataFrame(patients['NDAR_INV03XVEBPM']['baseline'], lbls, lbls)

print(df)
