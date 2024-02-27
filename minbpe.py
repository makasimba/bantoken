""" Encoders For GPTs """

from utils import merge, freq, frequency
from typing import List, Tuple, Dict
from tqdm import tqdm
import regex as re


class BasicBPE:

    """ Basic BPE Encode """

    def __init__(self):
        self.V = {idx: bytes([idx]) for idx in range(256)}  
        self.M = {}
    
    def train(self, text: str, vocab_size: int, verbose=False):
        n_merges = vocab_size - len(self.V)
        TRAIN = text.encode('utf-8')
        new_id = len(self.V)

        for _ in tqdm(range(n_merges)):
            counts = freq(TRAIN)
            pair = max(counts, key=counts.get)
            a, b = pair
            TRAIN = merge(TRAIN, (a, b), new_id)
            self.M[(a, b)] = new_id
            self.V[new_id] = self.V[a]+self.V[b]
            new_id += 1
        return TRAIN

    def encode(self, text: str)->List[int]:
        tokens = list(text.encode('utf-8'))
        for p, id in self.M.items():
            tokens = merge(tokens, p, id)
        return tokens

    def decode(self, ids: List[int])->str:
        bz = b''.join([self.V[id] for id in ids])
        return bz.decode('utf-8', errors='replace')


class BPE:
    
    """ Regular BPE Encode """
    
    def __init__(self):
        self.V = {d:bytes([d]) for d in range(256)}
        self.M = {}
        self.needle = r""" ?\p{N}+| ?\p{L}+|\s+(?!\S)|\s+|[^\s\p{N}\p{L}]+"""
        self.pat = re.compile(self.needle)
    
    def train(self, text, vocab_size):
        words = [list(word.encode('utf-8')) for word in re.findall(self.pat, text)]
        n_merges = vocab_size - len(self.V)

        new_token_id = len(self.V)

        for _ in tqdm(range(n_merges)):
            counts = {}
            for word in words:
                frequency(word, counts)
            
            a, b = max(counts, key=counts.get)
            self.M[(a, b)] = new_token_id
            self.V[new_token_id] = self.V[a] + self.V[b]

            words = [merge(word, (a, b), new_token_id) for word in words]
            new_token_id += 1
    
    def decode(self, ids):
        bz = b''.join(self.V[d] for d in ids)
        return bz.decode('utf-8', errors='replace')
    
    def encode(self, txt):
        t = list(txt.encode('utf-8'))
        for p, d in self.M.items():
            t = merge(t, p, d)
        return t
