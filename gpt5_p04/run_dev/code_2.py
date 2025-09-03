import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum

# Assuming that the data.json file is properly formatted and contains the needed data

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

TotalGold = data["TotalGold"] # Total amount of gold available
GoldPerLong = data["GoldPerLong"] # Gold required per long cable
GoldPerShort = data["GoldPerShort"] # Gold required per short cable
MinShortToLongRatio = data["MinShortToLongRatio"] # Minimum ratio of short to long cables
MinLongCables = data["MinLongCables"] # Minimum number of long cables
ProfitPerLong = data["ProfitPerLong"] # Profit per long cable
ProfitPerShort = data["ProfitPerShort"] # Profit per short cable

### Define the variables

x = model.addVar(vtype=GRB.INTEGER, name="LongCables") # Number of long cables
y = model.addVar(vtype=GRB.INTEGER, name="ShortCables") # Number of short cables

### Define the constraints

model.addConstr(GoldPerLong * x + GoldPerShort * y <= TotalGold, "GoldLimitation")
model.addConstr(y >= MinShortToLongRatio * x, "MinShortToLongRatioRequirement")
model.addConstr(x >= MinLongCables, "MinLongCablesRequirement")
model.addConstr(x >= 0, "NonNegativityForLongCables")
model.addConstr(y >= 0, "NonNegativityForShortCables")

### Define the objective

model.setObjective(ProfitPerLong * x + ProfitPerShort * y, GRB.MAXIMIZE)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write("Optimal long cables: {}\nOptimal short cables: {}\nMaximum Profit: ${}".format(int(model.getVarByName("LongCables").X), int(model.getVarByName("ShortCables").X), model.objVal))
    print("Optimal long cables: ", int(model.getVarByName("LongCables").X))
    print("Optimal short cables: ", int(model.getVarByName("ShortCables").X))
    print("Maximum Profit: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write("Model did not reach optimality")
print("Model status: ", model.status)