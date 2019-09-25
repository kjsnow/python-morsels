
def add(*inputs):
    for x in range(0, len(inputs) - 1):
        if len(inputs[x]) != len(inputs[x+1]):
            raise ValueError("Given matrices are not the same size.")
    matrix_sum = list()
    for i in range(0, len(inputs[0])):
        tmp_matrix = list()
        for j in range(0, len(inputs[0][0])):
            tmp = 0
            for k in range(0, len(inputs)):
                tmp = tmp + inputs[k][i][j]
            tmp_matrix.append(tmp)
        matrix_sum.append(tmp_matrix)
    return matrix_sum