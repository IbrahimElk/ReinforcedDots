import numpy as np


""" state_indexes = {0, 1, 2, 5, 6, 9, 11}
m = 4
n = 3

h_matrix = np.zeros((m,n), dtype=int)
mirrored_h_list = list()

def matrix_to_list(matrix, list):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 1:
                number = i * matrix.shape[1] + j
                list.append(number)
                
    return list

def list_to_matrix(list, matrix, num_cols):
    for number in list:
        row = number // num_cols
        column = number % num_cols
        matrix[row, column] = 1

    return matrix

new_matrix = list_to_matrix(state_indexes, h_matrix, n)
print(new_matrix)
new_list = matrix_to_list(new_matrix, list())
print(new_list)
new_list1 = [x + 12 for x in new_list]
print(new_list)
print(new_list+new_list1) """

def matrix_to_list(matrix, list):
    for index, value in np.ndenumerate(matrix):
        if value == 1:
            list.append(np.ravel_multi_index(index, matrix.shape))
    return list

def list_to_matrix(list, matrix):
    for number in list:
        index = np.unravel_index(number, matrix.shape)
        matrix[index] = 1
    return matrix

state_indexes = {0, 1, 2, 4, 6, 9}
state_indexes = "101010100100"
num_rows = 2
num_cols = 2
def _hash_state(self, state):
        # symmetric_state = find_representative(state)
        # hash_hex = symmetric_state.dbn_string()
        
        # temp:
        hash_hex = state.dbn_string()
        return hash_hex
    
def list_to_matrix(list, matrix):
        for number in list:
            index = np.unravel_index(number, matrix.shape)
            matrix[index] = 1
        return matrix

def matrix_to_list(matrix, list):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] == 1:
                    number = i * matrix.shape[1] + j
                    list.append(number)
                    
        return list
    
def check_horizontal(state_list, num_rows, num_cols):
        state_indexes = list(map(int, list(state_list)))

        h_edges = (num_rows+1)*num_cols

        h_list = state_indexes[:h_edges]
        v_list = state_indexes[h_edges:]

        h_matrix = np.zeros((num_rows+1,num_cols), dtype=int)
        v_matrix = np.zeros((num_rows,num_cols+1), dtype=int)

        h_matrix = np.reshape(h_list, h_matrix.shape)
        v_matrix = np.reshape(v_list, v_matrix.shape)

        new_h_list = np.rot90(v_matrix).ravel()
        new_v_list = np.rot90(h_matrix).ravel()
        print(new_h_list)
        print(new_v_list)

        new_state_indexes = np.concatenate((new_h_list, new_v_list), axis=None)
        return "".join(map(str, new_state_indexes))

print(check_horizontal(state_indexes, num_rows, num_cols))