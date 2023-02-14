import set_partitioning as sp

global problem_parameters
global objective_function
global shots
global n, coeff, var_list
global expectation_evol


def init(w,c,A):
    global problem_parameters
    global objective_function
    global shots
    global n, coeff, var_list
    global expectation_evol

    problem_parameters = [w,c,A]
    objective_function = sp.sp_QUBO

    shots = 1000
    n = len(w)
    coeff = sp.hamiltonian(problem_parameters)
    var_list = list(coeff.keys())
    
    expectation_evol = []

def get_shots():
    return shots

def get_n():
    return n

def set_shots(shots_):
    global shots
    shots = shots_

def get_objective_function():
    return objective_function

def get_problem_parameters():
    return problem_parameters

def get_hamiltonian_variables():
    return var_list,coeff,n

def append_expectation(expectation):
    global expectation_evol
    expectation_evol.append(expectation)

def get_expectation_evol():
    return expectation_evol




