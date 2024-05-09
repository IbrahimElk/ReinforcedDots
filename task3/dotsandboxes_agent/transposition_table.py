import numpy as np

class TNaive_Table:
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
        return self.cache.copy()
    
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
        if self.check_horizontal(state, num_rows, num_cols) in self.cache:
            self.hits += 1
            return self.cache[hashed_state]
        if self.check_vertical(state, num_rows, num_cols) in self.cache:
            self.hits += 1
            return self.cache[hashed_state]
        if self.check_h_and_v(state, num_rows, num_cols) in self.cache:
            self.hits += 1
            return self.cache[hashed_state]
        if num_rows == num_rows:
            if self.check_diag_1(state, num_rows, num_cols) in self.cache:
                self.hits += 1
                return self.cache[hashed_state]
            if self.check_diag_2(state, num_rows, num_cols) in self.cache:
                self.hits += 1
                return self.cache[hashed_state]
            else:
                self.misses += 1
                return None
        else:
            self.misses += 1
            return None


    def _hash_state(self, state):
        hash_hex = state.dbn_string()
        return hash_hex
    
    def check_horizontal(self, state, num_rows, num_cols):
        state_indexes = list(map(int, list(state.dbn_string())))

        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        new_h_list = np.flipud(h_matrix).ravel()
        new_v_list = np.flipud(v_matrix).ravel()

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))

    def check_vertical(self, state, num_rows, num_cols):
        state_indexes = list(map(int, list(state.dbn_string())))
        
        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        new_h_list = np.fliplr(h_matrix).ravel()
        new_v_list = np.fliplr(v_matrix).ravel()

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))

    def check_h_and_v(self, state, num_rows, num_cols):
        state_indexes = list(map(int, list(state.dbn_string())))
        
        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        h_matrix = np.flipud(h_matrix)
        v_matrix = np.flipud(v_matrix)

        new_h_list = np.fliplr(h_matrix).ravel()
        new_v_list = np.fliplr(v_matrix).ravel()

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))
    
    #only for square boards
    def check_diag_1(self, state, num_rows, num_cols):
        state_indexes = list(map(int, list(state.dbn_string())))
        
        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        new_h_list = np.rot90(v_matrix, 3).ravel()
        new_v_list = np.rot90(h_matrix, 3).ravel()

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))

    #only for square boards
    def check_diag_2(self, state, num_rows, num_cols):
        state_indexes = list(map(int, list(state.dbn_string())))
        
        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        new_h_list = np.rot90(v_matrix, 3).ravel()
        new_v_list = np.rot90(h_matrix, 3).ravel()

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))
