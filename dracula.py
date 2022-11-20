from collections import Counter
import sys
import json
import numpy as np

filename = sys.argv[1]

def read_file() -> dict:
    
    with open(filename) as f:
        file_str = f.read().replace('\n', '').replace("'", '"')
        return json.loads(file_str)

def find(societies, name) -> dict:
    socs = dict()
    for s in societies:
        if name in map(str.lower, societies[s]):
            socs[s] = societies[s]
    return socs

def count_socs(societies) -> dict:
    people = list()
    [[people.append(p) for p in societies[s]] for s in societies]
            
    print(Counter(people))
            # if not people[p]:
        

def common_communicators(a, b, all_socs):
    common = list()
    for s in all_socs:
        print(all_socs[s])
    
        

if __name__ == "__main__":
    societies = read_file()
    d_socs = find(societies, 'dracula')
    p_socs = find(societies, 'pumpkin')
    count_socs(societies)
    # paths = common_communicators(d_socs, p_socs, societies)
    
    # print(d_socs, p_socs)