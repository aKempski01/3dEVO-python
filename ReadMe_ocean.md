# Gather3d Evo - Python
# This is not a repository. This implementation was added to enable quick tests of our implementation.

# If you would like to use graphical interface download the newest version of software from the official github repository.
## "https://github.com/aKempski01/3dEVO-python"

### The following repository contains both spatial and mixed games, that can be updated in multiple ways. All configuration is done via a YAML file. The implementation of all program elements allow simple adjustments and modifications of all provided functions.


#### 1. [Algorithm overview](#Algorithm-overview)
#### 1.1 [The initial matrix](#The-initial-matrix)

#### 2. [Implemented Problems](#Implemented-problems)
#### 2.1 [Hawk Dove](#Hawk-Dove-problem)
#### 2.2 [Hawk Dove with resource function](#Dynamic-Hawk-Dove-problem)
#### 2.3 [Avoidance of apoptosis](#Apoptosis-problem)


#### 3. [Mortality](#Mortality)
#### 3.1 [Asynch](#Asynch)
#### 3.2 [Semi Synch](#Semi-Synch)
#### 3.3 [Synch](#Synch)

#### 4. [Neighbourhood](#Neighbourhood)
#### 4.1 [Von Neumann](#Von-Neumann)
#### 4.2 [Moore](#Moore)

#### 5. [Reproduction](#Reproduction)
#### 5.1 [Deterministic](#Deterministic)
#### 5.2 [Probabilistic](#Probabilistic)
#### 5.3 [Weighted](#Weighted)

#### 6. [Resource Function](#Resource-Function)
#### 6.1 [Single Step resource function](#Single-Step-resource-function)
#### 6.2 [Linear resource function](#Linear-resource-function)
#### 6.3 [Quadratic resource function](#Quadratic-resource-function)
#### 6.4 [Reciprocal resource function](#Reciprocal-resource-function)
#### 6.5 [Cosinus resource function](#Cosinus-resource-function)

---

---


# First run
### To run an algorithm edit a run command in a code directory.
```console
python main.py --yaml-path "<PATH TO YOUR YAML FILE>"
```
#### If a --yaml-path argument is not used a default yaml file is being loaded.
#### The results of analysis are saved in the results/runs folder.

### You can visualise the results by observing the changes on the history plot. For GUI download code from our repository.
### "https://github.com/aKempski01/3dEVO-python"

---

---

## Algorithm overview
The evolutionary game takes place in so-called game array. Our software allows users to solve 2 and 3 dimensional problems, with an unlimited number of phenotypes (decisions). 
In each iteration a chosen mortality method selects N cell to be replaced/updated. Selected cells are being replaced using a reproduction method. 
It can be said that a cell is updated based on its neighbours and their fitness function.
The fitness for each cell is determined, by the chosen game theory problem. The fitness is calculated as the cell's phenotype against each neighbour's phenotype. 

<img src="/readme_files/fitness_formula.png" alt="">

* f - problem matrix
* f(i,j) - the value of problem matrix - player strategy i against enemy strategy j
* $G_i$ - Game array containing the allocations of phenotype i
* $G_i$[p] - The value of phenotype i in the player cell p
* $G_i$[q] - The value of phenotype i in the enemy cell q
* H - Set of neighbour's indices
* K - Num. Phenotypes.



### The matrix 
2 Dimensional game requires 3-dimensional matrix and 3-dimensional game requires 4 dimensional matrix. Additional dimension stores information about phenotype allocation in a given cell.

#### Example:
The game matrix of a 2-d problem with 3 phenotypes and population length equal to 10 is a matrix of size 10X10X3.

The phenotype allocation values are in range <0; 1> and their sum must be equal to 1 for each cell.

## The initial matrix
The matrix to be initiated requires an information about the number of dimensions and about the length of population. 
Additionally, it is required to determine the name of the problem (number and names of phenotypes is stored inside the problem class).

#### yaml command
```yaml
# Example set of parameters
population_length: 10

# number of dimensions can be equal to 2 or 3 
num_dim: 2

# problem name shall be the same as the name of class, 
# that describes a given problem
problem_name: HawkDoveProblem
```
If you would like to control the distribution of initial phenotypes the following parameter can be added.
#### yaml command
```yaml
# Example set of parameters

# It is important, that the names of phenotypes 
# match the names declared in the problem class.
initial_probability:
  Hawk: 0.43
  Dove: 0.57
```

I you do not want to randomize the initial game matrix, you can load one by using the parameter shown below. The process of correct creation of initial game matrix is shown in attached jupiter notebook "create_game_matrix.ipynb". 

#### yaml command
```yaml
# Put path to initial matrix. If you want to generate matrix on random put None.
initial_matrix: <Put tour path here>
```

---

---

# Implemented problems
### Hawk Dove problem
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


### Dynamic Hawk Dove problem
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

### Apoptosis problem
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

---

---

# Mortality
### Asynch
#### Select one random cell for reproduction in an epoch.

#### yaml command
```yaml
mortality_strategy: ASynch
```


### Semi Synch
#### Each cell each cell has some probability of being selected, given probability by an additional parameter 'mortality_rate'.  It is important to note, that random number of cells is selected in each epoch, however in most cases it is close to the N% of all cells.
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

---

---

## Neighbourhood
#### The cells are updated based on their neighbor's fitness functions. This is why the proper choice of a neighbourhood is crucial for solving spatial games. 

### Von Neumann
#### Only cells that are connected with a full edge/face are selected.

<img src="/readme_files/vonNeumann.png" alt="">

```yaml
neighbourhood_type: VonNeumann
```

### MOORE
#### All surrounding cells are selected.

<img src="/readme_files/moore.png" alt="">

```yaml
neighbourhood_type: Moore
```

---

---

## Reproduction
Reproduction determines the new value of the cell based on its neighbours fitness values. 

### Deterministic
Replacing the selected cell with the neighbouring one with the highest fitness value.

### Probabilistic
Replacing the selected cell with the randomly chosen neighbour with probability proportional to its fitness value.

### Weighted
The value of the selected cell is set to the weighted mean of all neighbours with respect to their fitness values. The weighted method is only available for the mixed game arrays. 

---

---

## Resource Function
The parameter **r**, which might be used in dynamic problems to adjust the values of game matrix, is a result of function **R(x)**, where x can be a current epoch value, amount of a selected phenotype in the neighbourhood, or amount of a selected phenotype in the whole game matrix.
The resource function operates in 3 modes:
* local -> x = sum of allocation to certain phenotype for neighbours (normalised 0-1)
* global -> X = sum of allocation to certain phenotype for all cells (normalised 0-1) 
* time -> X = epoch num



### Single Step resource function
* local: Not supported
* global: Not supported
* time:
```
if x < step_epoch
    R(X) = step_initial_value 
else
    R(X) = step_int
```
#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: QuadraticResourceFunction
resource_function_params:
  #conly time mode supported
  mode: time 


# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk

  step_initial_value: 0
  step_inc: 1
  step_epoch: 200
```
---

### Step resource function
* local: Not supported
* global: Not supported
* time:
```
if x % step_epoch == 0
    R(X) += step_int
```

#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: QuadraticResourceFunction
resource_function_params:
  #conly time mode supported
  mode: time 


# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk

  step_initial_value: 0
  step_inc: 1
  step_epoch: 200
```

---

### Linear resource function
* local/global/time: 
```
R(X) = 1 - a_param * X + b_param
```

#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: QuadraticResourceFunction
resource_function_params:
  #choose one mode
  mode: time 
#  mode: local
#  mode: global

# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk

  a_param: -1
  b_param: 0
```

---

### Quadratic resource function
* local/global/time: 
```
R(X) = 1 - (X * X * a_param + X * b_param + c_param)
```

#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: QuadraticResourceFunction
resource_function_params:
  #choose one mode
  mode: time 
#  mode: local
#  mode: global

# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk

  a_param: -1
  b_param: 0
  c_param: 1

```

---

### Reciprocal resource function
* local/global/time: 
```
R(X) = 1 - k_param - (a_param)/(X-h_param)
```


#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: ReciprocalResourceFunction
resource_function_params:
  #choose one mode
  mode: time 
#  mode: local
#  mode: global

# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk

  a_param: -1

  k_param: 1
  h_param: 0.1
```
---

### Cosinus resource function
* local/global/time: 
```
R(X) = 1 - average_cos_value - cos(X  * num_periods * pi * 2 + offset * 2 * pi)
```

#### yaml command
```yaml
# Example set of parameters
chosen_resource_function: CosResourceFunction
resource_function_params:
  #choose one mode
  mode: time 
#  mode: local
#  mode: global

# select phenotype or phenotypes for local/global mode
  resource_phenotypes:
    ph1: Hawk


  num_periods: 2
  average_cos_value: 0
  offset: 0
```

---
---




