import os
import json
from gurobipy import Model, GRB

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalGold = data["TotalGold"]
GoldPerLong = data["GoldPerLong"]
GoldPerShort = data["GoldPerShort"]
MinShortToLongRatio = data["MinShortToLongRatio"]
MinLongCables = data["MinLongCables"]
ProfitPerLong = data["ProfitPerLong"]
ProfitPerShort = data["ProfitPerShort"]

# Variables
numLong = model.addVar(vtype=GRB.INTEGER, name="numLong")
numShort = model.addVar(vtype=GRB.INTEGER, name="numShort")

# Constraints
model.addConstr(GoldPerLong * numLong + GoldPerShort * numShort <= TotalGold, name="gold")
model.addConstr(MinShortToLongRatio * numLong <= numShort, name="ratio")
model.addConstr(numLong >= MinLongCables, name="minLong")

# Objective
model.setObjective(ProfitPerLong * numLong + ProfitPerShort * numShort, GRB.MAXIMIZE)

# Optimize
model.optimize()

# Output
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    print("Model Status: ", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))