import json
import sys

try:
    from gurobipy import Model, GRB
except ImportError:
    sys.exit("GurobiPy module is not installed. Please ensure you have Gurobi and its Python package installed correctly.")

model = Model("OptimizationProblem")

# Define the parameters
TotalBudget = 760000
ProfitPerDollarCondos = 0.50
ProfitPerDollarDetachedHouses = 1.00
MinimumPercentageCondos = 0.20
MinimumInvestmentDetachedHouses = 20000

# Define the variables
investmentCondos = model.addVar(vtype=GRB.CONTINUOUS, name="investmentCondos")
investmentDetachedHouses = model.addVar(vtype=GRB.CONTINUOUS, name="investmentDetachedHouses")

# Define the constraints
model.addConstr(investmentCondos + investmentDetachedHouses <= TotalBudget)
model.addConstr(investmentCondos >= MinimumPercentageCondos * (investmentCondos + investmentDetachedHouses))
model.addConstr(investmentDetachedHouses >= MinimumInvestmentDetachedHouses)
model.addConstr(investmentCondos >= 0)
model.addConstr(investmentDetachedHouses >= 0)

# Define the objective
model.setObjective(ProfitPerDollarCondos * investmentCondos + ProfitPerDollarDetachedHouses * investmentDetachedHouses, GRB.MAXIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))