# DANIEL VERDEJO, ID: 22240224

from collections import Counter
import sys
import json
from itertools import chain

filename = sys.argv[1]

def read_file() -> dict:
    with open(filename) as f:
        file_str = f.read().replace('\n', '').replace("'", '"')
        return json.loads(file_str)

# get the societies which the target is in
def find(societies, target) -> list:
    socs = list()
    for s in societies:
        if target.lower() in map(str.lower, societies[s]):
            socs.append(societies[s])
    return list(chain(*socs)) # flattenlist of lists (if the target is in multiple socs)

def get_all_candidates(societies) -> list:
    people = list()
    [[people.append(p) for p in societies[s]] for s in societies]
    people = Counter(people)
    return  [k for k, v in people.items() if v > 1] # Return a list of people which are in more than one society

# Recursively search and collect people who have a connection to the source and target 
def recursive_search(curr_person, socs, collector=['Dracula']) -> list: 
    if 'Pumpkin' in collector or curr_person in collector: # short circut the search just return immediately if we found Pumpkin
        return collector
    for curr_soc in socs:
        if 'Dracula' not in curr_soc: # Don't consider  the root of the search we do that in common_communicators
            if curr_person in curr_soc:
                collector.append(curr_person) 
                if 'Pumpkin' not in curr_soc: # If no pumpkin, repeat the search for each member in the current soc
                    next_socs = socs.copy()
                    next_socs.remove(curr_soc) # drop the current soc from the next search 
                    for next_person in curr_soc: 
                        recursive_search(next_person, next_socs, collector)
                else:
                    collector.append('Pumpkin') # We found Pumpkin! now we can begin our return
                    return collector
    return collector

# does what it says, returns a list of common communicators between the source and target...
def common_communicator(a, b, candidates, societies, source, target):
    get_candidate = (lambda t, c: [p for p in c if p in t]) 

    a_cand = get_candidate(a, candidates) # filter out the people in our source and target societies that don't participate in other societies
    b_cand = get_candidate(b, candidates)
    if len(a_cand) < 1 or len(b_cand) < 1: # if either of these have 0 people theres no path, short circut our search
        return []
    
    relevant_socs = list()
    for v in societies.values():
        if any(x in v for x in a_cand) or any(x in v for x in b_cand):
            relevant_socs.append([i for i in v if i in [*candidates, source, target]]) #filter out some noise
    
    results, i = [], 0
    while target not in results and i < len(a_cand): # for each person in the root society while we havent found our target
        results.append(recursive_search(a_cand[i], relevant_socs))
        results = list(chain(*results))
        i+=1
    return results
        

if __name__ == "__main__":
    src, tgt = 'Dracula', 'Pumpkin'
    societies = read_file() # now we have our dict of socs
    d_socs, p_socs = find(societies, src), find(societies, tgt) # get the societies each person of interest is in
    multi = get_all_candidates(societies) # get only the folks who are in multiple societies, the rest are just noise
    path = common_communicator(d_socs, p_socs, multi, societies, src, tgt)  # get the path

    if 'Pumpkin' in path:
        print('Dracula can pass a message to Pumpkin! Heres how:')
        print(' -> '.join(path))
    else:
        print("Dracula cannot pass a message to Pumpkin... :(")
