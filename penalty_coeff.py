import numpy as np
#define I as a list of constraints, P the list of partitions
#w is the dictionary of weights

def naive_penalty_coeff(w,A):
    return sum(w)


def tighter_penalty_coeff(w,A_matrix):
    A = A_matrix.copy()
    
    w_index = [i for i in range(len(w))]
    w_index = w_index.sort(key=lambda x: w[x])
    #sort A according to w
    for index, line in enumerate(A):
        A[index] = [x for _, x in sorted(zip(w, line))]
    #sort w
    w = sorted(w)    
    
    N = len(w)
    M = len(A)
    c = 0
    #create a dictionary for A with key each line position
    A_dict = {i: A[i] for i in range(len(A))}
    
    while(len(A_dict) > 0):
        #check if the empty set is in A_dict, and if it is, remove it
        
       
        #get indices of the max value in the last line
        if len(A_dict)>1:
            
            max_indices = [key for key in A_dict if A_dict[key][-1] != 0]
        else:
            max_indices = [key for key in A_dict]
            
        #check for ties
        if max_indices != []:
            if len(max_indices) > 1:
                count = 1
                while(len(max_indices) > 1):
                    #check if all elements with max_indices are equal
                    flag = False
                    for i in range(len(max_indices)):
                        for j in range(i+1,len(max_indices)):
                            if A_dict[max_indices[i]] == A_dict[max_indices[j]]:
                                flag = True
                    if flag:            
                        max_indices = [max_indices[0]]
                    else:
                        count += 1
                        
                        submatrix_dict = {i: A_dict[i] for i in max_indices}
                        #get the min of -i-th line
                        
                        last = [submatrix_dict[key][-count] for key in submatrix_dict]
                        min = np.min(last)
                        #get the indices of the min in the submatrix_dict
                        min_indices = [key for key in submatrix_dict if submatrix_dict[key][-count] == min]
                        
                        max_indices = min_indices
            index = max_indices[0]
            
            c = c + w[-1]
            #remove the line from A_dict
            A_dict.pop(index)
            w.pop(-1)
            #remove the column from A_dict
            for key in A_dict:
                A_dict[key].pop(len(A_dict[key])-1)
        else:
            w.pop(-1)
            #remove the column from A_dict
            for key in A_dict:
                A_dict[key].pop(len(A_dict[key])-1)
        if [] in A_dict.values():
            #return the key associated with the empty set
            for key in list(A_dict.keys()):
                if A_dict[key] == []:
                    A_dict.pop(key)
    return c