import os, json, pandas as pd

os.chdir('../working')

class Patient:
    def __init__(self, id, baseline, year2):
        self.id = id 
        self.baseline = baseline
        self.year2 = year2

    def __str__(self):
        return f"ID: {self.id}\nBaseline {self.baseline}\n\n\nFollow Up: {self.year2}\n\n\n"

    def getBaseline(self):
        return self.baseline
    
    def getFollowup(self):
        return self.year2
        
data = json.load(open('output.txt'))

patients = dict(); 
for id in data:
    patients[id] = Patient(id, pd.DataFrame(data[id]['baseline']), pd.DataFrame(data[id]['2year']))

