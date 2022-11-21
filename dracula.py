from collections import Counter
import sys
import json
from itertools import chain

filename = sys.argv[1]

def read_file() -> dict:
    with open(filename) as f:
        file_str = f.read().replace('\n', '').replace("'", '"')
        return json.loads(file_str)

def find(societies, target) -> list:
    socs = list()
    for s in societies:
        if target.lower() in map(str.lower, societies[s]):
            socs.append(societies[s])
    return list(chain(*socs)) # flattenlist of lists (if the target is in multiple socs)

def get_all_candidates(societies) -> dict:
    people = list()
    [[people.append(p) for p in societies[s]] for s in societies]
    people = Counter(people)
    return  [k for k, v in people.items() if v > 1]

def recursive_search(c, socs, collector=['Dracula']) -> list:
    if 'Pumpkin' in collector or c in collector:
        return collector
    for s in socs:
        if 'Dracula' not in s:
            if c in s:
                collector.append(c) 
                if 'Pumpkin' not in s: 
                    x = socs.copy()
                    x.remove(s)
                    for si in s:
                        recursive_search(si, x, collector)
                else:
                    collector.append('Pumpkin')
                    return collector
    return collector

def common_communicator(a, b, candidates, societies, source, target):
    get_candidate = (lambda t, c: [p for p in c if p in t])

    a_cand = get_candidate(a, candidates)
    b_cand = get_candidate(b, candidates)
    if len(a_cand) < 1 or len(b_cand) < 1:
        return []
    
    relevant_socs = list()
    for v in societies.values():
        if any(x in v for x in a_cand) or any(x in v for x in b_cand):
            relevant_socs.append([i for i in v if i in [*candidates, source, target]])
    
    results, i = [], 0
    while target not in results and i < len(a_cand):
        results.append(recursive_search(a_cand[i], relevant_socs))
        results = list(chain(*results))
        i+=1
    return results
        

if __name__ == "__main__":
    src, tgt = 'Dracula', 'Pumpkin'
    societies = read_file()
    d_socs, p_socs = find(societies, src), find(societies, tgt)
    multi = get_all_candidates(societies)
    path = common_communicator(d_socs, p_socs, multi, societies, src, tgt)

    if 'Pumpkin' in path:
        print('Dracula can pass a message to Pumpkin! Heres how:')
        print(' -> '.join(path))
    else:
        print("Dracula cannot pass a message to Pumpkin... :(")
