import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
TotalBudget = data["TotalBudget"]
ProfitPerDollarCondos = data["ProfitPerDollarCondos"]
ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"]
MinimumPercentageCondos = data["MinimumPercentageCondos"]
MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"]

# Define the variables
investCondos = model.addVar(vtype=GRB.CONTINUOUS, name="investCondos")
investDetachedHouses = model.addVar(vtype=GRB.CONTINUOUS, name="investDetachedHouses")

# Define the constraints
model.addConstr(investCondos + investDetachedHouses <= TotalBudget, name="budget")
# enforce investCondos >= MinimumPercentageCondos * (investCondos + investDetachedHouses)
model.addConstr((1 - MinimumPercentageCondos) * investCondos - MinimumPercentageCondos * investDetachedHouses >= 0, name="min_condos_pct")
model.addConstr(investDetachedHouses >= MinimumInvestmentDetachedHouses, name="min_detached")

# Define the objective
model.setObjective(ProfitPerDollarCondos * investCondos + ProfitPerDollarDetachedHouses * investDetachedHouses, GRB.MAXIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value or status
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    print("Model status:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))