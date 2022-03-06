# Quantum-3SAT-Solver
This project proposes a new algorithm to solve 3-SAT problem by utilizing quantum properties and classic random walk approach. This documentation will help you to try different setups yourself.

# Requirements
Python version 3.7.1  
Qiskit version 0.19.1 

# Reproduction of the Results

If you want to produce the results demonstrated in our publication, you can use the input files that we provide. We named them for each different n and k values. You can run the code from the terminal as follows.

# Parameters

We want to clarify what each and every parameter do.  
- CNF: Input file to be selected.
- n: Number of variables.
- k: Number of clauses.
- shot_count: Number of repetitions of the quantum simulator.
- min_step: Minimum step count for the quantum algorithm.
- max_step: Maximum step count for the quantum algorithm.
- goal_accuracy: Target values that the algorithm aims to reach.
- total_iteration: Total iteration count for the quantum algorithm.

# Running the Code

There are some parameters that you have to specify and some you can specify. You have to make sure to chose your input file and you should define n and k values as well as goal accuracy you want to reach. You can change the shot count, max or min step value, or total iteration to your demand, however, they already have their default values set.

To run with default values try the following.  

```
python run_experiment.py datafile3_7.txt 3 7 0.80  
```

Following is an example of how can you run the code with specified values.  
```
python run_experiment.py datafile3_7.txt 3 7 0.80 -min_step=1 -max_step=30 -shot_count=5000 -total_iteration=35  
```

# Results

There will be 3 output files generated.  
Accuracy file will be demonstrating the accuracy value in the designated step.  
Gates file and depth file will be demonstrating gate count and depth count respectively.

