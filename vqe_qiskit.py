from sys import argv
from qiskit import *
from qiskit import Aer
from qiskit.opflow import X, Z, I
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
import set_partitioning as sp
import generate_instances as ins
import numpy as np
import globals as glb
import random as rd
import os
import time


#function that implements the Z-pauli matrices tensor product using numpy (Z_i)
def tensor_product(index,n):
    Z = [[1,0],[0,-1]]
    I = [[1,0],[0,1]]
    prod = [1]
    if index == []:
        for j in range(n):
            prod = np.kron(prod,I)
    else:
        for j in range(n):
            if j in index:
                prod = np.kron(prod,Z)
            else:
                prod = np.kron(prod,I)
               
    return prod

#function that given var and coeff, calculates the matrix representation of the hamiltonian
def hamiltonian_toMatrix(n, coeff):
    H = np.zeros((2**(n),2**(n)))
    for i in coeff.keys():
        H += coeff[i] * tensor_product(i,n)
    return H

def operator_pauli(parameters):
    coeff = sp.hamiltonian(parameters)
    n = glb.get_n()
    var_list = list(coeff.keys())
    operator_prob = 0
    for i in range(len(var_list)):    
        temp = 1
        for j in range(n):
            if j in var_list[i]:
                temp ^= Z
            else:
                temp ^= I
        if coeff[var_list[i]] == 0.0:
            continue
        else:
            operator_prob += temp*coeff[var_list[i]]
    
    return operator_prob

def entanglement_map(A):
    #define entanglement map for partitions that are complementary (that did not violate the constraints)
    A = np.matrix(A)
    A = A.transpose()
    m,n = A.shape
    map = []
    for i in range(m):
        for j in range(m):
            if i != j:
                flag = False
                for k in range(n):
                    if A[i,k] == 1 and A[j,k] == 1:
                        flag = True
                if flag:
                    map.append((i,j))
    return map
            
def run(w,c,A,repetitions,entanglement_strat,singleq_blocks,ent_blocks):
    seed = 50
    algorithm_globals.random_seed = seed
    qi = QuantumInstance(Aer.get_backend('qasm_simulator'), seed_transpiler=seed, seed_simulator=seed,shots=20000)
    #ansatz = vqe.vqe_circuit_full
    ansatz = TwoLocal(rotation_blocks=singleq_blocks, entanglement_blocks=ent_blocks,reps=repetitions,entanglement=entanglement_strat)
    glb.init(w,c,A)
    slsqp = COBYLA(maxiter=10000,tol=1e-6)
    alg = VQE(ansatz,optimizer= slsqp, quantum_instance= qi)
    result = alg.compute_minimum_eigenvalue(operator_pauli(glb.get_problem_parameters()))

    return result

def main(instance,read_directory,reps,entanglement_strat,s_gate,e_gate):
    w,c,A = ins.read_instance(read_directory + instance)
    
    if entanglement_strat == 'structured':
        ent = entanglement_map(A)
    else:
        ent = entanglement_strat
    result = run(w,c,A,int(reps),entanglement_strat=ent,singleq_blocks=s_gate,ent_blocks=e_gate)
    return result


if __name__ == "__main__":
    main(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6])

    
    