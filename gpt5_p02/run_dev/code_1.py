import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
NumSandwichTypes = int(data["NumSandwichTypes"])
NumIngredients = int(data["NumIngredients"])
Required = data["Required"]
TotalAvailable = data["TotalAvailable"]
ProfitPerSandwich = data["ProfitPerSandwich"]

# Define the variables
numSandwiches = model.addVars(range(NumSandwichTypes), vtype=GRB.INTEGER, name="numSandwiches")

# Define the constraints
model.addConstr(
    quicksum(Required[0][j] * numSandwiches[j] for j in range(NumSandwichTypes)) <= TotalAvailable[0]
)
model.addConstr(
    quicksum(Required[1][j] * numSandwiches[j] for j in range(NumSandwichTypes)) <= TotalAvailable[1]
)
# non-negativity (redundant because default lb=0, but kept for clarity)
for i in range(NumSandwichTypes):
    model.addConstr(numSandwiches[i] >= 0)

# Define the objective
model.setObjective(
    quicksum(ProfitPerSandwich[i] * numSandwiches[i] for i in range(NumSandwichTypes)),
    GRB.MAXIMIZE
)

# Optimize the model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))