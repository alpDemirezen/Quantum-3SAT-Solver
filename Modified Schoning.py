#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random, re
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, BasicAer, IBMQ, execute
from qiskit.tools.visualization import plot_histogram
from collections import defaultdict
import pycosat
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


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


# In[ ]:


line=tcnfgen(3,7)


# In[ ]:


count = 0
for sol in pycosat.itersolve(line):
        count += 1
print(count)


# In[ ]:


ortalama = 4754/2**14


# In[ ]:


print(ortalama)


# In[ ]:


clauselength = 6 


# In[3]:


def clause_variables(clause):
    clauseToschoning1 = []
    for i in range (0, len(clause)):
        clauseToschoning1.append(abs(int(clause[i])))
    return clauseToschoning1


# In[4]:


def findZeroClauseN(mycircuit, clause):
    clauseToschoning1 = clause_variables(clause)
    print(clauseToschoning1)
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


# In[5]:


"""fzc_array = []
for i in range (len(nextLine)):
    fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),CNF_1[f'clause{i+1}']).to_gate())"""


# In[6]:


def controller(fzc, mycircuit, qreg, n, variables):
    mycircuit.append(fzc,qargs=qreg)
    r = random.choice(variables)
    mycircuit.x(qreg[0])
    mycircuit.cx(qreg[0],qreg[r])
    mycircuit.barrier()
    mycircuit.reset(qreg[0])


# In[7]:


def schoning(mycircuit,qreg,iteration, n):
    for i in range (iteration):  
        for j in range (len(nextLine)):
            variables = clause_variables(nextLine[j])
            controller(fzc_array[random.randint(0,len(nextLine)-1)],mycircuit,qreg,n, variables)


# In[8]:


def back_to_initial(outcome_reversed):
    back_list = []
    for i in range(1, len(outcome_reversed)):
        if outcome_reversed[i] == '0':
            back_list.append(0 - i)
        else:
            back_list.append(i)
    return back_list


# In[9]:


def calculate_accuracy(solution_list, tuple_list):
    counter = 0
    for sol in tuple_list:
        if sol[0] in solution_list:
            counter += sol[1]
    return counter/1000


# In[ ]:


"""qreg = QuantumRegister(maxN)
creg = ClassicalRegister(maxN)
mycircuit = QuantumCircuit(qreg, creg)
tuple_list = []

print(CNF_1)
for i in range(1, qubit_count):
    mycircuit.h(qreg[i]) 

schoning(mycircuit, qreg, 1, n)

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
    print(reverse_outcome, "is observed", counts[outcome], "times")

print(calculate_accuracy(solution_list, tuple_list))
    
print("\n")
print("next_iteration")"""


# In[10]:


qubit_count = 4
nextLine = [[1,2,3],[1,2,-3],[1,-2,3],[1,-2,-3],[-1,2,3],[-1,2,-3],[-1,-2,3]]
maxN = 4

solution_list = []
for sol in pycosat.itersolve(nextLine):
    solution_list.append(sol)
    
fzc_array = []
for next_line in nextLine:
    fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())
    
for j in range(1,3):
    qreg = QuantumRegister(maxN)
    creg = ClassicalRegister(maxN)
    mycircuit = QuantumCircuit(qreg, creg)
    tuple_list = []

    for i in range(1, qubit_count):
        mycircuit.h(qreg[i]) 

    schoning(mycircuit, qreg, j, 3)

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
        print(reverse_outcome, "is observed", counts[outcome], "times")


    print("\n")
    print("next_iteration", j)


# In[ ]:


print(solution_list)


# In[ ]:


list_of_lists = []
list_of_CNFs = []
n_list = [9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14]
k_list = [6,7,8,9,6,7,8,9,6,7,8,9,6,7,8,9,6,7,8,9,6,7,8,9]
label_list=["9,6","9,7","9,8","9,9","10,6","10,7","10,8","10,9","11,6","11,7","11,8","11,9","12,6","12,7","12,8","12,9","13,6","13,7","13,8","13,9","14,6","14,7","14,8","14,9"]
for n,k in zip(n_list, k_list):
    qubit_count = n+1
    nextLine = tcnfgen(n,k)
    list_of_CNFs.append(nextLine)
    maxN = n+1
    accuracy_list = []
    CNF_1 = defaultdict(lambda: 0)
    
    solution_list = []
    for sol in pycosat.itersolve(nextLine):
        solution_list.append(sol)

    
    fzc_array = []
    for next_line in nextLine:
        fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())
    
    for j in range(1,10):
        qreg = QuantumRegister(maxN)
        creg = ClassicalRegister(maxN)
        mycircuit = QuantumCircuit(qreg, creg)
        tuple_list = []

        for i in range(1, qubit_count):
            mycircuit.h(qreg[i]) 

        schoning(mycircuit, qreg, j, n)

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
            print(reverse_outcome, "is observed", counts[outcome], "times")


        print("\n")
        print("next_iteration", j)
        accuracy_list.append(calculate_accuracy(solution_list, tuple_list))
        
    
    list_of_lists.append(accuracy_list)


# In[ ]:


for n,k in zip(n_list, k_list):
    qubit_count = n+1
    nextLine = tcnfgen(n,k)
    list_of_CNFs.append(nextLine)
    maxN = n+1
    accuracy_list = []
    CNF_1 = defaultdict(lambda: 0)
    
    solution_list = []
    for sol in pycosat.itersolve(nextLine):
        solution_list.append(sol)

    
    fzc_array = []
    for next_line in nextLine:
        fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())
    
    for j in range(1,8):
        qreg = QuantumRegister(maxN)
        creg = ClassicalRegister(maxN)
        mycircuit = QuantumCircuit(qreg, creg)
        tuple_list = []

        for i in range(1, qubit_count):
            mycircuit.h(qreg[i]) 

        schoning(mycircuit, qreg, j, n)

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
            print(reverse_outcome, "is observed", counts[outcome], "times")


        print("\n")
        print("next_iteration", j)
        accuracy_list.append(calculate_accuracy(solution_list, tuple_list))
        
    
    list_of_lists.append(accuracy_list)


# In[ ]:


for n,k in zip(n_list, k_list):
    qubit_count = n+1
    nextLine = tcnfgen(n,k)
    list_of_CNFs.append(nextLine)
    maxN = n+1
    accuracy_list = []
    CNF_1 = defaultdict(lambda: 0)
    
    solution_list = []
    for sol in pycosat.itersolve(nextLine):
        solution_list.append(sol)
 
    
    fzc_array = []
    for next_line in nextLine:
        fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())
    
    for j in range(1,6):
        qreg = QuantumRegister(maxN)
        creg = ClassicalRegister(maxN)
        mycircuit = QuantumCircuit(qreg, creg)
        tuple_list = []

        for i in range(1, qubit_count):
            mycircuit.h(qreg[i]) 

        schoning(mycircuit, qreg, j, n)

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
            print(reverse_outcome, "is observed", counts[outcome], "times")


        print("\n")
        print("next_iteration", j)
        accuracy_list.append(calculate_accuracy(solution_list, tuple_list))
        
    
    list_of_lists.append(accuracy_list)


# In[ ]:


for n,k in zip(n_list, k_list):
    qubit_count = n+1
    nextLine = tcnfgen(n,k)
    list_of_CNFs.append(nextLine)
    maxN = n+1
    accuracy_list = []
    CNF_1 = defaultdict(lambda: 0)
    
    solution_list = []
    for sol in pycosat.itersolve(nextLine):
        solution_list.append(sol)

    
    fzc_array = []
    for next_line in nextLine:
        fzc_array.append(findZeroClauseN(QuantumCircuit(qubit_count),next_line).to_gate())
    
    for j in range(1,4):
        qreg = QuantumRegister(maxN)
        creg = ClassicalRegister(maxN)
        mycircuit = QuantumCircuit(qreg, creg)
        tuple_list = []

        for i in range(1, qubit_count):
            mycircuit.h(qreg[i]) 

        schoning(mycircuit, qreg, j, n)

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
            print(reverse_outcome, "is observed", counts[outcome], "times")


        print("\n")
        print("next_iteration", j)
        accuracy_list.append(calculate_accuracy(solution_list, tuple_list))
        
    
    list_of_lists.append(accuracy_list)


# In[ ]:


for i,labels in zip(range(4),label_list[0:4]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(4,8),label_list[4:8]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(8,12),label_list[8:12]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(12,16),label_list[12:16]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(16,20),label_list[16:20]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(20,24),label_list[20:24]):
    plt.plot(range(1,10), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


for i,labels in zip(range(24,28),label_list[0:4]):
    plt.plot(range(1,8), list_of_lists[i],label = labels)
plt.legend()
plt.show()


# In[ ]:


data = {'Variable Count':[],'Clause Count':[],'Accuracy':[]}


# In[ ]:


df = pd.DataFrame(data = data)
df


# In[ ]:


new_row = {'Variable Count':n_list[0],'Clause Count':k_list[0],'Accuracy':list_of_lists[0][8]}
new_row_2 = {'Variable Count':n_list[1],'Clause Count':k_list[1],'Accuracy':list_of_lists[1][8]}
new_row_3 = {'Variable Count':n_list[2],'Clause Count':k_list[2],'Accuracy':list_of_lists[2][8]}
new_row_4 = {'Variable Count':n_list[3],'Clause Count':k_list[3],'Accuracy':list_of_lists[3][8]}
new_row_5 = {'Variable Count':n_list[4],'Clause Count':k_list[4],'Accuracy':list_of_lists[4][8]}

df = df.append(new_row, ignore_index=True)
df = df.append(new_row_2, ignore_index=True)
df = df.append(new_row_3, ignore_index=True)
df = df.append(new_row_4, ignore_index=True)
df = df.append(new_row_5, ignore_index=True)

df


# In[ ]:


#df.drop(df.index, inplace=True)
#df


# In[ ]:


new_row_6 = {'Variable Count':n_list[5],'Clause Count':k_list[5],'Accuracy':list_of_lists[5][8]}
new_row_7 = {'Variable Count':n_list[6],'Clause Count':k_list[6],'Accuracy':list_of_lists[6][8]}
new_row_8 = {'Variable Count':n_list[7],'Clause Count':k_list[7],'Accuracy':list_of_lists[7][8]}
new_row_9 = {'Variable Count':n_list[8],'Clause Count':k_list[8],'Accuracy':list_of_lists[8][8]}
new_row_10 = {'Variable Count':n_list[9],'Clause Count':k_list[9],'Accuracy':list_of_lists[9][8]}
new_row_11 = {'Variable Count':n_list[10],'Clause Count':k_list[10],'Accuracy':list_of_lists[10][8]}
new_row_12 = {'Variable Count':n_list[11],'Clause Count':k_list[11],'Accuracy':list_of_lists[11][8]}
new_row_13 = {'Variable Count':n_list[12],'Clause Count':k_list[12],'Accuracy':list_of_lists[12][8]}
new_row_14 = {'Variable Count':n_list[13],'Clause Count':k_list[13],'Accuracy':list_of_lists[13][8]}
new_row_15 = {'Variable Count':n_list[14],'Clause Count':k_list[14],'Accuracy':list_of_lists[14][8]}
new_row_16 = {'Variable Count':n_list[15],'Clause Count':k_list[15],'Accuracy':list_of_lists[15][8]}
new_row_17 = {'Variable Count':n_list[16],'Clause Count':k_list[16],'Accuracy':list_of_lists[16][8]}
new_row_18 = {'Variable Count':n_list[17],'Clause Count':k_list[17],'Accuracy':list_of_lists[17][8]}
new_row_19 = {'Variable Count':n_list[18],'Clause Count':k_list[18],'Accuracy':list_of_lists[18][8]}
new_row_20 = {'Variable Count':n_list[19],'Clause Count':k_list[19],'Accuracy':list_of_lists[19][8]}
new_row_21 = {'Variable Count':n_list[20],'Clause Count':k_list[20],'Accuracy':list_of_lists[20][8]}
new_row_22 = {'Variable Count':n_list[21],'Clause Count':k_list[21],'Accuracy':list_of_lists[21][8]}
new_row_23 = {'Variable Count':n_list[22],'Clause Count':k_list[22],'Accuracy':list_of_lists[22][8]}
new_row_24 = {'Variable Count':n_list[23],'Clause Count':k_list[23],'Accuracy':list_of_lists[23][8]}


df = df.append(new_row_6, ignore_index=True)
df = df.append(new_row_7, ignore_index=True)
df = df.append(new_row_8, ignore_index=True)
df = df.append(new_row_9, ignore_index=True)
df = df.append(new_row_10, ignore_index=True)
df = df.append(new_row_11, ignore_index=True)
df = df.append(new_row_12, ignore_index=True)
df = df.append(new_row_13, ignore_index=True)
df = df.append(new_row_14, ignore_index=True)
df = df.append(new_row_15, ignore_index=True)
df = df.append(new_row_16, ignore_index=True)
df = df.append(new_row_17, ignore_index=True)
df = df.append(new_row_18, ignore_index=True)
df = df.append(new_row_19, ignore_index=True)
df = df.append(new_row_20, ignore_index=True)
df = df.append(new_row_21, ignore_index=True)
df = df.append(new_row_22, ignore_index=True)
df = df.append(new_row_23, ignore_index=True)
df = df.append(new_row_24, ignore_index=True)

df


# In[ ]:


new_row_25 = {'Variable Count':n_list[0],'Clause Count':k_list[0],'Accuracy':list_of_lists[24][6]}
new_row_26 = {'Variable Count':n_list[1],'Clause Count':k_list[1],'Accuracy':list_of_lists[25][6]}
new_row_27 = {'Variable Count':n_list[2],'Clause Count':k_list[2],'Accuracy':list_of_lists[26][6]}
new_row_28 = {'Variable Count':n_list[3],'Clause Count':k_list[3],'Accuracy':list_of_lists[27][6]}
new_row_29 = {'Variable Count':n_list[4],'Clause Count':k_list[4],'Accuracy':list_of_lists[28][6]}
new_row_30 = {'Variable Count':n_list[5],'Clause Count':k_list[5],'Accuracy':list_of_lists[29][6]}
new_row_31 = {'Variable Count':n_list[6],'Clause Count':k_list[6],'Accuracy':list_of_lists[30][6]}
new_row_32 = {'Variable Count':n_list[7],'Clause Count':k_list[7],'Accuracy':list_of_lists[31][6]}
new_row_33 = {'Variable Count':n_list[8],'Clause Count':k_list[8],'Accuracy':list_of_lists[32][6]}
new_row_34 = {'Variable Count':n_list[9],'Clause Count':k_list[9],'Accuracy':list_of_lists[33][6]}
new_row_35 = {'Variable Count':n_list[10],'Clause Count':k_list[10],'Accuracy':list_of_lists[34][6]}
new_row_36 = {'Variable Count':n_list[11],'Clause Count':k_list[11],'Accuracy':list_of_lists[35][6]}
new_row_37 = {'Variable Count':n_list[12],'Clause Count':k_list[12],'Accuracy':list_of_lists[36][6]}
new_row_38 = {'Variable Count':n_list[13],'Clause Count':k_list[13],'Accuracy':list_of_lists[37][6]}
new_row_39 = {'Variable Count':n_list[14],'Clause Count':k_list[14],'Accuracy':list_of_lists[38][6]}
new_row_40 = {'Variable Count':n_list[15],'Clause Count':k_list[15],'Accuracy':list_of_lists[39][6]}
new_row_41 = {'Variable Count':n_list[16],'Clause Count':k_list[16],'Accuracy':list_of_lists[40][6]}
new_row_42 = {'Variable Count':n_list[17],'Clause Count':k_list[17],'Accuracy':list_of_lists[41][6]}
new_row_43 = {'Variable Count':n_list[18],'Clause Count':k_list[18],'Accuracy':list_of_lists[42][6]}
new_row_44 = {'Variable Count':n_list[19],'Clause Count':k_list[19],'Accuracy':list_of_lists[43][6]}
new_row_45 = {'Variable Count':n_list[20],'Clause Count':k_list[20],'Accuracy':list_of_lists[44][6]}
new_row_46 = {'Variable Count':n_list[21],'Clause Count':k_list[21],'Accuracy':list_of_lists[45][6]}
new_row_47 = {'Variable Count':n_list[22],'Clause Count':k_list[22],'Accuracy':list_of_lists[46][6]}
new_row_48 = {'Variable Count':n_list[23],'Clause Count':k_list[23],'Accuracy':list_of_lists[47][6]}



df = df.append(new_row_25, ignore_index=True)
df = df.append(new_row_26, ignore_index=True)
df = df.append(new_row_27, ignore_index=True)
df = df.append(new_row_28, ignore_index=True)
df = df.append(new_row_29, ignore_index=True)
df = df.append(new_row_30, ignore_index=True)
df = df.append(new_row_31, ignore_index=True)
df = df.append(new_row_32, ignore_index=True)
df = df.append(new_row_33, ignore_index=True)
df = df.append(new_row_34, ignore_index=True)
df = df.append(new_row_35, ignore_index=True)
df = df.append(new_row_36, ignore_index=True)
df = df.append(new_row_37, ignore_index=True)
df = df.append(new_row_38, ignore_index=True)
df = df.append(new_row_39, ignore_index=True)
df = df.append(new_row_40, ignore_index=True)
df = df.append(new_row_41, ignore_index=True)
df = df.append(new_row_42, ignore_index=True)
df = df.append(new_row_43, ignore_index=True)
df = df.append(new_row_44, ignore_index=True)
df = df.append(new_row_45, ignore_index=True)
df = df.append(new_row_46, ignore_index=True)
df = df.append(new_row_47, ignore_index=True)
df = df.append(new_row_48, ignore_index=True)


# In[ ]:


df


# In[ ]:


new_df = pd.DataFrame(data = data)


# In[ ]:


newer_row_1 = {'Variable Count':n_list[0],'Clause Count':k_list[0],'Accuracy':list_of_lists[0][4]}
newer_row_2 = {'Variable Count':n_list[1],'Clause Count':k_list[1],'Accuracy':list_of_lists[1][4]}
newer_row_3 = {'Variable Count':n_list[2],'Clause Count':k_list[2],'Accuracy':list_of_lists[2][4]}
newer_row_4 = {'Variable Count':n_list[3],'Clause Count':k_list[3],'Accuracy':list_of_lists[3][4]}
newer_row_5 = {'Variable Count':n_list[4],'Clause Count':k_list[4],'Accuracy':list_of_lists[4][4]}
newer_row_6 = {'Variable Count':n_list[5],'Clause Count':k_list[5],'Accuracy':list_of_lists[5][4]}
newer_row_7 = {'Variable Count':n_list[6],'Clause Count':k_list[6],'Accuracy':list_of_lists[6][4]}
newer_row_8 = {'Variable Count':n_list[7],'Clause Count':k_list[7],'Accuracy':list_of_lists[7][4]}
newer_row_9 = {'Variable Count':n_list[8],'Clause Count':k_list[8],'Accuracy':list_of_lists[8][4]}
newer_row_10 = {'Variable Count':n_list[9],'Clause Count':k_list[9],'Accuracy':list_of_lists[9][4]}
newer_row_11 = {'Variable Count':n_list[10],'Clause Count':k_list[10],'Accuracy':list_of_lists[10][4]}
newer_row_12 = {'Variable Count':n_list[11],'Clause Count':k_list[11],'Accuracy':list_of_lists[11][4]}
newer_row_13 = {'Variable Count':n_list[12],'Clause Count':k_list[12],'Accuracy':list_of_lists[12][4]}
newer_row_14 = {'Variable Count':n_list[13],'Clause Count':k_list[13],'Accuracy':list_of_lists[13][4]}
newer_row_15 = {'Variable Count':n_list[14],'Clause Count':k_list[14],'Accuracy':list_of_lists[14][4]}
newer_row_16 = {'Variable Count':n_list[15],'Clause Count':k_list[15],'Accuracy':list_of_lists[15][4]}
newer_row_17 = {'Variable Count':n_list[16],'Clause Count':k_list[16],'Accuracy':list_of_lists[16][4]}
newer_row_18 = {'Variable Count':n_list[17],'Clause Count':k_list[17],'Accuracy':list_of_lists[17][4]}
newer_row_19 = {'Variable Count':n_list[18],'Clause Count':k_list[18],'Accuracy':list_of_lists[18][4]}
newer_row_20 = {'Variable Count':n_list[19],'Clause Count':k_list[19],'Accuracy':list_of_lists[19][4]}
newer_row_21 = {'Variable Count':n_list[20],'Clause Count':k_list[20],'Accuracy':list_of_lists[20][4]}
newer_row_22 = {'Variable Count':n_list[21],'Clause Count':k_list[21],'Accuracy':list_of_lists[21][4]}
newer_row_23 = {'Variable Count':n_list[22],'Clause Count':k_list[22],'Accuracy':list_of_lists[22][4]}
newer_row_24 = {'Variable Count':n_list[23],'Clause Count':k_list[23],'Accuracy':list_of_lists[23][4]}



new_df = new_df.append(newer_row_1, ignore_index=True)
new_df = new_df.append(newer_row_2, ignore_index=True)
new_df = new_df.append(newer_row_3, ignore_index=True)
new_df = new_df.append(newer_row_4, ignore_index=True)
new_df = new_df.append(newer_row_5, ignore_index=True)
new_df = new_df.append(newer_row_6, ignore_index=True)
new_df = new_df.append(newer_row_7, ignore_index=True)
new_df = new_df.append(newer_row_8, ignore_index=True)
new_df = new_df.append(newer_row_9, ignore_index=True)
new_df = new_df.append(newer_row_10, ignore_index=True)
new_df = new_df.append(newer_row_11, ignore_index=True)
new_df = new_df.append(newer_row_12, ignore_index=True)
new_df = new_df.append(newer_row_13, ignore_index=True)
new_df = new_df.append(newer_row_14, ignore_index=True)
new_df = new_df.append(newer_row_15, ignore_index=True)
new_df = new_df.append(newer_row_16, ignore_index=True)
new_df = new_df.append(newer_row_17, ignore_index=True)
new_df = new_df.append(newer_row_18, ignore_index=True)
new_df = new_df.append(newer_row_19, ignore_index=True)
new_df = new_df.append(newer_row_20, ignore_index=True)
new_df = new_df.append(newer_row_21, ignore_index=True)
new_df = new_df.append(newer_row_22, ignore_index=True)
new_df = new_df.append(newer_row_23, ignore_index=True)
new_df = new_df.append(newer_row_24, ignore_index=True)

new_df


# In[ ]:


newer_row_25 = {'Variable Count':n_list[0],'Clause Count':k_list[0],'Accuracy':list_of_lists[24][2]}
newer_row_26 = {'Variable Count':n_list[1],'Clause Count':k_list[1],'Accuracy':list_of_lists[25][2]}
newer_row_27 = {'Variable Count':n_list[2],'Clause Count':k_list[2],'Accuracy':list_of_lists[26][2]}
newer_row_28 = {'Variable Count':n_list[3],'Clause Count':k_list[3],'Accuracy':list_of_lists[27][2]}
newer_row_29 = {'Variable Count':n_list[4],'Clause Count':k_list[4],'Accuracy':list_of_lists[28][2]}
newer_row_30 = {'Variable Count':n_list[5],'Clause Count':k_list[5],'Accuracy':list_of_lists[29][2]}
newer_row_31 = {'Variable Count':n_list[6],'Clause Count':k_list[6],'Accuracy':list_of_lists[30][2]}
newer_row_32 = {'Variable Count':n_list[7],'Clause Count':k_list[7],'Accuracy':list_of_lists[31][2]}
newer_row_33 = {'Variable Count':n_list[8],'Clause Count':k_list[8],'Accuracy':list_of_lists[32][2]}
newer_row_34 = {'Variable Count':n_list[9],'Clause Count':k_list[9],'Accuracy':list_of_lists[33][2]}
newer_row_35 = {'Variable Count':n_list[10],'Clause Count':k_list[10],'Accuracy':list_of_lists[34][2]}
newer_row_36 = {'Variable Count':n_list[11],'Clause Count':k_list[11],'Accuracy':list_of_lists[35][2]}
newer_row_37 = {'Variable Count':n_list[12],'Clause Count':k_list[12],'Accuracy':list_of_lists[36][2]}
newer_row_38 = {'Variable Count':n_list[13],'Clause Count':k_list[13],'Accuracy':list_of_lists[37][2]}
newer_row_39 = {'Variable Count':n_list[14],'Clause Count':k_list[14],'Accuracy':list_of_lists[38][2]}
newer_row_40 = {'Variable Count':n_list[15],'Clause Count':k_list[15],'Accuracy':list_of_lists[39][2]}
newer_row_41 = {'Variable Count':n_list[16],'Clause Count':k_list[16],'Accuracy':list_of_lists[40][2]}
newer_row_42 = {'Variable Count':n_list[17],'Clause Count':k_list[17],'Accuracy':list_of_lists[41][2]}
newer_row_43 = {'Variable Count':n_list[18],'Clause Count':k_list[18],'Accuracy':list_of_lists[42][2]}
newer_row_44 = {'Variable Count':n_list[19],'Clause Count':k_list[19],'Accuracy':list_of_lists[43][2]}
newer_row_45 = {'Variable Count':n_list[20],'Clause Count':k_list[20],'Accuracy':list_of_lists[44][2]}
newer_row_46 = {'Variable Count':n_list[21],'Clause Count':k_list[21],'Accuracy':list_of_lists[45][2]}
newer_row_47 = {'Variable Count':n_list[22],'Clause Count':k_list[22],'Accuracy':list_of_lists[46][2]}
newer_row_48 = {'Variable Count':n_list[23],'Clause Count':k_list[23],'Accuracy':list_of_lists[47][2]}


# In[ ]:


new_df = new_df.append(newer_row_25, ignore_index=True)
new_df = new_df.append(newer_row_26, ignore_index=True)
new_df = new_df.append(newer_row_27, ignore_index=True)
new_df = new_df.append(newer_row_28, ignore_index=True)
new_df = new_df.append(newer_row_29, ignore_index=True)
new_df = new_df.append(newer_row_30, ignore_index=True)
new_df = new_df.append(newer_row_31, ignore_index=True)
new_df = new_df.append(newer_row_32, ignore_index=True)
new_df = new_df.append(newer_row_33, ignore_index=True)
new_df = new_df.append(newer_row_34, ignore_index=True)
new_df = new_df.append(newer_row_35, ignore_index=True)
new_df = new_df.append(newer_row_36, ignore_index=True)
new_df = new_df.append(newer_row_37, ignore_index=True)
new_df = new_df.append(newer_row_38, ignore_index=True)
new_df = new_df.append(newer_row_39, ignore_index=True)
new_df = new_df.append(newer_row_40, ignore_index=True)
new_df = new_df.append(newer_row_41, ignore_index=True)
new_df = new_df.append(newer_row_42, ignore_index=True)
new_df = new_df.append(newer_row_43, ignore_index=True)
new_df = new_df.append(newer_row_44, ignore_index=True)
new_df = new_df.append(newer_row_45, ignore_index=True)
new_df = new_df.append(newer_row_46, ignore_index=True)
new_df = new_df.append(newer_row_47, ignore_index=True)
new_df = new_df.append(newer_row_48, ignore_index=True)


# In[ ]:


new_df


# In[ ]:




