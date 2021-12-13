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


def blackBox (mycircuit,qreg,n, k, nextLine):
    ancillaList=[]
    clauselength=6 #6 sabit olmamalı
    for i in range(n+1, n+k+1):
        ancillaList.append(qreg[i])
 ############ her clause için
    for j in range(k):
        ########### not ###########3
        initElement = clauselength*j
        for i in range(3):
            if (int(nextLine[initElement+2*i+1])==0):
                mycircuit.x(qreg[int(nextLine[initElement+2*i])])
        ##################### or ########################
        orList=[]
        for i in range(n): 
            mycircuit.x(qreg[i+1])
            orList.append(qreg[i+1])
       
        mycircuit.mcx(orList,ancillaList[j])
        mycircuit.x(ancillaList[j])

        for i in range(n): 
            mycircuit.x(qreg[i+1])
            ################  not geri al #################
        for i in range(3):
            if (int(nextLine[initElement+2*i+1])==0):
                mycircuit.x(qreg[int(nextLine[initElement+2*i])])
    ############# or ları notla ################
    mycircuit.mcx(ancillaList,qreg[0])
    ############# ancila listi geri al
    ############ her clause için
    for j in range(k):
        
        ########### not ###########3
        initElement = clauselength*j
        for i in range(3):#3 değil n
            if (int(nextLine[initElement+2*i+1])==0):
                mycircuit.x(qreg[int(nextLine[initElement+2*i])])
               # print(int(nextLine[initElement+2*i])-1)
       ##################### or ########################
        orList=[]
        for i in range(n):
            mycircuit.x(qreg[i+1])
            orList.append(qreg[i+1])
       
        mycircuit.x(ancillaList[j])
        mycircuit.mcx(orList,ancillaList[j])
       
        for i in range(n): 
            mycircuit.x(qreg[i+1])
            
        ################  not geri al #################
        for i in range(3):
            if (int(nextLine[initElement+2*i+1])==0):
                mycircuit.x(qreg[int(nextLine[initElement+2*i])])


# In[3]:


def inversion(circuit,quantum_reg,n):
    
    
    #step 1
    for i in range(1,n+1):
        circuit.h(quantum_reg[i])
    
    #step 2
 
    for i in range(1,n+1):
        circuit.x(quantum_reg[i])

 

    #step 3
    #[0...n-1] control list, extra qubit list
    controlQubits=[]
    
    for i in range(n):
        controlQubits.append(quantum_reg[i+1])
    
    circuit.mcx(controlQubits, quantum_reg[0])
        
    #step 4

    for i in range(1,n+1):
        circuit.x(quantum_reg[i])
    #step 5
   
    for i in range(1,n+1):
        circuit.h(quantum_reg[i])

 

    #step 6
    circuit.x(quantum_reg[0])


# In[4]:


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, BasicAer, IBMQ, execute
from qiskit.tools.visualization import plot_histogram

k=7 #number of clauses
n=3 #number of variables
maxN= max(n+k+1,2*n-1)


nextLine= '102030112130102131102130102031112030112031'

qreg = QuantumRegister(maxN)  # quantum register with max(n+2*k+2+k,2*n+1) qubits
creg = ClassicalRegister(maxN)  # classical register with max(n+2*k+2+k,2*n+1) bits
mycircuit = QuantumCircuit(qreg, creg)  # quantum circuit with quantum and classical registers


for i in range(1, n+1):
    mycircuit.h(qreg[i])
    

    
iterations = 3

mycircuit.h(qreg[0])
mycircuit.x(qreg[0])

for i in range(iterations):
    #query
    blackBox(mycircuit, qreg, n, k, nextLine)
    mycircuit.barrier()
    #inversion
    inversion(mycircuit, qreg,n)
    mycircuit.barrier()


mycircuit.x(qreg[0])
mycircuit.h(qreg[0])  
    
mycircuit.measure(qreg, creg)

job = execute(mycircuit, Aer.get_backend('qasm_simulator'), shots=1000)
#job = execute(mycircuit, backend= simulator_backend, shots=8192)
counts = job.result().get_counts(mycircuit)

# print the reverse of the outcome
for outcome in counts:
    reverse_outcome = ''
    for i in outcome:
        reverse_outcome = i + reverse_outcome
    print(reverse_outcome, "is observed", counts[outcome], "times")
print("\n")


# In[5]:


mycircuit.draw()


# In[ ]:




