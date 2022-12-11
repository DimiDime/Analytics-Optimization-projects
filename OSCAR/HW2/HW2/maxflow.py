
from pyomo.environ import *

model= AbstractModel()

#NODES (countries)
model.C = Set()
#ARCS BETWEEN NODES
model.T = Set(within = model.C*model.C) #not more than one arc between nodes

#SOURCE
model.initial = Param(within = model.C)
#So we have a inital point called initial and its destination will be destination
#CAPACITIES OF EACH ARC
model.capacity = Param(model.T) # we cannot exceed these flow capacity limits
#MINIMUMS OF THE DESTINATIONS
model.minimums = Param(model.C)
#FINAL DESTINATIONS
model.destinations=Param(model.C)

#THE DECISION VARIABLE IS THE FLOWid
model.flow = Var(model.T ,within=NonNegativeReals) #model.T as is the one with all the connections, so number of connections is equal to the number of variables

#OBJECTIVE FUNCTION
#Maximize the flow so the final destinations receive as much as possible
def objective(model):
    total=0
    for (i,d) in model.T:
            if d=="UAE" or d=="Argelia" or d=="EUDistributor": #FINAL DESTINATIONS
                total+=model.flow[i,d]
    return total
    
model.obj = Objective(rule=objective, sense=maximize) #we are looking to maximize


#CONSTRAINTS
#1)Limit the flow to the capacity of the connection
def capacity_limit(model, i, d):
    return model.flow[i,d] <= model.capacity[i, d] #the flow between i (source node) and (d) destination, should be less than the pre-defined capacity between i and d


#2)Rule of the maximization problems, all the flow coming to a node, should also go out, except if we are in the first, source node, that it only goes out, 
#or if we are in one of the final destinations, that only receives the flow.
def total_flow_rule(model, k):
    if value(model.initial) == k: #if the node we are is the initial one, or one of the final destinations, skip
        return Constraint.Skip
    if k=="UAE" or k=="Argelia" or k=="EUDistributor": #FINAL DESTINATIONS
            return Constraint.Skip
    inFlow = sum(model.flow[i,d] for (i,d) in model.T if d==k) #flow entering the node
    outFlow = sum(model.flow[i,d] for (i,d) in model.T if i==k) #flow exiting the node
    return inFlow == outFlow #both should be equal


    
#3)MAKE SURE THE FINAL DESTINATIONS RECEIVE THE MINIMUM AMOUNT OF WHEAT PACTED FOR EACH OF THEM
def min_wheat(model, k):
    if k=="UAE" or k=="Argelia" or k=="EUDistributor": #FINAL DESTINATIONS
            return sum(model.flow[i, d] for (i,d) in model.T if d==k)>=model.minimums[k]
    else:
        return Constraint.Skip
        
#INCLUDE THEM IN THE MODEL
model.capacity_limit = Constraint(model.T, rule = capacity_limit)

model.total_flow_rule = Constraint(model.C, rule = total_flow_rule)

model.min_wheat = Constraint(model.C, rule = min_wheat)
