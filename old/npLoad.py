import os, json, pandas as pd, numpy as np, time, multiprocessing

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

os.chdir('../working')

class Patient:
    def __init__(self, id, baseline, followup):
        self.id = id 
        self.baseline = baseline
        self.followup = followup

    def __str__(self):
        return f"ID: {self.id}\nBaseline {self.baseline}\n\n\nFollow Up: {self.followup}\n\n\n"

    def getBaseline(self):
        return self.baseline
    
    def getFollowup(self):
        return self.followup
    
start = time.perf_counter()

# Load JSON 
data = json.load(open('tests6.json'))

# Change to CSV
lC = []
with open('tests6.json', 'r') as file:
    for line in file:
        for char in line:
            if char == '{' or char == '}':
                lC.append(',')
            else:
                lC.append(char)

# Followups
followups = []
for i in data:
    followups.append(data[i]["2year"])

# Baslines
baselines = []
for i in data:
    followups.append(data[i]["baseline"])

# Dict
patients = {} 
for i in data:
    patients[id] = Patient(i, pd.DataFrame(data[i]['baseline'], cM.keys(), cM.keys()), pd.DataFrame(data[i]['2year'], cM.keys(), cM.keys()))




end = time.perf_counter()
print(end - start)

# Before: 39, 
# After: 
