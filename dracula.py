from collections import Counter
import sys
import json
# import numpy as np
from itertools import chain

filename = sys.argv[1]

def read_file() -> dict:
    with open(filename) as f:
        file_str = f.read().replace('\n', '').replace("'", '"')
        return json.loads(file_str)

def find(societies, target) -> list:
    socs = list()
    for s in societies:
        if target in map(str.lower, societies[s]):
            socs.append(societies[s])
    return list(chain(*socs)) # flattenlist of lists (if they target is in multiple socs)

def get_all_candidates(societies) -> dict:
    people = list()
    [[people.append(p) for p in societies[s]] for s in societies]
    people = Counter(people)
    return  [k for k, v in people.items() if v > 1]        

def common_communicators(a, b, candidates, societies):
    get_candidate = (lambda t, c: [p for p in c if p in t])
    common = get_candidate(a, b)
    if len(common) > 1:
        return f"{common}"

    a_cand = get_candidate(a, candidates)
    b_cand = get_candidate(b, candidates)
    if len(a_cand) < 1 or len(b_cand) < 1:
        return 'Dracula will not meet Pumpkin :( </3'
    
    relevant_socs = list()
    # get rid of any socs that our candidates are in
    for k, v in societies.items():
        if any(x in v or y in v for x, y in (a_cand, b_cand)):
            relevant_socs.append([i for i in v if i in candidates])
    print(relevant_socs, candidates)

        # print(any(a_cand) in v)
        # for c in a_cand:
        #     print(any())filt
        # if any(c in v for c in a_cand):
        #     print(c)
        # # print(k, v)

    
        

if __name__ == "__main__":
    societies = read_file()
    d_socs, p_socs = find(societies, 'dracula'), find(societies, 'pumpkin')
    multi = get_all_candidates(societies)
    path = common_communicators(d_socs, p_socs, multi, societies)
    print(path)
    # paths = common_communicators(d_socs, p_socs, societies)
    
    # print(d_socs, p_socs)