
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSandwichTypes = data["NumSandwichTypes"] # shape: [], definition: NumSandwichTypes parameter

NumIngredients = data["NumIngredients"] # shape: [], definition: NumIngredients parameter

Required = data["Required"] # shape: [2, 2], definition: Required parameter

TotalAvailable = data["TotalAvailable"] # shape: [2], definition: TotalAvailable parameter

ProfitPerSandwich = data["ProfitPerSandwich"] # shape: [2], definition: ProfitPerSandwich parameter



### Define the variables

numSandwiches = model.addVars(NumSandwichTypes, vtype=GRB.INTEGER, name="numSandwiches")



### Define the constraints

model.addConstr(sum(Required[0][j] * numSandwiches[j] for j in range(NumSandwichTypes)) <= TotalAvailable[0])
model.addConstr(sum(Required[1][t] * numSandwiches[t] for t in range(NumSandwichTypes)) <= TotalAvailable[1])
for i in range(NumSandwichTypes):
    model.addConstr(numSandwiches[i] >= 0)


### Define the objective

del.setObjective(quicksum(ProfitPerSandwich[i] * numSandwiches[i] for i in range(NumSandwichTypes)), GRB.MAXIMIZE


### Optimize the model

model.optimize()



### Output optimal objective value

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
