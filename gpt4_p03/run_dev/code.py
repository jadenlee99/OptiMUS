
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AdvertisingBudget = data["AdvertisingBudget"] # shape: [], definition: AdvertisingBudget parameter

CostRadioAd = data["CostRadioAd"] # shape: [], definition: CostRadioAd parameter

CostSocialMediaAd = data["CostSocialMediaAd"] # shape: [], definition: CostSocialMediaAd parameter

ExposureRadioAd = data["ExposureRadioAd"] # shape: [], definition: ExposureRadioAd parameter

ExposureSocialMediaAd = data["ExposureSocialMediaAd"] # shape: [], definition: ExposureSocialMediaAd parameter

MinRadioAds = data["MinRadioAds"] # shape: [], definition: MinRadioAds parameter

MaxRadioAds = data["MaxRadioAds"] # shape: [], definition: MaxRadioAds parameter

MinSocialMediaAds = data["MinSocialMediaAds"] # shape: [], definition: MinSocialMediaAds parameter



### Define the variables

NumRadioAds = model.addVar(vtype=GRB.INTEGER, name="NumRadioAds")

NumSocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="NumSocialMediaAds")



### Define the constraints

model.addConstr(CostRadioAd * NumRadioAds + CostSocialMediaAd * NumSocialMediaAds <= AdvertisingBudget)
model.addConstr(NumRadioAds >= MinRadioAds)
model.addConstr(NumRadioAds <= MaxRadioAds)
model.addConstr(NumSocialMediaAds >= MinSocialMediaAds)
model.addConstr(NumRadioAds >= 0)
model.addConstr(NumSocialMediaAds >= 0)


### Define the objective

model.setObjective(ExposureRadioAd * NumRadioAds + ExposureSocialMediaAd * NumSocialMediaAds, GRB.MAXIMIZE)


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
