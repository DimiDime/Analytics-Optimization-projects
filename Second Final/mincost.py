# Inports
from pyomo.core import Constraint
from pyomo.environ import *

# Create an instance of the model
model = AbstractModel()

# Set Nodes list
model.N = Set()
# Set Arcs
model.A = Set(within = model.N * model.N)

# Set origin
model.origin = Param(within = model.N)
# Set destination
#model.destination = Param(model.N)
# Set transition
#model.transition = Param(model.A)
# Set costs
model.costs = Param(model.A)
# Set capacity
model.capacity = Param(model.A)
# Set demand
model.demand = Param(model.N)

# Set the decission variables => number of flows
model.flow = Var(model.A,within=NonNegativeReals)

# Define objective function
def minCost_rule(model):
    '''
    Defines the objective functions, which ensure that the objective of the model is properly calculated. The constraint multiplies the cost of the chosed arc with the flow of the commodities. The function is defined over the set of costs and flows using the Objective class.
    '''
    return sum((model.flow[i,j] * model.costs[i,j]) for (i,j) in model.A)
model.minCost = Objective(rule=minCost_rule, sense=minimize)

#Define minimum demand constraint
def demand_rule(model,i):
    '''
    Defines the demand constraints, which ensure that the final Nodes receives the necessary amount of units. This constraint is defined over the set of nodes using the Constraint class.
    '''
    if i == "Leningrad" or i == "Moscow" or i == "Stalingrad":
        return sum(model.flow[s,d] for (s,d) in model.A if d==i)>=model.demand[i]
    else: 
        return Constraint.Skip
model.demandConstraint = Constraint(model.N, rule=demand_rule)

# Create the capacity constraints
def capacity_rule(model,i,j):
    '''
    Defines the capacity constraints, which ensure that the flow on each arc does not exceed the capacity of that arc. This constraint is defined over the set of arcs (model.A) using the Constraint class.
    '''
    return model.flow[i,j] <= model.capacity[i,j]

model.capacityConstraint = Constraint(model.A, rule=capacity_rule)


# Create the flow conservation constraints
def conservation_rule(model, node):
    '''
    Defines the flow conservation constraints, which ensure that flow is conserved at each node. This constraint is defined over the set of nodes (model.N) using the Constraint class.
    '''
    if node == "Berlin" or node == "Laipzig" or node == "Munic":
        return Constraint.Skip
    if node == "Leningrad" or node == "Moscow" or node == "Stalingrad":
        #return sum(model.flow[arc] for arc in model.A if arc[1] == node) == 1
        return Constraint.Skip
    # Incoming node
    incoming = sum(model.flow[i,j] for (i,j) in model.A if node==i) # in
    # Outgoing node
    outgoing = sum(model.flow[i,j] for (i,j) in model.A if node==j) # out
    return incoming == outgoing

model.conservationConstraint = Constraint(model.N, rule=conservation_rule)
