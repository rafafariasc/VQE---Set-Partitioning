import gurobipy as gb
from gurobipy import GRB

#function that defines the original objective function of the set partitioning problem
def sp_objective(w,x):
    """
    Objective function of the set partitioning problem
    :param x: binary vector of length n
    :param c: vector of length n
    :return: value of the objective function
    """
    obj = 0
    for i in range(len(w)):
        obj += w[i]*x[i]
    return obj

def sp_constraint(A,x):
    """
    Constraint function of the set partitioning problem
    :param A: matrix of size nxn
    :param x: binary vector of length n
    :return: value of the constraint function
    """
    cons = []
    for i in range(len(A)):
        temp = 0
        for j in range(len(x)):
            temp += A[i][j]*x[j]
        cons.append(temp)
    return cons

#function that returns the objective function of the QUBO formulation
def sp_QUBO(x, parameters):
    w, c, A = parameters[0], parameters[1], parameters[2]
    n = len(w)
    m = len(A)
    ret = 0
    for i in range(n):
        ret += w[i]*x[i]
    for j in range(m):
        temp = 0
        for i in range(n):
            temp += A[j][i] * x[i]
        temp = (temp - 1)**2
        ret += temp*c[j]
    return ret

#classical solution using guroby for the set partitioning problem
def sp_gurobi(w,A):
    """
    Classical solution using guroby for the set partitioning problem
    :param c: vector of length n
    :param A: matrix of size nxn
    :return: binary vector of length n
    """
    with gb.Env(empty=True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gb.Model(env=env) as model:
            model.Params.LogToConsole = 0
            n = len(w)
            
            x = model.addVars(n,vtype=gb.GRB.BINARY,name='x')
            
            model.setObjective(sp_objective(w,x),GRB.MINIMIZE)
            model.addConstrs(sp_constraint(A,x)[i] == 1 for i in range(len(A)))
            model.optimize()
            return model.x


    

#set partitioning hamiltonian
def hamiltonian(parameters):
    w, c, A = parameters[0], parameters[1], parameters[2]
    m = len(A)
    n = len(w)
    
    coeff = {tuple([i]):0 for i in range(n)}
    coeff[()] = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                coeff[(i, j)] = 0
    for i in range(n):
        coeff[()] += w[i] / 2
        coeff[tuple([i])] -= w[i] / 2
    
    for i in range(m):
        temp = 0
        for k in range(n):
            for j in range(n):
                #print(i, j, k, A.shape, c)
                
                a = c[i]*A[i][j]*A[i][k] / 4
                coeff[()] += a
                coeff[tuple([j])] -= a
                coeff[tuple([k])] -= a
                if j == k:
                    coeff[()] += a
                else:
                    coeff[tuple([j, k])] += a
            coeff[()] -= A[i][k] * c[i]
            coeff[tuple([k])] += A[i][k] * c[i]
        coeff[()] += c[i]
            
    return coeff
