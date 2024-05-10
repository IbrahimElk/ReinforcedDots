import symmetry.symmetries as s

class TNaive_Table:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.symmhits = 0

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
        return self.cache.copy()
    
    def get_symmhits(self):
        return self.symmhits
    
class TEmpty_Table(TNaive_Table):
    def get(self, state):
        self.misses += 1
        return None

    def set(self, state, value):
        return
    
class TOptimised_Table(TNaive_Table):
    def get(self, state):
        hashed_state = self._hash_state(state)
        params = state.get_game().get_parameters()
        num_rows = params['num_rows']
        num_cols = params['num_cols']

        if hashed_state in self.cache:
            self.hits += 1
            return self.cache[hashed_state]
        
        cache_result = s.check_horizontal(state, num_rows, num_cols)
        if cache_result in self.cache:
            self.symmhits += 1
            return self.cache[cache_result]
        
        cache_result = s.check_vertical(state, num_rows, num_cols)
        if cache_result in self.cache:
            self.symmhits += 1
            return self.cache[cache_result]
        
        cache_result = s.check_hv(state, num_rows, num_cols)
        if cache_result in self.cache:
            self.symmhits += 1
            return self.cache[cache_result]
        
        # FIXME : ibr : MSS OVERBODIG!!
        cache_result = s.check_vh(state, num_rows, num_cols)
        if cache_result in self.cache:
            self.symmhits += 1
            return self.cache[cache_result]

        if num_rows == num_cols:
            cache_result = s.check_diag1(state, num_rows, num_cols)
            if cache_result in self.cache:
                self.symmhits += 1
                return self.cache[cache_result]
            cache_result = s.check_diag2(state, num_rows, num_cols)
            if cache_result in self.cache:
                self.symmhits += 1
                return self.cache[cache_result]
            
            cache_result = s.check_h_diag1(state, num_rows, num_cols)
            if cache_result in self.cache:
                self.symmhits += 1
                return self.cache[cache_result]
            else:
                self.misses += 1
                return None
        else:
            self.misses += 1
            return None