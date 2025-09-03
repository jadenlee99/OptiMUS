
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SeniorWage = data["SeniorWage"] # shape: [], definition: SeniorWage parameter

YoungAdultWage = data["YoungAdultWage"] # shape: [], definition: YoungAdultWage parameter

MaxWeeklyWageBill = data["MaxWeeklyWageBill"] # shape: [], definition: MaxWeeklyWageBill parameter

MinWorkersPerDay = data["MinWorkersPerDay"] # shape: [], definition: MinWorkersPerDay parameter

MinYoungAdultsPerDay = data["MinYoungAdultsPerDay"] # shape: [], definition: MinYoungAdultsPerDay parameter

MinYoungToSeniorRatio = data["MinYoungToSeniorRatio"] # shape: [], definition: MinYoungToSeniorRatio parameter



### Define the variables

numSeniorCitizens = model.addVar(vtype=GRB.INTEGER, name="numSeniorCitizens")

numYoungAdults = model.addVar(vtype=GRB.INTEGER, name="numYoungAdults")



### Define the constraints

model.addConstr(SeniorWage * numSeniorCitizens + YoungAdultWage * numYoungAdults <= MaxWeeklyWageBill)
model.addConstr(numSeniorCitizens + numYoungAdults >= MinWorkersPerDay)
model.addConstr(numYoungAdults >= MinYoungAdultsPerDay)
model.addConstr(numYoungAdults >= numSeniorCitizens / 3)
model.addConstr(numSeniorCitizens >= 0)
model.addConstr(numYoungAdults >= 0)


### Define the objective

model.setObjective(SeniorWage * numSeniorCitizens + YoungAdultWage * numYoungAdults, GRB.MINIMIZE)


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
