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
        if target in map(str.lower, societies[s]):
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


def common_communicator(a, b, candidates, societies):
    get_candidate = (lambda t, c: [p for p in c if p in t])
    common = get_candidate(a, b)
    if len(common) > 1:
        return f"{common}"

    a_cand = get_candidate(a, candidates)
    b_cand = get_candidate(b, candidates)
    if len(a_cand) < 1 or len(b_cand) < 1:
        return []
    
    relevant_socs = list()
    for v in societies.values():
        if any(x in v or y in v for x, y in (a_cand, b_cand)):
            relevant_socs.append([i for i in v if i in [*candidates, 'Dracula', 'Pumpkin']])
    
    results, i = [], 0
    while 'Pumpkin' not in results:
        results.append(recursive_search(a_cand[i], relevant_socs))
        results = list(chain(*results))
        i+=1
    return results
        

if __name__ == "__main__":
    societies = read_file()
    d_socs, p_socs = find(societies, 'dracula'), find(societies, 'pumpkin')
    multi = get_all_candidates(societies)
    path = common_communicator(d_socs, p_socs, multi, societies)

    if 'Pumpkin' in path:
        print('Dracula can meet Pumpkin! Heres how:')
        print(' -> '.join(path))
    else:
        print("Dracula cannot meet Pumpkin... :(")
