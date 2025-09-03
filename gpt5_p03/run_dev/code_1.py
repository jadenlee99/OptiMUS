import os
import json
from gurobipy import Model, GRB

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters (cast to appropriate numeric types)
AdvertisingBudget = float(data["AdvertisingBudget"])
CostRadioAd = float(data["CostRadioAd"])
CostSocialMediaAd = float(data["CostSocialMediaAd"])
ExposureRadioAd = float(data["ExposureRadioAd"])
ExposureSocialMediaAd = float(data["ExposureSocialMediaAd"])
MinRadioAds = int(data["MinRadioAds"])
MaxRadioAds = int(data["MaxRadioAds"])
MinSocialMediaAds = int(data["MinSocialMediaAds"])

# Define the variables
numRadioAds = model.addVar(vtype=GRB.INTEGER, name="numRadioAds")
numSocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="numSocialMediaAds")

# Define the constraints
model.addConstr(CostRadioAd * numRadioAds + CostSocialMediaAd * numSocialMediaAds <= AdvertisingBudget, name="budget")
model.addConstr(numRadioAds >= MinRadioAds, name="min_radio")
model.addConstr(numRadioAds <= MaxRadioAds, name="max_radio")
model.addConstr(numSocialMediaAds >= MinSocialMediaAds, name="min_social")

# Define the objective
model.setObjective(ExposureRadioAd * numRadioAds + ExposureSocialMediaAd * numSocialMediaAds, GRB.MAXIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value (only if optimal)
if model.status == GRB.OPTIMAL:
    obj_val = model.objVal
    print("Optimal Objective Value: ", obj_val)
    with open("output_solution.txt", "w") as f:
        f.write(str(obj_val))
else:
    # write the status code or a message to the output file
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
    print("Model did not solve to optimality. Status:", model.status)