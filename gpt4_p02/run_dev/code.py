
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

xRegular = model.addVar(vtype=GRB.INTEGER, name="xRegular")

xSpecial = model.addVar(vtype=GRB.INTEGER, name="xSpecial")



### Define the constraints

model.addConstr(2 * xRegular + 3 * xSpecial <= 40)
model.addConstr(3 * xRegular + 5 * xSpecial <= 70)
model.addConstr(xRegular >= 0, "NonNegativeRegular")
model.addConstr(xSpecial >= 0, "NonNegativeSpecial")


### Define the objective

model.setObjective(3 * xRegular + 4 * xSpecial, GRB.MAXIMIZE)


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
