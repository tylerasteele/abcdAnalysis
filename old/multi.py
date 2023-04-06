import os, json, pandas as pd, numpy as np, time, multiprocessing, ujson, orjson

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

def create_patient(id):
    # create a Patient object from the data
    baseline = pd.DataFrame(data[id]['baseline'], cM.keys(), cM.keys())
    followup = pd.DataFrame(data[id]['2year'], cM.keys(), cM.keys())
    return Patient(id, baseline, followup)

def change_to_csv(line):
    # change a line of json to csv
    lC = []
    for char in line:
        if char == '{' or char == '}':
            lC.append(',')
        else:
            lC.append(char)
    
    return ''.join(lC)

start = time.perf_counter()

# Load JSON 
data = json.load(open('tests6.json'))

# Create a pool of workers
pool = multiprocessing.Pool()

# Map the change_to_csv function to the lines in parallel
with open('tests6.json', 'r') as file:
    csv_lines = pool.map(change_to_csv, file)

# Map the create_patient function to the ids in parallel
patients = pool.map(create_patient, data.keys())

# Close the pool and wait for all workers to finish
pool.close()
pool.join()

end = time.perf_counter()
print(end - start)

# 28.711686077000195