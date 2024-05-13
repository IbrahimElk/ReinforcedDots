import numpy as np

def matrix_to_list(matrix, list):
    """ for index, value in np.ndenumerate(matrix):
        if value == 1:
            list.append(np.ravel_multi_index(index, matrix.shape))
            print(index, value) """
    list = np.ravel(matrix)
    return list

def list_to_matrix(list, matrix):
        return np.reshape(list, matrix.shape)

# Example usage
filled_matrix = np.array([[1, 1, 0, 1],
                          [1, 1, 0, 0],
                          [1, 1, 0, 1]])
print(np.rot90(filled_matrix))
print(np.rot90(filled_matrix, 3))


