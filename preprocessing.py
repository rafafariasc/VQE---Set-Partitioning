from reductions import *

def preprocess_function(A_orig, C_orig): 

    # initialize lists
    deleted_row_indices = []
    F_0 = [] # list of variables fixed to zero
    F_1 = [] # list of variables fixed to one

    # apply preprocessing reductions
    A_orig = reduction_0(A_orig, deleted_row_indices)
    # deleted_row_indices = []
    # print(f"The matrix A_orig = \n", A_orig)
    F_0, F_1 = reduction_1(A_orig, F_0, F_1)
    deleted_row_indices, F_0, F_1 = reduction_2(A_orig, deleted_row_indices, F_0, F_1)
    deleted_row_indices, F_0, F_1 = reduction_3(A_orig, deleted_row_indices, F_0, F_1)
    F_0 = reduction_4(A_orig, F_0, C_orig)
    F_0, F_1 = reduction_5(A_orig, F_0, F_1)

    # create a list of columns to delete
    deleted_column_indices = [index for index in F_0]
    deleted_column_indices.extend(F_1)

    # delete rows and columns of A
    A_reduced = np.delete(A_orig, deleted_row_indices, axis = 0)
    A_reduced = np.delete(A_reduced, deleted_column_indices, axis = 1)

    # create a list of cost coefficients corresponding to columns that aren't deleted
    C_reduced = np.delete(C_orig, deleted_column_indices)

    return A_reduced, C_reduced, deleted_row_indices, F_0, F_1