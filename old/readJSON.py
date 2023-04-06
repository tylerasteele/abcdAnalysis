import os, pandas as pd, json

os.chdir('../working')

with open ('output.json', 'r') as file:
    data = json.load(file)


for pt in data:
    for scan in data[pt]:
        data[pt][scan] = pd.DataFrame(data[pt][scan])


