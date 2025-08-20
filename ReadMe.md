# Gather3d Evo - Python
### The following project allows users to compute 2, or 3 dimensional problems from the field of game theory. It is an implementation of work present in paper "". Please cite our work using a following formula "".

### The following repository contains both spatial and mixed games, that can be updated in multiple ways. All configuration is done via a YAML file. The implementation of all program elements allow simple adjustments and modifications of all provided functions.

## Installation
### Our application was developed using python 3.11.3, however it shall run smoothly with other modern python versions.

## For python 3.11.3
```console
pip install requiremens.txt
```

## In case of conflicts try a minimal version
```console
pip install requiremens_minimal.txt
```
## 1. First run
### To run an algorithm use a following command
```console
python main.py --yaml-path "<PATH TO YOUR YAML FILE>"
```
#### If a --yaml-path argument is not used a default yaml file is being loaded.
#### The results of analysis are saved in runs folder.

### To visualise the results of computations, use a following command: 
```console
python visualise.py 
```

## 2. Algorithm overview

## 3. YAML overview

## 4. Implemented problems
### 4.1 Hawk Dove problem
Hawk-dove is a state-of-the-art problem from the game theory domain. This problem assumes two phenotypes (decisions), between which players can choose. The fitness matrix is defined by 2 parameters - **V** (value of contest) and **C** (cost of escalated fight). 

$\begin{matrix}  & enemy \ Hawk & enemy \ Dove \\ player \ Hawk & (V-C)/2 & V \\ player \ Dove & 0 & V/2 \end{matrix}$

#### yaml command
```yaml
problem_name: HawkDoveProblem
```
#### yaml command
```yaml
# Example set of parameters
problem_params:
  V_param: 9
  C_param: 6
```

#### yaml command
```yaml
# Optional
# Example set of initial probabilities
initial_probability:
  Hawk: 0.29
  Dove: 0.71
```


### 4.2 Dynamic Hawk Dove problem
Dynamic Hawk Dove problem is a modification of a well Hawk Dove problem. Apart from **V** and **C** parameters, the dynamic version introduces the **r** (resource function value) parameter. The resource function for this problem must be additionally declared. Parameter **r** might depend on time (number of epochs), amount of selected phenotype in the whole matrix, or amount of a phenotype in a neighbourhood.

$\begin{matrix}  & enemy \ Hawk & enemy \ Dove \\ player \ Hawk & (V-C)/2 & V \\ player \ Dove & r * V * 0.25 & V*0.5*(r+1) \end{matrix}$

#### yaml command
```yaml
problem_name: HawkDoveDynamicProblem
```
#### yaml command
```yaml
# Example set of parameters
problem_params:
  V_param: 9
  C_param: 6

```

#### yaml command
```yaml
# Optional
# Example set of initial probabilities
initial_probability:
  Hawk: 0.29
  Dove: 0.71
```

### 4.3 Apoptosis problem
$\begin{matrix}  
        & enemy \ K & enemy \ M & enemy \ N \\ 
player \ K & 1 - a + b & 1 - a & 1-a \\ 
player \ M & 1+b+c & 1+c & 1+c \\  
player \ N & 1+b & 1 & 1
\end{matrix}$

#### yaml command
```yaml
problem_name: ApoptosisProblem
```
#### yaml command
```yaml
# Example set of parameters
problem_params:
  a_param: 0.2
  b_param: 0.3
  c_param: 0
```
## 5. Mortality
### Asynch
#### Select one random cell for reproduction in an epoch.

#### yaml command
```yaml
mortality_strategy: ASynch
```


### Semi Synch
#### Each cell each cell has some probability of being selected, given probability by an additional parameter 'mortality_rate'. It is important to note, that random number of cells is selected in each epoch, however in most cases it is close to the N% of all cells.
#### yaml command
```yaml
mortality_strategy: SemiSynch
```

### Synch
#### All cells are selected for the reproduction in each epoch.
#### yaml command
```yaml
mortality_strategy: Synch
```


## 6. Neighbourhood

### Von Neumann
### MOORE

## 7. Reproduction
### Deterministic
### Probabilistic
### Weighted


## 8. Resource Function

### Single Step resource function
### Step resource function
### Linear resource function
### Quadratic resource function
### Reciprocal resource function

### Cosinus resource function

## 9. Implemented parallelism
