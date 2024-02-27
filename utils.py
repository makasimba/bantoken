from typing import List, Tuple, Dict

def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if ids[i] == pair[0] and i < len(ids) - 1 and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1
    return newids

def freq(T: List[int])->Dict[Tuple[int], int]:
    counts = {}
    for t in range(len(T)-1):
        a, b = T[t], T[t+1]
        counts[(a, b)] = counts.get((a, b), 0) + 1
    return counts

def frequency(T, counts=None):
    counts = counts if counts is not None else {}
    for t in range(len(T)-1):
        a, b = T[t], T[t+1]
        counts[(a, b)] = counts.get((a, b), 0) + 1
    return counts