from minimax.symmetry_minimax import find_representative
from minimax.chains_minimax import extract_chain_info

class Transposition_Table:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def get(self, state):
        hashed_state = self._hash_state(state)
        if hashed_state in self.cache:
            self.hits += 1
            return self.cache[hashed_state]
        else:
            self.misses += 1
            return None

    def set(self, state, value):
        hashed_state = self._hash_state(state)
        self.cache[hashed_state] = value

    def _hash_state(self, state):
        hash_hex = state.dbn_string()
        return hash_hex
    
    def get_hits(self):
        return self.hits
    
    def get_misses(self):
        return self.misses
    
    def get_cache(self) -> dict:
        return self.cache
    
class TNaive_Table(Transposition_Table):
    def get(self, state):
        return None

    def set(sefl, state, value):
        return 

class TChains_Table(Transposition_Table):
    # TODO:
    def _hash_state(self, state):
        # change state representation
        # gebruik args argumetn bv. 
        # bv. aantal chains in state = chains_info 
        chains_info = extract_chain_info(state)
        hash_hex = state.dbn_string()
        return hash_hex
    
class TSymmetric_Table(Transposition_Table):
    # TODO:
    def _hash_state(self, state):
        symmetric_state = find_representative(state)
        hash_hex = symmetric_state.dbn_string()
        return hash_hex

class TTable(Transposition_Table):
    # TODO:
    def _hash_state(self, state):
        chains_info = extract_chain_info(state)
        symmetric_state = find_representative(state)
        hash_hex = symmetric_state.dbn_string()
        return hash_hex
    