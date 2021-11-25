#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random, re
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, BasicAer, IBMQ, execute
from qiskit.tools.visualization import plot_histogram
from collections import defaultdict
import itertools
import pycosat
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


clause_length = 6


# In[3]:


def tcnfgen(n,k,horn=1):
    cnf = []
    def unique(l,k):
        t = random.randint(1,n)
        while(t in l):
            t = random.randint(1,n)
        return t
    r = (lambda : random.randint(0,1))
    def r_to_sign(x):
        if r() == 1:
            return x
        else:
            return -x
    for i in range(k):
        x = unique([],n)
        y = unique([x],n)
        z = unique([x, y],n)
        if horn:
            cnf.append([x, -y,-z])
        else:
            cnf.append([r_to_sign(x), r_to_sign(y),r_to_sign(z)])
    return cnf


# In[4]:


def create_assignment(n):
    assignment = []
    for i in range(n):
        a = random.choice([-i-1, i+1])
        assignment.append(a)
    return assignment


# In[5]:


def create_not_to_have_clauses(assignment):
    not_to_have_clauses = [i*(-1) for i in assignment]
    possible_clauses = itertools.combinations(not_to_have_clauses,3)
    return possible_clauses


# In[6]:


def convert(possible_clauses):
    new_possible_clauses = []
    for comb in possible_clauses:
        new_clause = []
        for element in comb:
            new_clause.append(element)
        new_possible_clauses.append(new_clause)
    return new_possible_clauses


# In[7]:


def create_CNF(n, k):
    new_line = []
    line = tcnfgen(n, k)
    for clause in line:
        new_line.append(sorted(clause, key = abs))
    return new_line


# In[8]:


def cal_average(int_list):
    return sum(int_list) / len(int_list)


# In[9]:


def clause_variables(clause):
    clauseToschoning1 = []
    for i in range (0, len(clause)):
        clauseToschoning1.append(abs(int(clause[i])))
    return clauseToschoning1


# In[10]:


def findZeroClauseN(mycircuit, clause):
    clauseToschoning1 = clause_variables(clause)
    for i in range(3):
         if (int(clause[i])<0):
            mycircuit.x(abs(int(clause[i])))
 
    for i in clauseToschoning1: 
        mycircuit.x(i)
        
    mycircuit.mcx(clauseToschoning1,[0])
    mycircuit.x([0])

    for i in clauseToschoning1:
        mycircuit.x(i)
            
    for i in range(3):
        if (int(clause[i])<0):
            mycircuit.x(abs(int(clause[i])))
        
    
    return mycircuit


# In[11]:


def controller(fzc, mycircuit, qreg, n, variables):
    mycircuit.append(fzc,qargs=qreg)
    r = random.choice(variables)
    mycircuit.x(qreg[0])
    mycircuit.cx(qreg[0],qreg[r])
    mycircuit.x(qreg[0])
    mycircuit.barrier()
    mycircuit.reset(qreg[0])


# In[90]:


def schoning_2(mycircuit, qreg, iteration, n, line, fzc_array):
    for i in range (iteration): 
        r = random.randint(0,len(line)-1)
        variables = clause_variables(line[r])
        controller(fzc_array[r],mycircuit, qreg, n, variables)


# In[13]:


def schoning(mycircuit, qreg, iteration, n, line, fzc_array):
    for i in range (iteration): 
        for j in range(len(line)):
            variables = clause_variables(line[j])
            controller(fzc_array[j],mycircuit, qreg, n, variables)


# In[14]:


def back_to_initial(outcome_reversed):
    back_list = []
    for i in range(1, len(outcome_reversed)):
        if outcome_reversed[i] == '0':
            back_list.append(0 - i)
        else:
            back_list.append(i)
    return back_list


# In[15]:


def calculate_accuracy(sol_list, tup_list):
    counter = 0
    for sol in tup_list:
        if sol[0] in sol_list:
            counter += sol[1]
    return counter/1000


# In[16]:


def schoning_calc_count(n, line):
    count_list = []
    for i in range(1000):
        assignment = create_assignment(n)
        count = 1
        for deneme in range(3*n):
            booli = True   
            impossible_clauses = create_not_to_have_clauses(assignment)
            converted = convert(impossible_clauses)
            for impossible_clause in converted:
                if sorted(impossible_clause, key = abs) in line:
                    booli = False
                    value_negated = random.choice(impossible_clause)
                    for a in range(len(assignment)):
                        if abs(assignment[a]) == abs(value_negated):
                            assignment[a] = assignment[a]*(-1)
                    break
            if booli == True:
                count_list.append(count)
                break
            count += 1
    return cal_average(count_list)


# In[91]:


def quantum_Run(step, n, qubit_count, maxN, line):
    accuracy_list = []
    solution_list = []
    for sol in pycosat.itersolve(new_line):
        solution_list.append(sorted(sol, key = abs))
    fzc_array = []
    for next_line in line:
        fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())

    for j in range(1, int(step) + 1):
        qreg = QuantumRegister(maxN)
        creg = ClassicalRegister(maxN)
        mycircuit = QuantumCircuit(qreg, creg)
        tuple_list = []

        for i in range(1, qubit_count):
            mycircuit.h(qreg[i]) 

        schoning_2(mycircuit, qreg, j, n, line, fzc_array)

        for i in range (qubit_count):
            mycircuit.measure(qreg[i], creg[i])

        job = execute(mycircuit, Aer.get_backend('qasm_simulator'), shots=1000)
        #job = execute(mycircuit, backend= simulator_backend, shots=20)
        counts = job.result().get_counts(mycircuit)


            # print the reverse of the outcome
        for outcome in counts:
            reverse_outcome = ''
            for i in outcome:
                reverse_outcome = i + reverse_outcome
            reverse_outcome = back_to_initial(reverse_outcome)
            tuple_list.append((reverse_outcome,counts[outcome]))
            
        accuracy_list.append(calculate_accuracy(solution_list, tuple_list))
    return accuracy_list[-1]


# In[18]:


def schoning_Run(step, n, line):
    count_list = defaultdict(int)
    for i in range(1000):
        assignment = create_assignment(n)
        count = 1
        for deneme in range(int(step)):
            booli = True   
            impossible_clauses = create_not_to_have_clauses(assignment)
            converted = convert(impossible_clauses)
            for impossible_clause in converted:
                if sorted(impossible_clause, key = abs) in line:
                    booli = False
                    value_negated = random.choice(impossible_clause)
                    for a in range(len(assignment)):
                        if abs(assignment[a]) == abs(value_negated):
                            assignment[a] = assignment[a]*(-1)
                    break
            if booli == True:
                count_list[str(assignment)] += 1
                break
            count += 1
    return sum(count_list.values())/1000


# In[82]:


def schoning_Run_2(step, n, line):
    count_list = defaultdict(int)
    sol_list = []
    for sol in pycosat.itersolve(new_line):
            sol_list.append(sol)
    for i in range(1000):
        assignment = create_assignment(n)  
        for deneme in range(int(step)): 
            #print(i, " presents the i value", deneme, assignment)
            for j in range(len(line)):
                impossible_clauses = create_not_to_have_clauses(assignment)
                converted = convert(impossible_clauses)
                #print("converted", converted)
                if line[j] in converted:
                    booli = False
                    value_negated = random.choice(line[j])
                    for a in range(len(assignment)):
                        if abs(assignment[a]) == abs(value_negated):
                            assignment[a] = assignment[a]*(-1)
              
        if assignment in sol_list:
            count_list[str(assignment)] += 1
        
    return sum(count_list.values())/1000


# In[89]:


def schoning_Run_3(step, n, line):
    count_list = defaultdict(int)
    sol_list = []
    for sol in pycosat.itersolve(new_line):
            sol_list.append(sol)
    for i in range(1000):
        assignment = create_assignment(n)  
        for deneme in range(int(step)): 
            #print(i, " presents the i value", deneme, assignment)
            r = random.randint(0, len(line)-1)
            impossible_clauses = create_not_to_have_clauses(assignment)
            converted = convert(impossible_clauses)
            #print("converted", converted)
            if line[r] in converted:
                booli = False
                value_negated = random.choice(line[r])
                for a in range(len(assignment)):
                    if abs(assignment[a]) == abs(value_negated):
                        assignment[a] = assignment[a]*(-1)

        if assignment in sol_list:
            count_list[str(assignment)] += 1
        
    return sum(count_list.values())/1000


# In[92]:


def compare_accuracies(n, q_count, maxN, line, step):
    sch_avg = schoning_Run_3(step, n, line)
    quant_avg = quantum_Run(step, n, q_count, maxN, line)
    return sch_avg, quant_avg


# In[93]:


n = 5
k = 18
qubit_count = n+1
maxN = qubit_count

new_line = create_CNF(n,k)
#average_count = schoning_calc_count(n, new_line)
#compare_accuracies(n, k, qubit_count, maxN, new_line, average_count)


# In[94]:


for sol in pycosat.itersolve(new_line):
    print(sol)


# In[98]:


list_of_schons = []
list_of_quants = []
for j in range(50):
    schoning_list = []
    quantum_list = []
    for i in range(1, 10):
        schoning_list.append(compare_accuracies(n, qubit_count, maxN, new_line, i)[0])
        quantum_list.append(compare_accuracies(n, qubit_count, maxN, new_line, i)[1])
    list_of_schons.append(schoning_list)
    list_of_quants.append(quantum_list)


# In[71]:


for x in zip(*list_of_schons):
    print(x)


# In[102]:


schon_avg = (y/len(list_of_schons) for y in (sum(x) for x in zip(*list_of_schons)))
quant_avg = (y/len(list_of_quants) for y in (sum(x) for x in zip(*list_of_quants)))


# In[68]:


schon_max = (y for y in (max(x) for x in zip(*list_of_schons)))
quant_max = (y for y in (max(x) for x in zip(*list_of_quants)))


# In[69]:


print(list(schon_max))


# In[70]:


print(list(quant_max))


# In[25]:


#print(list(quant_avg))


# In[103]:


f = plt.figure()
plt.plot(range(1,10), list(schon_avg), label = "Schöning Algorithm")
plt.plot(range(1,10), list(quant_avg), label = "Quantum Algorithm")
plt.xlabel("Number Of Iterations")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

f.savefig("output_3.pdf", bbox_inches = "tight")


# In[ ]:




