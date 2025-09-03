
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

numRadioAds = model.addVar(vtype=GRB.INTEGER, name="numRadioAds")

numSocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="numSocialMediaAds")



### Define the constraints

model.addConstr(CostRadioAd * numRadioAds + CostSocialMediaAd * numSocialMediaAds <= AdvertisingBudget)
model.addConstr(numRadioAds >= MinRadioAds)
model.addConstr(numRadioAds <= MaxRadioAds)
model.addConstr(numSocialMediaAds >= MinSocialMediaAds)
numRadioAds.vtype = GRB.INTEGER
numSocialMediaAds.vtype = GRB.INTEGER


### Define the objective

del.setObjective(ExposureRadioAd * numRadioAds + ExposureSocialMediaAd * numSocialMediaAds, GRB.MAXIMIZE


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
