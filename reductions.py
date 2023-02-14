import numpy as np
import itertools
import gurobipy as gp
from gurobipy import GRB

# Reduction 0: check for redundant rows
def reduction_0(A, deleted_row_indices):
    m = A.shape[0]
    for row1 in range(m):
        for row2 in range(m):
            if row1 >= row2: 
                continue
            if np.all(A[row1, :] == A[row2, :]):
                deleted_row_indices.append(row1)
                break
    
    A_true = np.delete(A, deleted_row_indices, axis = 0)
    # print(f"The matrix A_true = \n", A_true)

    return A_true

# Reduction 1: check for an empty row/column
def reduction_1(A, F_0, F_1):
    m = A.shape[0]

    for i in range(m):
        if sum(A[i, :]) == 0: # if there exists an empty row
            exit()

    # our addition
    n = A.shape[1]
    for j in range(n):
        if sum(A[:, j]) == 0: # if there exists an empty column
            F_0.append(j)
            # print(f"In reduction 1 we set x{j} to 0")

    F_0 = list(set(F_0)) # list of unique elements in F_0
    F_1 = list(set(F_1)) # list of unique elements in F_1

    return F_0, F_1

# Reduction 2: check for a unit row
def reduction_2(A, deleted_row_indices, F_0, F_1):
    m = A.shape[0]
    n = A.shape[1]
    deleted_row_indices = []

    for row in range(m):
        if sum(A[row, :]) == 1: # if there is a unit row
            deleted_row_indices.append(row)
            t = int(np.argwhere(A[row, :] == 1)) # find where the unit entry is located in the unit row
            
            if t not in F_1:
                F_1.append(t)
                # print(f"In reduction 2 we set x{t} to 1")

            for i in range(m): # iterate over the rows of A to find those with a[i, t] = 1
                if i != row and A[i, t] == 1 and i not in deleted_row_indices:
                    deleted_row_indices.append(i) 

                    for col in range(n):
                        if col != t and A[i, col] == 1 and col not in F_0:
                            F_0.append(col)
                            # print(f"In reduction 2 we set x{col} to 0")

    F_0 = list(set(F_0)) # list of unique elements in F_0
    F_1 = list(set(F_1)) # list of unique elements in F_1
    
    return deleted_row_indices, F_0, F_1

# Reduction 3: check if any row is greater than or equal to any other row (in a vector sense)
def reduction_3(A, deleted_row_indices, F_0, F_1):
    m = A.shape[0]
    deleted_row_indices = []

    for (row1, row2) in itertools.combinations(range(m), 2):
        if np.all(A[row1, :] - A[row2, :] >= 0) and row1 not in deleted_row_indices:
            deleted_row_indices.append(row1)
            dominating_entries_orig = np.argwhere(A[row1, :] - A[row2, :] == 1) # find where the dominating elements are in row1
            dominating_entries_new = [entry[0] for entry in dominating_entries_orig]
            F_0.extend(dominating_entries_new)

        if np.all(A[row2, :] - A[row1, :] >= 0) and row2 not in deleted_row_indices:
            deleted_row_indices.append(row2)
            dominating_entries_orig = list(np.argwhere(A[row2, :] - A[row1, :] == 1)) # find where the dominating elements are in row2
            dominating_entries_new = [entry[0] for entry in dominating_entries_orig]
            F_0.extend(dominating_entries_new)


    F_0 = list(set(F_0)) # list of unique elements in F_0
    
    return deleted_row_indices, F_0, F_1

# Reduction 4: check if items that are covered by a pattern can be covered by other patterns at no greater cost
def reduction_4(A, F_0, C):
    m = A.shape[0]
    n = A.shape[1]

    # suppress Gurobi output
    environment = gp.Env(empty = True)
    environment.setParam("OutputFlag", 0)
    environment.start()

    model = gp.Model(env = environment)
    y = model.addVars(n, vtype = GRB.BINARY, name = "y")
    model.ModelSense = GRB.MINIMIZE

    for t in range(n):
        model.setObjective(gp.quicksum(C[j] * y[j] for j in range(n) if j!=t))
        model.addConstrs(gp.quicksum(A[i, j] * y[j] for j in range(n) if j != t) == A[i, t] for i in range(m))
        model.addConstr(gp.quicksum(C[j] * y[j] for j in range(n) if j != t) <= C[t])
        model.update()
        model.write("reduction4.lp")
        model.optimize()

        if model.SolCount > 0:
            F_0.append(t)
            # print(f"In reduction 4, we set x{t} equal to 0")

        model.remove(model.getConstrs())

    return F_0

# Reduction 5: check if two rows are pairwise non-dominating
def reduction_5(A, F_0, F_1):
    m = A.shape[0]
    n = A.shape[1]

    for (row1, row2) in itertools.combinations(range(m), 2):
        if np.any(A[row1, :] - A[row2, :] < 0) and np.any(A[row1, :] - A[row2, :] > 0): # check if two rows are incomparable
            K = np.argwhere(A[row1, :] - A[row2, :] == 1) # list of dominating elements in row1
            I = np.argwhere(A[row2, :] - A[row1, :] == 1) # list of dominating elements in row2
            K_new = [int(element) for element in K]
            I_new = [int(element) for element in I]

            for row in range(m):
                if np.all(A[row, K_new] == A[row1, K_new]) and np.any(A[row, I_new] == A[row2, I_new]): # check if row exists (this is row s in the paper)
                    for col in range(n):
                        if A[row, col] == 1 and col in I_new and col not in F_0: # if row contains a 1 in a column whose index is in I_new and is not already in deleted_column_indices
                            F_0.append(col)
                            # print(f"In reduction 5 we set x{col} to 0")

        if np.any(A[row2, :] - A[row1, :] < 0) and np.any(A[row2, :] - A[row1, :] > 0): # check if two rows are incomparable
            K = np.argwhere(A[row2, :] - A[row1, :] == 1) # list of dominating elements in row1
            I = np.argwhere(A[row1, :] - A[row2, :] == 1) # list of dominating elements in row2
            K_new = [int(element) for element in K]
            I_new = [int(element) for element in I]

            for row in range(m):
                if np.all(A[row, K_new] == A[row2, K_new]) and np.any(A[row, I_new] == A[row1, I_new]): # check if row exists (this is row s in the paper)
                    for col in range(n):
                        if A[row, col] == 1 and col in I_new and col not in F_0: # if row contains a 1 in a column whose index is in I_new and is not already in deleted_column_indices
                            F_0.append(col)
                            # print(f"In reduction 5 we set x{col} to 0")
    
    F_0 = list(set(F_0)) # list of unique elements in F_0

    return F_0, F_1