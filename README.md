The codes available in this repository were utilized to generate the results presented in the research article entitled "The set partitioning problem in a quantum context," authored by Rafael Cacao, Lucas R. C. T. Cortez, Jackson Forner, Hamidreza Validi, Ismael R. de Farias Jr., and Illya V. Hicks.

Instructions for code usage:
The benchmark instances, originally provided by Svensson et al. [1], have been transformed to a format compatible with our codes. Each instance of the set partitioning problem comprises a vector of weights w, a matrix A representing the constraints, and a vector c representing the penalty coefficients associated with the QUBO formulation.

To read or generate random instances, please use the respective functions in generate_instance.py. By default, tight penalty coefficients are used, but you may modify the code to use a different type.

After defining the instances, they may be processed through the preprocessing function in order to apply reductions or utilized in the VQE algorithm.

If preprocessing is conducted, the output will comprise a new vector w and a new matrix A. Please ensure that the size of vector c matches the row dimension of matrix A (i.e., one penalty coefficient per row of the matrix, despite having the same value as implemented).

The VQE algorithm may be executed by calling the main function of vqe_qiskit.py. The arguments should be provided in the following order:

w (vector of weights, dimension m)
c (vector of penalty coefficients, dimension n)
A (matrix of constraints, dimension nxm)
repetitions (number of times the VQE circuit is repeated)
entanglement_strat (entanglement strategy used; default are linear, circular, and full; alternatively, you may provide a list of qubits to be entangled)
singleq_blocks (combination of single qubit gates to be applied on every qubit)
ent_blocks (combination of entanglement gates to be applied in every pair of entangled qubits)

The results will be written in a .txt file as follows:
[1] A dictionary of binary strings and the coefficients associated with each of them
[2] The expectation value of the energy
[3] Computational time associated with the VQE algorithm

If you have any questions or comments, please do not hesitate to contact us via the email address provided below.

Contact:
rafaelfariasc@gmail.com

Acknowledgments:

The authors would like to acknowledge the High-Performance Computing Center (HPCC) at Texas Tech University for providing computational resources that have contributed to the research results reported in this paper.

Svensson, M., Andersson, M., Grönkvist, M., Vikstål, P., Dubhashi, D., Ferrini, G., Johansson, G.,: A hybrid quantum-classical heuristic to solve large-scale integer linear programs. arXiv preprint arXiv:2103.15433 (2021).
