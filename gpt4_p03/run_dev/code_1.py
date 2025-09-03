import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

# Assuming the data.json is already properly formatted and contains the needed parameters
with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters
AdvertisingBudget = data["AdvertisingBudget"]
CostRadioAd = data["CostRadioAd"]
CostSocialMediaAd = data["CostSocialMediaAd"]
ExposureRadioAd = data["ExposureRadioAd"]
ExposureSocialMediaAd = data["ExposureSocialMediaAd"]
MinRadioAds = data["MinRadioAds"]
MaxRadioAds = data["MaxRadioAds"]
MinSocialMediaAds = data["MinSocialMediaAds"]

### Define the variables
NumRadioAds = model.addVar(vtype=GRB.INTEGER, name="NumRadioAds")
NumSocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="NumSocialMediaAds")

### Define the constraints
model.addConstr(CostRadioAd * NumRadioAds + CostSocialMediaAd * NumSocialMediaAds <= AdvertisingBudget, "BudgetConstraint")
model.addConstr(NumRadioAds >= MinRadioAds, "MinRadioAds")
model.addConstr(NumRadioAds <= MaxRadioAds, "MaxRadioAds")
model.addConstr(NumSocialMediaAds >= MinSocialMediaAds, "MinSocialMediaAds")
model.addConstr(NumRadioAds >= 0, "NonNegativityRadio")
model.addConstr(NumSocialMediaAds >= 0, "NonNegativitySocialMedia")

### Define the objective
model.setObjective(ExposureRadioAd * NumRadioAds + ExposureSocialMediaAd * NumSocialMediaAds, GRB.MAXIMIZE)

### Optimize the model
model.optimize()

### Output optimal objective value
if model.status == GRB.OPTIMAL:
    optimal_value = model.ObjVal  # Correct attribute name from objVal to ObjVal
    print("Optimal Objective Value: ", optimal_value)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
else:
    print("Optimal solution not found. Model status:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write("Model Status: " + str(model.status))