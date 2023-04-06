import json, orjson, ujson, multiprocessing, os, time, threading, mmap

os.chdir('../working')

file = 'tests6.json'




def read_file_multiprocessing(file):
    with open(file, 'r') as f:
        data = json.load(f)

def read_file_multithreading(file):
    with open(file, 'r') as f:
        data = json.load(f)



# Multiprocessing
start = time.perf_counter()
process = multiprocessing.Process(target=read_file_multiprocessing, args=(file,))
process.start()
process.join()
end = time.perf_counter()
print(f"Time taken with multiprocessing: {end - start}")

# Multithreading
start = time.perf_counter()
thread = threading.Thread(target=read_file_multithreading, args=(file,))
thread.start()
thread.join()
end = time.perf_counter()
print(f"Time taken with multithreading: {end - start}")





start = time.perf_counter()
with open(file, 'r') as f:
    data = ujson.loads(f.read())
end = time.perf_counter()
print(end - start)

start = time.perf_counter()
with open(file, 'r') as f:
    data = ujson.loads(f.read())
end = time.perf_counter()
print(end - start)




start = time.perf_counter()
with open(file, 'r') as f:
    data = json.load(f)
end = time.perf_counter()
print(end - start)


start = time.perf_counter()
data = []
with open(file, "r+b") as f: # open the file in read-write binary mode
  mm = mmap.mmap(f.fileno(), 0) # map the file into memory
  for line in iter(mm.readline, b""): # iterate over each line
    data.append(json.loads(line)) # parse each line as a JSON object
  mm.close() # close the memory map
end = time.perf_counter()
