
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalBudget = data["TotalBudget"] # shape: [], definition: TotalBudget parameter

ProfitPerDollarCondos = data["ProfitPerDollarCondos"] # shape: [], definition: ProfitPerDollarCondos parameter

ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"] # shape: [], definition: ProfitPerDollarDetachedHouses parameter

MinimumPercentageCondos = data["MinimumPercentageCondos"] # shape: [], definition: MinimumPercentageCondos parameter

MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"] # shape: [], definition: MinimumInvestmentDetachedHouses parameter



### Define the variables

investCondos = model.addVar(vtype=GRB.CONTINUOUS, name="investCondos")

investDetachedHouses = model.addVar(vtype=GRB.CONTINUOUS, name="investDetachedHouses")



### Define the constraints

model.addConstr(investCondos + investDetachedHouses <= TotalBudget)
model.addConstr((1 - MinimumPercentageCondos) * investCondos - MinimumPercentageCondos * investDetachedHouses >= 0)
model.addConstr(investDetachedHouses >= MinimumInvestmentDetachedHouses)


### Define the objective

del.setObjective(ProfitPerDollarCondos * investCondos + ProfitPerDollarDetachedHouses * investDetachedHouses, GRB.MAXIMIZE


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
