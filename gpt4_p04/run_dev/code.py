
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalGold = data["TotalGold"] # shape: [], definition: TotalGold parameter

GoldPerLong = data["GoldPerLong"] # shape: [], definition: GoldPerLong parameter

GoldPerShort = data["GoldPerShort"] # shape: [], definition: GoldPerShort parameter

MinShortToLongRatio = data["MinShortToLongRatio"] # shape: [], definition: MinShortToLongRatio parameter

MinLongCables = data["MinLongCables"] # shape: [], definition: MinLongCables parameter

ProfitPerLong = data["ProfitPerLong"] # shape: [], definition: ProfitPerLong parameter

ProfitPerShort = data["ProfitPerShort"] # shape: [], definition: ProfitPerShort parameter



### Define the variables

LongCables = model.addVar(vtype=GRB.INTEGER, name="LongCables")

ShortCables = model.addVar(vtype=GRB.INTEGER, name="ShortCables")



### Define the constraints

model.addConstr(GoldPerLong * LongCables + GoldPerShort * ShortCables <= TotalGold)
model.addConstr(ShortCables >= 5 * LongCables)
model.addConstr(LongCables >= MinLongCables)
model.addConstr(LongCables >= 0)
model.addConstr(ShortCables >= 0)


### Define the objective

model.setObjective(ProfitPerLong * LongCables + ProfitPerShort * ShortCables, GRB.MAXIMIZE)


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
