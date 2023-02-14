import numpy as np
import random as rd
import os
import set_partitioning as sp
import penalty_coeff as pc
import time as time


def generate_A(n,m):
    A = []
    
    for i in range(n):
        
        flag = True
        while(flag):
            temp = rd.randint(1,2**m - 1)
            #convert the integer to binary
            temp = bin(temp)[2:]
            #pad the binary number with zeros
            temp_b = temp.zfill(m)
            #convert in a list of size n
            temp = [int(x) for x in temp_b]
            #check if the list is already in A
            if temp not in A:
                A.append(temp)
                flag = False
    
    return A

def create_instance(id,n,m):
    flag = True
    while flag:
        A2 = generate_A(n,m)
        
        w = [rd.randint(1,m)*sum(A2[i]) for i in range(n)]
        A2 = np.array(A2).T.tolist()
        sol = sp.sp_gurobi(w,A2)
        if sol != "No solution":
            flag = False
    
    A = A2.copy()
    temp = pc.tighter_penalty_coeff(w,A)
    #temp = pc.naive_penalty_coeff(w,A2)
    c = [temp for i in range(m)]
    return w,c,A


def read_instance(fname):
    f = open(fname, "r")
    lines = f.readlines()
    size = int(lines[0])
    w = [int(x) for x in lines[1].split(",")]
    c = [int(x) for x in lines[2].split(",")]
    A = []
    for i in range(3,len(lines)):
        temp = lines[i][:-1].split(" ")
        temp = [int(x) for x in temp]
        A.append(temp)
    return w,c,A



