import os
import json
from gurobipy import Model, GRB

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Ensure numeric types
SeniorWage = float(data["SeniorWage"])
YoungAdultWage = float(data["YoungAdultWage"])
MaxWeeklyWageBill = float(data["MaxWeeklyWageBill"])
MinWorkersPerDay = int(data["MinWorkersPerDay"])
MinYoungAdultsPerDay = int(data["MinYoungAdultsPerDay"])
MinYoungToSeniorRatio = float(data["MinYoungToSeniorRatio"])

# Define the variables (nonnegative integers)
numSeniors = model.addVar(vtype=GRB.INTEGER, name="numSeniors", lb=0)
numYoungAdults = model.addVar(vtype=GRB.INTEGER, name="numYoungAdults", lb=0)

model.update()

# Define the constraints
model.addConstr(SeniorWage * numSeniors + YoungAdultWage * numYoungAdults <= MaxWeeklyWageBill, name="MaxWeeklyWageBill")
model.addConstr(numSeniors + numYoungAdults >= MinWorkersPerDay, name="MinWorkers")
model.addConstr(numYoungAdults >= MinYoungAdultsPerDay, name="MinYoungAdultsPerDay")
model.addConstr(numYoungAdults >= MinYoungToSeniorRatio * numSeniors, name="MinYoungToSeniorRatio")

# Define the objective
model.setObjective(SeniorWage * numSeniors + YoungAdultWage * numYoungAdults, GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    print("Model status:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))